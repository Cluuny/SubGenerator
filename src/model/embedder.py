import subprocess
import os
import logging


def embed_subtitles(video_path, temp_video_path, srt_file):
    """
    Embeds .srt subtitles into a video using FFmpeg with custom styles.

    Args:
        video_path (str): Path to the video file.
        temp_video_path (str): Path to the temporary video file.
        srt_file (str): Path to the .srt subtitle file.

    Returns:
        str: Path to the subtitled video.
    """
    try:
        # Normalize input paths
        video_path = os.path.abspath(video_path).replace("\\", "/")
        temp_video_path = os.path.abspath(temp_video_path).replace("\\", "/")
        srt_file = os.path.abspath(srt_file).replace("\\", "/")

        # Ensure files exist
        if not os.path.exists(video_path):
            logging.error(f"The video file at {video_path} does not exist.")
            raise FileNotFoundError(f"The video file at {video_path} does not exist.")
        if not os.path.exists(temp_video_path):
            logging.error(
                f"The temporary video file at {temp_video_path} does not exist."
            )
            raise FileNotFoundError(
                f"The video file at {temp_video_path} does not exist."
            )
        if not os.path.exists(srt_file):
            logging.error(f"The subtitle file at {srt_file} does not exist.")
            raise FileNotFoundError(f"The subtitle file at {srt_file} does not exist.")

        # Output file path for subtitled video
        output_path = os.path.splitext(video_path)[0] + "-sub.mp4"

        logging.info(f"Starting subtitle embedding for video: {video_path}")
        logging.info(f"Temporary video path: {temp_video_path}")
        logging.info(f"Subtitle file path: {srt_file}")
        logging.info(f"Output file path: {output_path}")

        # FFmpeg command with custom style
        force_style = "BackColour=&HA0000000,BorderStyle=4,Fontsize=6"
        command = [
            "ffmpeg",
            "-i",
            temp_video_path,
            "-vf",
            f"subtitles={srt_file.replace(':', '\\\\:')}:force_style='{force_style}'",
            "-c:a",
            "copy",
            output_path,
        ]

        logging.info(f"Executing FFmpeg command: {' '.join(command)}")
        subprocess.run(command, shell=True, check=True)
        logging.info(f"Subtitled video saved at: {output_path}")

        return output_path

    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg command failed with error: {e}")
        raise RuntimeError(f"An error occurred while embedding subtitles: {e}")

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        raise

    finally:
        logging.info("Subtitle embedding process completed.")
