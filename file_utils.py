import logging
import os
import re

from video_utils import create_video


def find_all_files_recursively(root_dir: str) -> list[str]:
    """Recursively finds all files in all folders."""
    all_files: list[str] = []
    for dirpath, _, filenames in os.walk(root_dir):
        files = [os.path.join(dirpath, f) for f in filenames if f.lower().endswith(".jpg")]
        all_files.extend(files)
    logging.info(f"Recursively found {len(all_files)} files.")
    return all_files


def group_by_sequence(files: list[str]) -> dict[str, list[str]]:
    """Groups files by sequences based on file name."""
    sequence_dict: dict[str, list[str]] = {}

    for file in files:
        file_name = os.path.basename(file)

        match = re.match(r"(.+?)([_\.\s]*\d+)?(\.\w+)$", file_name)

        if not match:
            continue

        # Extract main part of file name
        sequence_name = match.group(1).strip()

        # The key will be full initial part of name before indexing characters
        # For example, for blood_mist_001.jpg it will be blood_mist,
        # and for blood.003.jpg it will be blood
        if sequence_name not in sequence_dict:
            sequence_dict[sequence_name] = []

        sequence_dict[sequence_name].append(file)

    logging.info(f"Sequences formed: {list(sequence_dict.keys())}")

    return sequence_dict


def process_files(files: list[str], output_dir: str) -> None:
    """Groups files by sequences and creates videos."""
    if files:
        sequence_dict: dict[str, list[str]] = group_by_sequence(files)
        create_video(sequence_dict, output_dir)
    else:
        logging.info("No files to process.")
