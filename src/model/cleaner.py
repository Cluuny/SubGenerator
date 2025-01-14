import os
import shutil


def ensure_directory_exists(directory):
    """Create the directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def clean_old_files(exclude_files):
    """
    Remove the 'sub' folder and all .json, .tsv, .srt, .vtt, and .txt files,
    except those specified in exclude_files.
    """
    # Calculate the root directory of the project
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    try:
        # Define the folder to clean
        subtitles_dir = os.path.join(root_dir, "sub")

        if os.path.exists(subtitles_dir):
            shutil.rmtree(subtitles_dir)

        # Clean specific file types in the root directory
        for file in os.listdir(root_dir):
            if (
                file.endswith((".json", ".tsv", ".srt", ".vtt", ".txt"))
                and file not in exclude_files
            ):
                os.remove(os.path.join(root_dir, file))

        print(
            "Old files cleaned from project root, except those specified in the exclusion list."
        )
    except Exception as e:
        print(f"Error cleaning old files: {e}")
