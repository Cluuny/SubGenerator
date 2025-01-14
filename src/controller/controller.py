import os
from model.cleaner import clean_old_files
from model.generator import generate_subtitles
from model.embedder import embed_subtitles


def clenaup(exclude_files):
    clean_old_files(exclude_files)


def process_videos(directories, subtitles_dir, language):
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".mp4") and not file.endswith("-sub.mp4"):
                    video_path = os.path.join(root, file)
                    base_name, ext = os.path.splitext(file)
                    subtitled_file = os.path.join(root, f"{base_name}-sub{ext}")
                    if os.path.exists(subtitled_file):
                        continue
                    srt_file = generate_subtitles(video_path, language, subtitles_dir)
                    if srt_file:
                        embed_subtitles(video_path, srt_file)
