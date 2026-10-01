import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


# File extensions are matched to the folder where each file should go.
CATEGORIES = {
	"Images": {".bmp", ".gif", ".heic", ".jpeg", ".jpg", ".png", ".svg", ".tif", ".tiff", ".webp"},
	"Documents": {".doc", ".docx", ".odt", ".pdf", ".rtf", ".txt"},
	"Spreadsheets": {".csv", ".ods", ".xls", ".xlsx"},
	"Presentations": {".key", ".odp", ".ppt", ".pptx"},
	"Audio": {".aac", ".flac", ".m4a", ".mp3", ".ogg", ".wav", ".wma"},
	"Video": {".avi", ".m4v", ".mkv", ".mov", ".mp4", ".mpeg", ".mpg", ".webm", ".wmv"},
	"Archives": {".7z", ".bz2", ".gz", ".rar", ".tar", ".xz", ".zip"},
	"Code": {".c", ".cpp", ".css", ".html", ".java", ".js", ".json", ".py", ".rb", ".ts", ".xml", ".yaml", ".yml"},
	"Applications": {".apk", ".bat", ".deb", ".exe", ".msi", ".pkg", ".sh"},
}


# Match extensions without caring whether their letters are uppercase or lowercase.
def category_for(path):
	extension = path.suffix.lower()
	return next((name for name, extensions in CATEGORIES.items() if extension in extensions), "Other")


# Add a number to the filename when a file with that name already exists.
def unique_destination(destination):
	if not destination.exists():
		return destination

	counter = 1
	while True:
		candidate = destination.with_name(f"{destination.stem} ({counter}){destination.suffix}")
		if not candidate.exists():
			return candidate
		counter += 1


class FileSorterApp:
	def __init__(self, root):
		self.root = root
		self.root.title("File Sorter")
		self.root.geometry("760x520")
		self.root.minsize(600, 400)
		self.root.configure(background="#F1F3EE")

		self.folder = tk.StringVar()
		self.status = tk.StringVar(value="Choose a folder to start watching.")
		self.file_count = tk.StringVar(value="0 FILES")
		self.auto_sorting = tk.BooleanVar(value=True)
		self.auto_sort_label = tk.StringVar(value="AUTO SORT  ON")
		self.pause_button_label = tk.StringVar(value="Pause auto-sort")
		self.watched_folder = None
		self.known_files = set()
		self.pending_files = {}
		self.preview_entries = ()
		self.watch_job = None
		self._build_ui()

		# Start by watching Downloads when that folder is available.
		downloads = Path.home() / "Downloads"
		if downloads.is_dir():
			self._set_folder(downloads)

	def _build_ui(self):
		style = ttk.Style()
		style.theme_use("clam")
		style.configure("App.TFrame", background="#F1F3EE")
		style.configure("Header.TFrame", background="#183B33")
		style.configure("HeaderEyebrow.TLabel", background="#183B33", foreground="#D7ED79", font=("Segoe UI", 9, "bold"))
		style.configure("HeaderTitle.TLabel", background="#183B33", foreground="#FFFFFF", font=("Segoe UI", 22, "bold"))
		style.configure("HeaderCopy.TLabel", background="#183B33", foreground="#D3DFD8", font=("Segoe UI", 10))
		style.configure("Section.TLabel", background="#F1F3EE", foreground="#344940", font=("Segoe UI", 9, "bold"))
		style.configure("Count.TLabel", background="#F1F3EE", foreground="#68776D", font=("Segoe UI", 9, "bold"))
		style.configure("Status.TLabel", background="#F1F3EE", foreground="#466054", font=("Segoe UI", 9))
		style.configure("Path.TEntry", fieldbackground="#FFFFFF", foreground="#183B33", padding=(10, 9), bordercolor="#D5DDD5")
		style.configure("Browse.TButton", background="#D7ED79", foreground="#213329", padding=(16, 9), font=("Segoe UI", 9, "bold"), borderwidth=0)
		style.map("Browse.TButton", background=[("active", "#C9E45C")])
		style.configure("Sort.TButton", background="#1F5A47", foreground="#FFFFFF", padding=(18, 10), font=("Segoe UI", 10, "bold"), borderwidth=0)
		style.map("Sort.TButton", background=[("active", "#174A39")])
		style.configure("Pause.TButton", background="#E2E8DF", foreground="#294238", padding=(12, 10), font=("Segoe UI", 9, "bold"), borderwidth=0)
		style.map("Pause.TButton", background=[("active", "#D4DED1")])
		style.configure("Treeview", rowheight=30, background="#FFFFFF", fieldbackground="#FFFFFF", foreground="#263B32", font=("Segoe UI", 10), borderwidth=0)
		style.map("Treeview", background=[("selected", "#E4EFC8")], foreground=[("selected", "#183B33")])
		style.configure("Treeview.Heading", background="#E8EDE6", foreground="#53645A", font=("Segoe UI", 9, "bold"), padding=(12, 10), relief="flat")
		style.map("Treeview.Heading", background=[("active", "#E0E8DC")])
		style.configure("Vertical.TScrollbar", background="#E1E7DF", troughcolor="#F1F3EE", borderwidth=0, arrowsize=12)

		content = ttk.Frame(self.root, padding=18, style="App.TFrame")
		content.pack(fill="both", expand=True)
		content.columnconfigure(0, weight=1)
		content.rowconfigure(4, weight=1)

		header = ttk.Frame(content, style="Header.TFrame", padding=(20, 14))
		header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
		header.columnconfigure(0, weight=1)
		ttk.Label(header, text="LIVE FILE ORGANIZER", style="HeaderEyebrow.TLabel").grid(
			row=0, column=0, sticky="w"
		)
		ttk.Label(header, text="File Sorter", style="HeaderTitle.TLabel").grid(
			row=1, column=0, sticky="w", pady=(2, 1)
		)
		ttk.Label(
			header,
			text="New files are filed by type as they arrive.",
			style="HeaderCopy.TLabel",
		).grid(row=2, column=0, sticky="w")
		ttk.Label(header, textvariable=self.auto_sort_label, style="HeaderEyebrow.TLabel").grid(
			row=1, column=1, padx=(20, 0), sticky="e"
		)

		ttk.Label(content, text="WATCH FOLDER", style="Section.TLabel").grid(
			row=1, column=0, sticky="w", pady=(0, 7)
		)
		folder_row = ttk.Frame(content, style="App.TFrame")
		folder_row.grid(row=2, column=0, sticky="ew", pady=(0, 14))
		folder_row.columnconfigure(0, weight=1)
		ttk.Entry(folder_row, textvariable=self.folder, state="readonly", style="Path.TEntry").grid(
			row=0, column=0, sticky="ew", padx=(0, 8)
		)
		ttk.Button(folder_row, text="Browse...", command=self.choose_folder, style="Browse.TButton").grid(
			row=0, column=1, sticky="ns"
		)
		ttk.Label(content, text="FILES IN FOLDER", style="Section.TLabel").grid(
			row=3, column=0, sticky="w", pady=(0, 7)
		)
		ttk.Label(content, textvariable=self.file_count, style="Count.TLabel").grid(
			row=3, column=1, sticky="e", pady=(0, 7)
		)

		columns = ("name", "category")
		self.files = ttk.Treeview(content, columns=columns, show="headings", selectmode="browse")
		self.files.heading("name", text="FILE NAME", anchor="w")
		self.files.heading("category", text="CATEGORY", anchor="w")
		self.files.column("name", width=490, anchor="w")
		self.files.column("category", width=190, anchor="w")
		self.files.grid(row=4, column=0, sticky="nsew")

		scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.files.yview)
		scrollbar.grid(row=4, column=1, sticky="ns")
		self.files.configure(yscrollcommand=scrollbar.set)

		footer = ttk.Frame(content, style="App.TFrame")
		footer.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))
		footer.columnconfigure(0, weight=1)
		ttk.Label(footer, textvariable=self.status, style="Status.TLabel").grid(row=0, column=0, sticky="w")
		ttk.Button(
			footer,
			textvariable=self.pause_button_label,
			command=self.toggle_auto_sort,
			style="Pause.TButton",
		).grid(row=0, column=1, padx=(8, 0), sticky="e")
		ttk.Button(footer, text="Sort existing files", command=self.sort_files, style="Sort.TButton").grid(
			row=0, column=2, padx=(8, 0), sticky="e"
		)

	def toggle_auto_sort(self):
		# Pausing stops file moves, but the folder watcher keeps the preview current.
		enabled = not self.auto_sorting.get()
		self.auto_sorting.set(enabled)
		self.auto_sort_label.set("AUTO SORT  ON" if enabled else "AUTO SORT  PAUSED")
		self.pause_button_label.set("Pause auto-sort" if enabled else "Resume auto-sort")
		self.status.set(
			"Auto-sort resumed; new files will be sorted automatically."
			if enabled
			else "Auto-sort paused. New files stay here; the preview keeps updating."
		)

	def choose_folder(self):
		selected = filedialog.askdirectory(title="Choose a folder to sort")
		if selected:
			self._set_folder(Path(selected))

	def _set_folder(self, folder):
		if self.watch_job is not None:
			self.root.after_cancel(self.watch_job)
			self.watch_job = None
		self.folder.set(str(folder))
		self.watched_folder = folder
		self.pending_files.clear()
		try:
			# Treat files already here as the baseline; only later arrivals auto-sort.
			self.known_files = set(self._list_files(folder))
		except OSError as error:
			messagebox.showerror("Cannot read folder", str(error))
			return
		self.preview_entries = ()
		self.refresh_preview()
		self._watch_folder()

	def _list_files(self, folder):
		return sorted(
			(item for item in folder.iterdir() if item.is_file()),
			key=lambda item: item.name.lower(),
		)

	def refresh_preview(self):
		folder = Path(self.folder.get())
		if not folder.is_dir():
			self.status.set("Choose a folder to preview its files.")
			self.file_count.set("0 FILES")
			return

		try:
			items = self._list_files(folder)
		except OSError as error:
			self.status.set(f"Cannot read folder: {error}")
			return

		entries = tuple((item.name, category_for(item)) for item in items)
		self.file_count.set(f"{len(items)} FILE" if len(items) == 1 else f"{len(items)} FILES")
		if entries != self.preview_entries:
			self.files.delete(*self.files.get_children())
			for entry in entries:
				self.files.insert("", "end", values=entry)
			self.preview_entries = entries
		self.status.set(f"{len(items)} file(s) ready. Subfolders will be left alone.")

	def _watch_folder(self):
		folder = self.watched_folder
		if folder is None or not folder.is_dir():
			self.watch_job = None
			return

		try:
			items = self._list_files(folder)
		except OSError as error:
			self.status.set(f"Watching paused: {error}")
			self.watch_job = self.root.after(1000, self._watch_folder)
			return

		current_files = set(items)
		ready_to_sort = []
		# Wait until a new file's size and timestamp stay unchanged for two checks.
		for item in items:
			if item in self.known_files:
				continue
			try:
				stat = item.stat()
			except OSError:
				continue

			fingerprint = (stat.st_size, stat.st_mtime_ns)
			previous = self.pending_files.get(item)
			if previous is None or previous[0] != fingerprint:
				self.pending_files[item] = (fingerprint, 0)
			else:
				stable_polls = min(previous[1] + 1, 2)
				self.pending_files[item] = (fingerprint, stable_polls)
				if stable_polls == 2 and self.auto_sorting.get():
					ready_to_sort.append(item)

		for item in ready_to_sort:
			try:
				self._sort_one(item, folder)
			except OSError as error:
				self.status.set(f"Could not sort {item.name}: {error}")
			else:
				self.known_files.add(item)
				self.pending_files.pop(item, None)

		self.pending_files = {
			item: state for item, state in self.pending_files.items() if item in current_files
		}
		self.refresh_preview()
		self.status.set(
			"Watching for new files; new files sort automatically."
			if self.auto_sorting.get()
			else "Auto-sort paused. New files stay here; the preview keeps updating."
		)
		self.watch_job = self.root.after(1000, self._watch_folder)

	def _sort_one(self, item, folder):
		destination_folder = folder / category_for(item)
		destination_folder.mkdir(exist_ok=True)
		shutil.move(str(item), str(unique_destination(destination_folder / item.name)))

	def sort_files(self):
		folder = Path(self.folder.get())
		if not folder.is_dir():
			messagebox.showinfo("Choose a folder", "Choose a folder before sorting.")
			return

		try:
			items = [item for item in folder.iterdir() if item.is_file()]
		except OSError as error:
			messagebox.showerror("Cannot read folder", str(error))
			return

		if not items:
			self.status.set("There are no files to sort.")
			return

		if not messagebox.askyesno(
			"Sort files",
			f"Move {len(items)} file(s) into category folders inside:\n{folder}?",
		):
			return

		moved = 0
		failures = []
		for item in items:
			try:
				self._sort_one(item, folder)
				moved += 1
			except OSError as error:
				failures.append(f"{item.name}: {error}")

		self.refresh_preview()
		if failures:
			messagebox.showwarning(
				"Sort finished with errors",
				f"Moved {moved} file(s).\n\n" + "\n".join(failures[:8]),
			)
		else:
			self.status.set(f"Sorted {moved} file(s). New files will continue to sort automatically.")


if __name__ == "__main__":
	window = tk.Tk()
	FileSorterApp(window)
	window.mainloop()
