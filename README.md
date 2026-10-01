# 📁 File Sorter

> A lightweight desktop file organizer built with Python and Tkinter that automatically sorts files into categorized folders.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-2C2C2C?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ✨ Features

- 📂 **Automatic file organization** — New files are sorted automatically.
- 👀 **Live folder monitoring** — Checks for new files every second.
- 🗂️ **File categorization** — Organizes files by extension.
- 🔒 **Duplicate protection** — Prevents existing files from being overwritten.
- ⏸️ **Pause / Resume** — Temporarily disable automatic sorting.
- 🖱️ **Manual sorting** — Sort existing files with one click.
- 📊 **Live preview** — See files and their detected categories.
- ⏳ **Incomplete-file protection** — Waits for files to stop changing before moving them.
- 📁 **Subfolder protection** — Existing subfolders are left untouched.
- 🧩 **No third-party dependencies** — Uses Python's standard library.

---

## 🖥️ Preview

The application provides a simple desktop interface with:

- A folder selector
- Live file list
- File categories
- File counter
- Auto-sort status
- Pause/resume control
- Manual sorting button

---

## 📦 Categories

| Category | File Types |
|---|---|
| 🖼️ Images | `.bmp` `.gif` `.heic` `.jpeg` `.jpg` `.png` `.svg` `.tif` `.tiff` `.webp` |
| 📄 Documents | `.doc` `.docx` `.odt` `.pdf` `.rtf` `.txt` |
| 📊 Spreadsheets | `.csv` `.ods` `.xls` `.xlsx` |
| 📽️ Presentations | `.key` `.odp` `.ppt` `.pptx` |
| 🎵 Audio | `.aac` `.flac` `.m4a` `.mp3` `.ogg` `.wav` `.wma` |
| 🎬 Video | `.avi` `.m4v` `.mkv` `.mov` `.mp4` `.mpeg` `.mpg` `.webm` `.wmv` |
| 📦 Archives | `.7z` `.bz2` `.gz` `.rar` `.tar` `.xz` `.zip` |
| 💻 Code | `.c` `.cpp` `.css` `.html` `.java` `.js` `.json` `.py` `.rb` `.ts` `.xml` `.yaml` `.yml` |
| ⚙️ Applications | `.apk` `.bat` `.deb` `.exe` `.msi` `.pkg` `.sh` |
| 📁 Other | Any unsupported extension |

---

## 🚀 Getting Started

### Requirements

You only need:

- Python 3.x
- Tkinter

No external Python packages are required.

### Check Python

```bash
python --version

