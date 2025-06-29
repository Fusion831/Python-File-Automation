import pathlib
import shutil
import argparse
import json
import logging 



def load_rules(config_path: str) -> dict:
    """Load file organization rules from a JSON file.
    Args:        
        file_path (str): The path to the JSON file containing rules.
    Returns:
        dict: A dictionary containing the file organization rules.
        """
    try:
        with open(config_path, 'r') as file:
            rules = json.load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file {config_path} not found. Using default rules.")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from {config_path}. Using default rules.")
        return {}
    #Inverting the rules to a mapping of extensions to folder names
    inverted_rules = {}
    for folder_name, extensions in rules.items():
        for ext in extensions:
            inverted_rules[ext.lower()] = folder_name
    return inverted_rules


def get_file_folder(item,rules: dict ):
    """Determine the folder name based on the file extension.
    Args:
        item (pathlib.Path): The file path to check.
    Returns:
        str: The folder name where the file should be moved.
    """
    return rules.get(item.suffix.lower())
    
def organize_files(path,rules: dict, arg_dry_run=False):
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
            folder_name= get_file_folder(item,rules)
            if folder_name:
                folder_path = path / folder_name
                folder_path.mkdir(exist_ok=True)
                try:
                    if arg_dry_run:
                        logging.info(f"Dry run: {item.name} would be moved to {folder_name} folder.")
                    else:
                        shutil.move(str(item), str(folder_path))
                        logging.info(f"Moved {item.name} to {folder_name} folder.")
                except Exception as e:
                    logging.error(f"Error moving {item.name}: {e}")
        else:
            logging.info(f"Skipping non-file: {item.name}")

def setup_parser():
    """Set up the command line argument parser."""
    parser= argparse.ArgumentParser(description="Organize files in a directory into subfolders based on file type.")
    parser.add_argument("source", help="The directory path to organize.")
    parser.add_argument("-d","--dry-run",action="store_true",
                        help="Perform a dry run without moving files.")
    parser.add_argument("-c", "--config", default="config.json",
                        help="Path to the JSON configuration file (default: config.json).")
    return parser


def main():
    """Main function to run the file organization script."""
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s [%(levelname)s] - %(message)s", 
        handlers=[
            logging.FileHandler("organizer.log"), 
            logging.StreamHandler() 
        ]
    )
    logging.info("--- Starting File Organizer Script ---")
    
    
    args = setup_parser().parse_args()
    rules = load_rules(args.config) 
    if not rules:
        print("Halting due to configuration errors.")
        return
    path= pathlib.Path(args.source)
    try:
        source_path = pathlib.Path(args.source)
        if not source_path.exists():
            raise FileNotFoundError(f"The source directory '{source_path}' does not exist.")
        
        organize_files(source_path, rules, args.dry_run)
        logging.info("--- File organization complete. ---")
    except (FileNotFoundError, NotADirectoryError) as e:
        logging.critical(f"A critical error occurred: {e}")
    except Exception:
        logging.critical("An unexpected error occurred.", exc_info=True)
        
        

if __name__ == "__main__":
    main()