import os
import subprocess
import logging  # Importar logging


def generate_subtitles(video_path, language, subtitles_dir):
    try:
        logging.info(f"Generating subtitles for: {video_path}")
        subprocess.run(
            ["whisper", video_path, "--language", language, "--output_format", "srt"],
            check=True,
        )

        original_srt_file = os.path.splitext(os.path.basename(video_path))[0] + ".srt"
        srt_file = os.path.join(subtitles_dir, original_srt_file)

        if os.path.exists(original_srt_file):
            if not os.path.exists(subtitles_dir):
                os.makedirs(subtitles_dir)
            os.rename(original_srt_file, srt_file)
            return srt_file
        else:
            logging.error(f"Error: .srt file was not generated for {video_path}")
            return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Error generating subtitles for {video_path}: {e}")
        return None
