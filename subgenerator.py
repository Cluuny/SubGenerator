import os
import subprocess
import shutil

input_file = "videos.txt"
language = "English"
subtitles_dir = "sub"


def ensure_directory_exists(directory):
    """Create the directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def clean_old_files(exclude_files):
    """
    Remove the 'sub' folder and all .json, .tsv, .srt, .vtt, and .txt files,
    except those specified in exclude_files.
    """
    try:
        if os.path.exists(subtitles_dir):
            shutil.rmtree(subtitles_dir)

        for file in os.listdir("."):
            if (
                file.endswith((".json", ".tsv", ".srt", ".vtt", ".txt"))
                and file not in exclude_files
            ):
                os.remove(file)

        print("Old files cleaned, except those specified in the exclusion list.")
    except Exception as e:
        print(f"Error cleaning old files: {e}")


def generate_subtitles(video_path):
    """Generate subtitles for a video using Whisper."""
    try:
        print(f"Generating subtitles for: {video_path}")
        subprocess.run(
            ["whisper", video_path, "--language", language, "--output_format", "srt"],
            check=True,
        )

        original_srt_file = os.path.splitext(os.path.basename(video_path))[0] + ".srt"
        srt_file = os.path.join(subtitles_dir, original_srt_file)

        if os.path.exists(original_srt_file):
            ensure_directory_exists(subtitles_dir)
            os.rename(original_srt_file, srt_file)
            return srt_file
        else:
            print(f"Error: .srt file was not generated for {video_path}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error generating subtitles for {video_path}: {e}")
        return None


def embed_subtitles(video_path, srt_file):
    """Embed subtitles into the video using ffmpeg with styling options."""
    try:
        # Construct output path with "-sub" suffix
        video_dir = os.path.dirname(video_path)
        base_name, ext = os.path.splitext(os.path.basename(video_path))
        output_path = os.path.join(video_dir, f"{base_name}-sub{ext}")

        # Ensure paths are properly formatted
        video_path = video_path.replace("\\", "/")
        srt_file = srt_file.replace("\\", "/")
        output_path = output_path.replace("\\", "/")

        print(f"Embedding subtitles into: {output_path}")
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-filter_complex",
                f"subtitles={
                srt_file}:force_style='BackColour=&HA0000000,BorderStyle=4,Fontsize=6'",
                "-c:a",
                "copy",
                output_path,
            ],
            check=True,
        )

        print(f"Subtitled video saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error embedding subtitles: {e}")
    except Exception as e:
        print(f"Unexpected error embedding subtitles: {e}")


def process_videos_in_directory(directory):
    """Process all .mp4 files in the directory that do not have '-sub' in their name."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4") and not file.endswith("-sub.mp4"):
                video_path = os.path.join(root, file)

                # Check if a subtitled version already exists
                base_name, ext = os.path.splitext(file)
                subtitled_file = os.path.join(root, f"{base_name}-sub{ext}")
                if os.path.exists(subtitled_file):
                    print(f"Skipping: {video_path} (subtitled version already exists)")
                    continue

                # Generate subtitles and embed them
                srt_file = "./" + generate_subtitles(video_path)
                if srt_file:
                    embed_subtitles(video_path, srt_file)


def natural_sort_key(path):
    """Extract numeric values from strings for natural sorting."""
    import re

    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", path)]


def main():
    # Lista de archivos que deseas conservar
    exclude_files = ["requirements.txt", "videos.txt"]

    clean_old_files(exclude_files)

    """Main function to process all directories listed in videos.txt."""
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    try:
        with open(input_file, "r") as file:
            # Read and clean directory paths
            directories = [
                line.strip().strip('"').strip("'") for line in file if line.strip()
            ]

        # Sort directories naturally
        directories = sorted(directories, key=natural_sort_key)

        for directory in directories:
            if os.path.exists(directory):
                print(f"Processing directory: {directory}")
                process_videos_in_directory(directory)
            else:
                print(f"Warning: Directory does not exist: {directory}")

    except Exception as e:
        print(f"Error reading {input_file}: {e}")


if __name__ == "__main__":
    main()
