import logging
import os
import shutil
import tempfile
import traceback
from model.cleaner import clean_old_files
from model.embedder import embed_subtitles
from model.generator import generate_subtitles


class SubtitleController:
    """
    Controller class in the MVC pattern to manage the subtitle generation process.
    It interacts with the view and manages backend operations for subtitle creation.
    """

    def __init__(self, view, exclude_files):
        """
        Initialize the SubtitleController.

        :param view: The view instance to interact with the GUI.
        :param exclude_files: List of files to be excluded from processing.
        """
        self.view = view
        self.exclude_files = exclude_files
        self.is_processing = False

    def _generate_subtitles_thread(self, folder, language):
        """
        Generate subtitles for all MP4 files in the specified folder.

        :param folder: The folder containing video files.
        :param language: Language for subtitle generation.
        """
        temp_dir = None
        try:
            logging.info(
                f"Starting subtitle generation in folder: {folder}, Language: {language}"
            )

            # Count total files to process
            directories = [folder]
            total_files = sum(
                1
                for directory in directories
                for _, _, files in os.walk(directory)
                if any(
                    file.endswith(".mp4") and not file.endswith("-sub.mp4")
                    for file in files
                )
            )
            logging.info(f"Total MP4 files found for processing: {total_files}")

            processed_files = 0

            for directory in directories:
                for root, _, files in os.walk(directory):
                    for file in files:
                        if file.endswith(".mp4") and not file.endswith("-sub.mp4"):
                            video_path = os.path.join(root, file)
                            base_name, ext = os.path.splitext(file)
                            subtitled_file = os.path.join(root, f"{base_name}-sub{ext}")

                            if os.path.exists(subtitled_file):
                                logging.info(f"Skipping already processed file: {file}")
                                continue

                            processed_files += 1
                            logging.info(
                                f"Processing file {processed_files}/{total_files}: {file}"
                            )

                            # Create a temporary directory
                            temp_dir = tempfile.mkdtemp()
                            temp_video_path = os.path.join(
                                temp_dir, os.path.basename(video_path)
                            )
                            shutil.copy2(video_path, temp_video_path)
                            logging.info(f"Temporary file created: {temp_video_path}")

                            # Generate subtitles
                            str_file = generate_subtitles(temp_video_path, language)
                            if str_file:
                                logging.info(f"Generated subtitles: {str_file}")
                                logging.info(f"Embedding subtitles into: {video_path}")
                                embed_subtitles(video_path, temp_video_path, str_file)

            logging.info("Subtitle generation completed successfully.")

        except Exception as e:
            error_msg = f"An error occurred: {e}"
            tb_details = "".join(
                traceback.format_exception(type(e), e, e.__traceback__)
            )
            logging.error(f"{error_msg}\n{tb_details}")

            if self.view:
                self.view.root.after(0, self.view.show_error, "Error", tb_details)
        finally:
            # Clean up temporary files and reset processing flag
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logging.info(f"Cleaned up temporary directory: {temp_dir}")
            self.is_processing = False
            logging.info("Process Completed!")

    def start_subtitle_generation(self, folder, language):
        """
        Start the subtitle generation process in a separate thread.

        :param folder: The folder containing video files.
        :param language: Language for subtitle generation.
        """
        if self.is_processing:
            logging.warning("Subtitle generation is already in progress.")
            return

        logging.info(
            f"Starting subtitle generation for folder: {folder} with language: {language}"
        )
        self.is_processing = True
        self.view.start_thread(self._generate_subtitles_thread, folder, language)
