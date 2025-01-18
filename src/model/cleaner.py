import os
import logging  # Import logging for detailed process tracking


def ensure_directory_exists(directory):
    """
    Create the directory if it does not exist.

    Args:
        directory (str): The path of the directory to check or create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directory created: {directory}")


def clean_old_files(folder):
    """
    Deletes all .ass files in the directory of the given video.

    Args:
        folder (str): Path to a folder containing files.

    Returns:
        int: The number of .ass files deleted.

    Raises:
        FileNotFoundError: If the folder does not exist.
    """
    try:
        # Get the absolute path of the provided folder
        video_dir = os.path.abspath(folder)

        if not os.path.exists(video_dir):
            logging.error(f"Directory not found: {video_dir}")
            raise FileNotFoundError(f"The directory {video_dir} does not exist.")

        # Find and delete all .ass files in the directory
        ass_files = [f for f in os.listdir(video_dir) if f.endswith(".ass")]
        for ass_file in ass_files:
            os.remove(os.path.join(video_dir, ass_file))
            logging.info(f"Deleted file: {ass_file}")

        logging.info(f"Deleted {len(ass_files)} .ass file(s) from {video_dir}.")
        return len(ass_files)

    except FileNotFoundError as e:
        logging.exception("Directory not found error.")
        raise e

    except Exception as e:
        logging.exception("An unexpected error occurred while deleting .ass files.")
        raise e
