# Python File Automation

> A powerful, command-line file organization script built with Python.

## Introduction

In a world of digital clutter, maintaining an organized file system is crucial for productivity. This project was built to solve that exact problem. It serves as a practical demonstration of Python's capabilities for file system automation and provides a robust foundation for more complex scripting projects.

This script is more than just a file sorter; it's a showcase of core software engineering principles, including:

* **System Interaction:** Mastering the ability to read, create, and modify files and directories.
* **Configuration Management:** Separating the script's logic from its rules, allowing for easy customization without touching the source code.
* **Robust Tooling:** Building a reliable command-line interface (CLI) with user-friendly features like safety checks and detailed logging.

This project defines a developer's proficiency with Python's standard library and their ability to create practical, real-world solutions.

## Key Features

* **Dynamic Sorting:** Automatically organizes files into subfolders based on their file extension.
* **Fully Customizable Rules:** Uses an external `config.json` file to define which extensions go into which folders. Modify the rules without ever editing the Python code!
* **Command-Line Interface:** A professional CLI built with `argparse` allows for easy integration into workflows and other scripts.
* **Safety First (Dry Run Mode):** A `--dry-run` flag lets you preview all the changes the script *would* make without actually moving a single file. This ensures you can verify the logic before committing to any changes.
* **Robust Logging:** The script generates a detailed `organizer.log` file, creating a timestamped audit trail of every action taken, every file moved, and every error encountered.

## Tech Stack

* **Language:** Python 3
* **Standard Libraries:**
  * `pathlib`: For modern, object-oriented file system path manipulation.
  * `shutil`: For high-level file operations (moving files).
  * `argparse`: For creating a powerful command-line interface.
  * `json`: For parsing the external configuration file.
  * `logging`: For professional, configurable logging to the console and a file.

## The Choice for `pathlib` over `os`

This project exclusively uses the `pathlib` module for path manipulation instead of the older `os` module. This was a deliberate design choice for several key reasons:

1. **Object-Oriented Approach:** `pathlib` treats file system paths as objects with methods and properties, not as simple strings. This leads to more readable and less error-prone code.
2. **Readability and Conciseness:** Operations are more intuitive.
    * **Joining paths:** `path / "subfolder"` is cleaner than `os.path.join(path, "subfolder")`.
    * **Getting parts:** `path.name`, `path.suffix`, and `path.stem` are clearer than `os.path.basename()` and `os.path.splitext()`.
3. **Cross-Platform Consistency:** `pathlib` automatically handles differences between Windows (`\`) and Unix-based (`/`) path separators, making the script more portable.
4. **Consolidated Functionality:** The `Path` object has methods like `.exists()`, `.is_dir()`, and `.mkdir()` built-in, reducing the need to import and use multiple `os.path` functions.

In essence, `pathlib` is the modern, Pythonic way to handle file system paths, resulting in a cleaner, more robust, and more maintainable codebase.

## Getting Started

### Prerequisites

* Python 3.6 or newer.

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Fusion831/Python-File-Automation.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Python-File-Automation
    ```

3. It is highly recommended to create a virtual environment to keep dependencies isolated:

    ```bash
    # For Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

    No external packages are needed as this project only uses Python's standard library.

## Usage

The script is run from the command line and accepts several arguments to control its behavior.

### Basic Usage

To organize a directory, provide the path to it as the main argument.

```bash
python organize.py /path/to/your/test_directory
```

### Dry Run (Preview Changes)

To see what the script *would* do without moving any files, use the `-d` or `--dry-run` flag. **This is highly recommended for the first run on any new directory.**

```bash
python organize.py /path/to/your/test_directory --dry-run
```

### Using a Custom Configuration File

To use a set of rules from a different file, specify the path with the `-c` or `--config` flag.

```bash
python organize.py /path/to/your/test_directory --config my_custom_rules.json
```

## Configuration

You can easily customize the sorting logic by editing the `config.json` file. The structure is a simple JSON object where:

* Each **key** is the name of the folder you want files to be moved into (e.g., `"Images"`).
* Each **value** is a list of file extensions (as strings) that should be moved into that folder (e.g., `[".jpg", ".png"]`).

**Example `config.json`:**

```json
{
  "Images": [".jpg", ".jpeg", ".png"],
  "Documents": [".pdf", ".docx", ".pptx"],
  "Archives": [".zip"],
  "TextFiles": [".txt"]
}
```

## Demonstration

This repository includes a `test_directory` to demonstrate the script's functionality.

### Before Running the Script

The initial state of the `test_directory` is a mix of various file types and a pre-existing subfolder.

```bash
test_directory/
├── old_project_files/
│   └── archive.txt
├── family_photo.jpg
├── important_notes.txt
├── monthly_report.docx
├── photo1.jpg
├── presentation.pptx
├── project_files.zip
├── README
├── summer_vacation.jpg
└── user_manual.pdf
```

### After Running the Script

After executing the command `python organize.py test_directory`, the script will create new folders and move the corresponding files into them. Files with unmapped extensions (like the extension-less `README`) and existing folders are left untouched. Note that `project_files.zip` is sorted because it's in our example `config.json`.

```bash
test_directory/
├── Archives/
│   └── project_files.zip
│
├── Documents/
│   ├── monthly_report.docx
│   ├── presentation.pptx
│   └── user_manual.pdf
│
├── Images/
│   ├── family_photo.jpg
│   ├── photo1.jpg
│   └── summer_vacation.jpg
│
├── TextFiles/
│   └── important_notes.txt
│
├── old_project_files/
│   └── archive.txt
│
└── README
