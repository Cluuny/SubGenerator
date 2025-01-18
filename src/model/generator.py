import os
import logging
import subprocess


def format_timestamp(timestamp):
    """
    Converts a timestamp from seconds to ASS format (H:MM:SS.sss).

    Args:
        timestamp (float): Time in seconds.

    Returns:
        str: Time in ASS format.
    """
    hours = int(timestamp // 3600)
    minutes = int((timestamp % 3600) // 60)
    seconds = int(timestamp % 60)
    milliseconds = int((timestamp % 1) * 1000)
    return f"{hours}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def generate_subtitles(video_path, language):
    """
    Generates a .srt file for the given video using Whisper CLI.

    Args:
        video_path (str): Path to the video file.
        language (str): Language code (e.g., 'en' for English, 'es' for Spanish).

    Returns:
        str: Path to the generated .srt file.

    Raises:
        FileNotFoundError: If the video file does not exist.
        RuntimeError: If the Whisper CLI command fails.
    """
    try:
        # Ensure the video file exists
        video_path = os.path.abspath(video_path)
        if not os.path.exists(video_path):
            logging.error(f"The file at {video_path} does not exist.")
            raise FileNotFoundError(f"The file at {video_path} does not exist.")

        logging.info(
            f"Starting subtitle generation for video: {video_path} with language: {language}"
        )

        # Output file path for subtitles
        srt_path = os.path.splitext(video_path)[0] + ".srt"

        # Command to run Whisper CLI
        command = [
            "whisper",  # Whisper CLI command
            video_path,
            "--language",
            language,
            "--output_format",
            "srt",
            "--output_dir",
            os.path.dirname(video_path),
        ]

        logging.info(f"Executing command: {' '.join(command)}")

        # Run the command and show output in real-time
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        for line in process.stdout:
            print(line, end="")  # Print stdout in real-time

        for line in process.stderr:
            print(line, end="")  # Print stderr in real-time (optional)

        # Wait for the process to complete
        process.wait()

        # Check for errors in execution
        if process.returncode != 0:
            logging.error("Whisper CLI command failed.")
            raise RuntimeError(
                f"Whisper CLI failed with return code {process.returncode}."
            )

        # Verify if the .srt file was created
        if not os.path.exists(srt_path):
            logging.error("Subtitle file not found after Whisper CLI execution.")
            raise FileNotFoundError("The Whisper CLI did not produce a subtitle file.")

        logging.info(f".srt file generated successfully at: {srt_path}")
        return srt_path

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        raise

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        raise

    finally:
        logging.info("Subtitle generation process completed.")
