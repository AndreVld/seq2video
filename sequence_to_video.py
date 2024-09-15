import argparse
import logging
import os

from file_utils import find_all_files_recursively, process_files
from gui_utils import choose_directory
from logging_config import configure_logging


def main() -> None:
    configure_logging()

    parser = argparse.ArgumentParser(description="Process image sequences and create videos.")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="""Path to the directory containing image sequences.
        If not provided, folder selection dialog will be opened.""",
    )

    args = parser.parse_args()

    if args.path:
        dir = args.path
    else:
        # Open folder selection dialog if no directory path is provided
        dir = choose_directory()
        if not dir:
            return

    # Check if directory exists
    if not os.path.isdir(dir):
        print(f"Provided directory does not exist: {dir}")
        return

    logging.info(f"Selected directory: {dir}")

    # Recursively find all files
    all_files: list[str] = find_all_files_recursively(dir)

    # Create output directory in selected directory
    output_dir = os.path.join(dir, "output_videos")
    os.makedirs(output_dir, exist_ok=True)

    # Process files and create videos
    process_files(all_files, output_dir)


if __name__ == "__main__":
    main()
