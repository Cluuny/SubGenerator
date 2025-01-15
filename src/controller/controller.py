import os
import sys
from model.cleaner import clean_old_files
from model.embedder import embed_subtitles
from model.generator import generate_subtitles


class SubtitleController:
    def __init__(self, view, subtitles_dir, exclude_files):
        """
        Initialize the SubtitleController.

        :param view: The view instance to interact with the GUI.
        :param subtitles_dir: Directory where the generated subtitles will be stored.
        :param exclude_files: List of files to be excluded from processing.
        :param log_queue: Queue for redirecting log messages to the GUI.
        """
        self.view = view
        self.subtitles_dir = subtitles_dir
        self.exclude_files = exclude_files
        self.is_processing = False

    def _generate_subtitles_thread(self, folder, language):
        """
        Generate subtitles for all MP4 files in the specified folder.

        :param folder: The folder containing video files.
        :param language: Language for subtitle generation.
        """
        try:

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
            processed_files = 0

            for directory in directories:
                for root, _, files in os.walk(directory):
                    for file in files:
                        if file.endswith(".mp4") and not file.endswith("-sub.mp4"):
                            video_path = os.path.join(root, file)
                            base_name, ext = os.path.splitext(file)
                            subtitled_file = os.path.join(root, f"{base_name}-sub{ext}")

                            if os.path.exists(subtitled_file):
                                continue

                            processed_files += 1

                            srt_file = generate_subtitles(
                                video_path, language, self.subtitles_dir
                            )
                            if srt_file:
                                embed_subtitles(video_path, srt_file)

            clean_old_files(self.exclude_files)
            self.is_processing = False
        except Exception as e:
            error_msg = f"An error occurred: {e}"
            if self.view:
                self.view.root.after(0, self.view.show_error, "Error", error_msg)
        finally:
            self.is_processing = False

    def start_subtitle_generation(self, folder, language):
        """
        Start the subtitle generation process in a separate thread.

        :param folder: The folder containing video files.
        :param language: Language for subtitle generation.
        """
        if self.is_processing:
            self.logger.warning("Subtitle generation is already in progress.")
            return

        self.is_processing = True
        self.view.start_thread(self._generate_subtitles_thread, folder, language)
