# MP4 Subtitle Generator

MP4 Subtitle Generator is a tool that allows you to automatically generate and add subtitles to MP4 files. This project includes a graphical user interface (GUI) for ease of use.

## System Requirements

- **Python**: Version 3.12
- **Whisper**: Must be installed and configured to run from the `whisper` command.
- **FFmpeg**: Must be installed and added to the PATH to run from the command `ffmpeg`.

### Installing Dependencies

1. Make sure you have [Python 3.12](https://www.python.org/downloads/) installed on your system.
2. Install customtkinter by running the following command:

   ````bash
   pip install customtkinter
   ````

3. Install Whisper following the official instructions: [OpenAI Whisper](https://github.com/openai/whisper).
4. Download and install FFmpeg from [FFmpeg.org](https://ffmpeg.org/download.html) and make sure it is set in your PATH variable.

## Usage

### Graphical User Interface (GUI)

To use the GUI, simply run the program by his .exe

1. Select the folder containing the MP4 files.
2. Choose the subtitle language (e.g. English, Spanish, etc.).
3. Click the `Start` button to start processing.

## Features

- Automatic subtitle generation using Whisper technology.
- Subtitle embedding in MP4 videos using FFmpeg.
- Support for multiple languages.

## Project Structure

- **main.py**: Main entry point for CLI and GUI.
- **controller.py**: Main controller for subtitle generation and embedding.
- **cleaner.py**: Cleaning of temporary and old files.
- **embedder.py**: Embedding subtitles in MP4 videos.
- **generator.py**: Generation of subtitle files using Whisper.
- **view/cli_view.py**: Command line interface.
- **view/gui_view.py**: Graphical interface built with CustomTkinter.

## Additional Notes

- Make sure the file paths are correct in `videos.txt`.
- If you encounter errors during execution, check the logs generated in the interface or in the console.

## Contributions

If you wish to contribute to this project, please make a fork of the repository and send a pull request with your improvements.

## License

This project is licensed under the MIT license. See the `LICENSE` file for details.

---

Thanks for using MP4 Subtitle Generator!
