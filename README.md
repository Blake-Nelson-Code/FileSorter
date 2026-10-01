File Sorter

A lightweight desktop file organizer built with Python and Tkinter that automatically sorts files into categorized folders based on their file extensions.

File Sorter can monitor a folder in real time, automatically organize newly added files, safely handle duplicate filenames, and also sort existing files on demand.

Features

Automatic file organization
Newly added files are automatically moved into category folders.

Real-time folder monitoring
The application checks the selected folder every second for new files.

File type categorization
Files are organized into categories such as Images, Documents, Audio, Video, Archives, Code, and more.

Duplicate-safe file moving
Existing files are never overwritten. If a filename already exists, the application creates a numbered copy such as:

report.pdf
report (1).pdf
report (2).pdf


Download-folder support
If a Downloads folder exists in the user's home directory, it is selected automatically when the application starts.

Preview interface
The application displays the files currently present in the watched folder along with their detected categories.

Pause and resume
Automatic sorting can be temporarily paused without stopping folder monitoring.

Manual sorting
Existing files can be sorted manually using the Sort existing files button.

Safe handling of incomplete files
The application waits for a newly detected file to remain unchanged across multiple checks before moving it. This helps avoid moving files while they are still being downloaded or copied.

Unknown file types
Extensions that are not defined in the category list are placed in an Other folder.

Subfolder protection
The application only processes files directly inside the selected folder. Existing subfolders are left untouched.

How It Works

When the application starts, it creates a Tkinter window and initializes the file sorter.

If a Downloads directory exists, the application automatically begins monitoring it.

Otherwise, the user can select a folder using the Browse... button.

Once a folder is selected, File Sorter:

Records the files that already exist.

Displays those files in the interface.

Begins checking the folder once per second.

Detects newly created files.

Checks whether each new file has stopped changing.

Determines the appropriate category from the file extension.

Creates the category folder if necessary.

Moves the file into that folder.

Updates the interface.

Existing files are treated as the initial baseline. This means they are not automatically moved immediately after selecting a folder. They can instead be organized with the Sort existing files button.

File Categories

The application currently supports the following categories:

Category	Extensions
Images	.bmp, .gif, .heic, .jpeg, .jpg, .png, .svg, .tif, .tiff, .webp
Documents	.doc, .docx, .odt, .pdf, .rtf, .txt
Spreadsheets	.csv, .ods, .xls, .xlsx
Presentations	.key, .odp, .ppt, .pptx
Audio	.aac, .flac, .m4a, .mp3, .ogg, .wav, .wma
Video	.avi, .m4v, .mkv, .mov, .mp4, .mpeg, .mpg, .webm, .wmv
Archives	.7z, .bz2, .gz, .rar, .tar, .xz, .zip
Code	.c, .cpp, .css, .html, .java, .js, .json, .py, .rb, .ts, .xml, .yaml, .yml
Applications	.apk, .bat, .deb, .exe, .msi, .pkg, .sh
Other	Any extension not listed above

File extensions are matched case-insensitively, so files such as:

PHOTO.JPG
photo.jpg
Photo.JpG


are all recognized as image files.

Example

Suppose the watched folder initially contains:

Downloads/
├── vacation.jpg
├── resume.pdf
├── budget.xlsx
├── song.mp3
├── project.py
└── movie.mp4


After sorting, the structure becomes:

Downloads/
├── Images/
│   └── vacation.jpg
├── Documents/
│   └── resume.pdf
├── Spreadsheets/
│   └── budget.xlsx
├── Audio/
│   └── song.mp3
├── Code/
│   └── project.py
└── Video/
    └── movie.mp4


The original files are moved rather than copied.

Requirements

You need:

Python 3.x

Tkinter

The application uses the following Python modules:

import shutil
import tkinter
from pathlib import Path


shutil, tkinter, and pathlib are part of the Python standard library, so no third-party Python packages are required.

Checking Python

Run:

python --version


or:

python3 --version


You should have Python 3 installed.

Checking Tkinter

You can test whether Tkinter is available with:

python -m tkinter


If Tkinter is installed correctly, a small test window should appear.

Installation

Clone the repository:

git clone https://github.com/your-username/file-sorter.git


Move into the project directory:

cd file-sorter


No pip install step is required because the application uses Python's standard library.

Running the Application

Run the Python script:

python file_sorter.py


On some systems, you may need:

python3 file_sorter.py


The File Sorter window should open.

If your system has a Downloads directory, it will automatically be selected.

Using the Application
1. Choose a folder

Click:

Browse...


and select the folder you want to monitor.

2. Review the files

The main file list displays:

File name

Detected category

The file counter shows how many files are currently inside the watched folder.

3. Automatic sorting

Automatic sorting is enabled by default.

When a new file appears, the application waits until the file stops changing before moving it.

For example, if you download:

example.pdf


the application waits for the download to finish and then moves it into:

Documents/example.pdf

4. Pause automatic sorting

Click:

Pause auto-sort


The application will continue monitoring and updating the preview, but newly detected files will remain in the watched folder.

Click:

Resume auto-sort


to enable automatic organization again.

5. Sort existing files

Click:

Sort existing files


The application asks for confirmation before moving the files.

This is useful when you select a folder containing files that existed before monitoring began.

File Safety

File Sorter takes several precautions when moving files.

Duplicate filenames

The application never intentionally overwrites an existing destination file.

For example, if:

Documents/report.pdf


already exists and another report.pdf needs to be moved there, it becomes:

Documents/report (1).pdf


If that also exists:

Documents/report (2).pdf


and so on.

Incomplete files

New files may appear before they have finished downloading or copying.

Instead of moving them immediately, the application records their:

File size

Modification timestamp

The file must remain unchanged across multiple monitoring checks before automatic sorting occurs.

This reduces the chance of moving a file while another application is still writing to it.

Existing files

When a folder is first selected, its existing files are recorded as known files.

They are therefore not automatically moved just because the folder was opened.

Use Sort existing files if you want to organize them.

Subfolders

File Sorter does not recursively scan directories.

For example:

Downloads/
├── file.pdf
└── ExistingFolder/
    └── photo.jpg


Only file.pdf is considered.

ExistingFolder and its contents are left untouched.

Project Structure

A minimal project structure can look like this:

file-sorter/
├── file_sorter.py
├── README.md
└── LICENSE


The main application is contained in file_sorter.py.

Code Overview
Category Detection

The CATEGORIES dictionary defines which extensions belong to each folder.

The category_for() function then checks a file's extension:

def category_for(path):
    extension = path.suffix.lower()
    return next(
        (
            name
            for name, extensions in CATEGORIES.items()
            if extension in extensions
        ),
        "Other",
    )


Calling:

category_for(Path("photo.jpg"))


returns:

Images


While:

category_for(Path("unknown.xyz"))


returns:

Other

Duplicate Handling

The unique_destination() function checks whether the intended destination already exists.

If it does, a numbered filename is generated:

file.txt
file (1).txt
file (2).txt
file (3).txt


This prevents an existing file from being overwritten.

Moving Files

The _sort_one() method determines the category folder, creates it if necessary, and moves the file:

destination_folder = folder / category_for(item)
destination_folder.mkdir(exist_ok=True)

shutil.move(
    str(item),
    str(unique_destination(destination_folder / item.name))
)

Folder Monitoring

The application uses Tkinter's after() method rather than creating a separate background thread.

The watcher schedules itself again after approximately one second:

self.watch_job = self.root.after(1000, self._watch_folder)


This keeps the monitoring logic integrated with Tkinter's event loop.

Design Decisions
Why Tkinter?

Tkinter is included with standard Python installations and provides enough functionality for a small desktop utility without requiring a large dependency stack.

Why polling?

The application uses simple periodic polling rather than an external filesystem-watching library.

Advantages include:

No third-party dependencies

Simple implementation

Cross-platform approach

Easy to understand and modify

The tradeoff is that changes are detected approximately once per second rather than through an operating-system filesystem event.

Why wait for file stability?

Moving a file immediately after detecting it can cause problems if another application is still writing to it.

Checking its size and modification timestamp provides a simple way to wait until the file appears stable.

Limitations

The current implementation intentionally keeps things simple.

Monitoring interval

The folder is checked approximately once per second. This means sorting is not instantaneous.

No recursive sorting

Only files directly inside the selected folder are processed.

Extension-based classification

The application determines file categories from filename extensions rather than inspecting file contents.

For example:

document.pdf


is classified as a document because of .pdf.

No undo feature

Once a file is moved, the application does not currently provide an undo button.

No custom categories through the UI

Categories and extensions currently need to be modified in the Python source code.

No persistent settings

The selected folder and application settings are not saved between sessions.

Customizing Categories

You can add or remove extensions by editing the CATEGORIES dictionary.

For example:

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png"},
    "Documents": {".pdf", ".docx", ".txt"},
    "3D": {".blend", ".fbx", ".obj", ".stl"},
}


You could also add a new category:

"Design": {".fig", ".sketch", ".xd"},


The application will automatically create the corresponding folder when it needs to move a file into it.

Error Handling

The application handles common filesystem errors and reports them through the interface.

Examples include:

Inaccessible folders

Files disappearing during processing

Permission errors

Failed moves

Problems reading directory contents

When manually sorting, failed files are collected and displayed after the operation.

The application also avoids crashing the entire interface when an individual file cannot be moved.

Future Improvements

Potential improvements include:

Recursive directory support

Drag-and-drop folder selection

Custom categories through the GUI

User-defined file extensions

Configurable monitoring intervals

Undo/revert functionality

Sorting rules based on filename patterns

Sorting by date

Sorting by file size

Automatic startup

System tray support

Dark mode

Activity/history log

File operation notifications

Configurable destination folders

Windows executable packaging

macOS application packaging

Linux desktop integration

More sophisticated filesystem event monitoring

Contributing

Contributions are welcome.

A typical workflow is:

git checkout -b feature/my-feature


Make your changes, test the application, and commit them:

git add .
git commit -m "Add my feature"


Then push the branch:

git push origin feature/my-feature


Open a pull request describing:

What was changed

Why the change was made

How it was tested

Any limitations or known issues

Testing

Before submitting changes, test at least the following scenarios:

Select a valid folder.

Select an empty folder.

Add a supported file type.

Add an unsupported file type.

Add files with uppercase extensions.

Add multiple files simultaneously.

Add a duplicate filename.

Pause automatic sorting.

Resume automatic sorting.

Manually sort existing files.

Test files that are still being copied.

Test a folder containing existing subdirectories.

Test inaccessible or restricted files where applicable.

License

Add your preferred open-source license to the repository.

For example, if using the MIT License, create a LICENSE file containing the appropriate MIT License text.

Disclaimer

File Sorter moves files rather than copying them. Always test the application on a non-critical folder before using it with important data.

Although the application includes safeguards for duplicate names and incomplete files, filesystem operations can still fail because of permissions, locked files, external applications, or other operating-system conditions.

Summary

File Sorter is a simple, dependency-free desktop utility for keeping folders organized automatically.

It combines:

Python

Tkinter

pathlib

shutil

Real-time polling

Extension-based classification

Duplicate-safe file movement

A graphical preview interface

The result is a lightweight file-management tool that can continuously organize incoming files while giving the user control over when automatic sorting is enabled.
