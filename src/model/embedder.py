import os
import subprocess
import logging  # Importar logging


def embed_subtitles(video_path, srt_file):
    try:
        video_dir = os.path.dirname(video_path)
        base_name, ext = os.path.splitext(os.path.basename(video_path))
        output_path = os.path.join(video_dir, f"{base_name}-sub{ext}")

        video_path = video_path.replace("\\", "/")
        srt_file = srt_file.replace("\\", "/")
        output_path = output_path.replace("\\", "/")

        logging.info(f"Embedding subtitles into: {output_path}")
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-filter_complex",
                f"subtitles={srt_file}:force_style='BackColour=&HA0000000,BorderStyle=4,Fontsize=6'",
                "-c:a",
                "copy",
                output_path,
            ],
            check=True,
        )

        logging.info(f"Subtitled video saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error embedding subtitles: {e}")
    except Exception as e:
        logging.error(f"Unexpected error embedding subtitles: {e}")
