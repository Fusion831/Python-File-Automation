import pathlib
import shutil
import argparse

def get_file_folder(item):
    """Determine the folder name based on the file extension.
    Args:
        item (pathlib.Path): The file path to check.
    Returns:
        str: The folder name where the file should be moved.
    """
    mapping = {
        ".jpg": "Images",
        ".jpeg": "Images",
        ".png": "Images",
        ".pdf": "Documents",
        ".docx": "Documents",
        ".txt": "TextFiles"
    }
    extension = item.suffix.lower()
    return mapping.get(extension)
    
def organize_files(path,arg_dry_run=False):
    """Organize files in the specified directory into subfolders based on file type.
    Args:
        path (pathlib.Path): The directory path to organize.
        arg_dry_run (bool): If True, perform a dry run without moving files.
        Raises:
            FileNotFoundError: If the specified path does not exist.
            NotADirectoryError: If the specified path is not a directory.
            """
    if not path.exists():
        raise FileNotFoundError(f"The path {path} does not exist.")
    if not path.is_dir():
        raise NotADirectoryError(f"The path {path} is not a directory.")
    
    for item in path.iterdir():
        if item.is_file():
            folder_name= get_file_folder(item)
            if folder_name:
                folder_path = path / folder_name
                folder_path.mkdir(exist_ok=True)
                try:
                    if arg_dry_run:
                        print(f"Dry run: {item.name} would be moved to {folder_name} folder.")
                    else:
                        shutil.move(str(item), str(folder_path / item.name))
                        print(f"Moved {item.name} to {folder_name} folder.")
                except Exception as e:
                    print(f"Error moving {item.name}: {e}")
        else:
            print(f"{item.name} is not a file, skipping.")

def setup_parser():
    """Set up the command line argument parser."""
    parser= argparse.ArgumentParser(description="Organize files in a directory into subfolders based on file type.")
    parser.add_argument("source", help="The directory path to organize.")
    parser.add_argument("-dy","--dry-run",action="store_true",
                        help="Perform a dry run without moving files.")
    return parser


def main():
    """Main function to run the file organization script."""
    args = setup_parser().parse_args()
    path= pathlib.Path(args.source)
    try:
        organize_files(path,args.dry_run)
        print("File organization complete.")
    except (FileNotFoundError, NotADirectoryError) as e:
        print(e)