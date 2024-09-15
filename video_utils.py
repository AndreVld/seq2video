import logging
import os
import subprocess


def create_video(sequence_dict: dict[str, list[str]], output_dir: str) -> None:
    """Creates a video from each sequence using ffmpeg and a temporary file."""
    for sequence_name, files in sequence_dict.items():
        files.sort()  # Sort files by frame number

        temp_list_file = f"{sequence_name}_temp_list_file.txt"

        # Write the list of files to text file
        with open(temp_list_file, "w") as f:
            for file in files:
                # each line starts with "file" which is part of the syntax for ffmpeg,
                # indicating that the following is path to file.
                f.write(f"file '{file}'\n")

        # Construct ffmpeg command
        output_file = os.path.join(output_dir, f"{sequence_name}.mov")
        command = [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",  # "-safe 0" allows use of absolute paths
            "-i",
            temp_list_file,
            "-c:v",
            "mjpeg",
            "-framerate",
            "24",
            output_file,
        ]

        # log number of files found for this sequence
        logging.info(f'Found {len(files)} files for "{sequence_name}".')

        # convert command to string for logging
        command_str = " ".join(f'"{arg}"' for arg in command)

        # Run ffmpeg
        try:
            logging.info(f"Running command: {command_str}")
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            if result.returncode != 0:
                logging.error(f"Error executing ffmpeg for sequence {sequence_name}: {result.stderr}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing ffmpeg command: {e.stderr}")

        # Remove the temporary list file
        os.remove(temp_list_file)

    logging.info(f"All video files have been created in directory: {output_dir}.")
