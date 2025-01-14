import os


def main():
    from controller.controller import process_videos, clenaup
    from view.cli_view import print_message, print_error

    input_file = input_file = os.path.join(os.path.dirname(__file__), "videos.txt")
    subtitles_dir = "sub"
    language = "English"
    exclude_files = ["videos.txt", "requirements.txt"]

    try:
        with open(input_file, "r") as file:
            directories = [
                line.strip().strip('"').strip("'") for line in file if line.strip()
            ]
        process_videos(directories, subtitles_dir, language)
        clenaup(exclude_files)
    except FileNotFoundError:
        print_error(f"Input file '{input_file}' not found.")


if __name__ == "__main__":
    main()
