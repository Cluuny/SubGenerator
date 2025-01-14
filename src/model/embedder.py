def embed_subtitles(video_path, srt_file):
    import os, subprocess

    try:
        video_dir = os.path.dirname(video_path)
        base_name, ext = os.path.splitext(os.path.basename(video_path))
        output_path = os.path.join(video_dir, f"{base_name}-sub{ext}")

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
                f"subtitles={srt_file}:force_style='BackColour=&HA0000000,BorderStyle=4,Fontsize=6'",
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
