# MP4 Subtitle Generator

MP4 Subtitle Generator is a Python tool that automates the generation and embedding of subtitles into MP4 videos. It uses OpenAI's Whisper model for speech‑to‑text and ffmpeg to embed the resulting subtitles. The project includes both a command‑line interface (CLI) and a graphical user interface (GUI) built with CustomTkinter.

## Features

- Automatic transcription of video audio using Whisper.
- Generation of .srt subtitle files.
- Embedding subtitles into MP4 videos using ffmpeg.
- Batch processing of multiple videos and languages.
- Support for CLI and user‑friendly GUI.
- Temporary file cleanup and organized output directories.

## Prerequisites

- **Python 3.12+** installed on your system.
- **Whisper** installed and accessible via the whisper command. See the [OpenAI Whisper installation guide](https://github.com/openai/whisper).
- **FFmpeg** installed and added to your PATH. [Download ffmpeg](https://ffmpeg.org/download.html).
- **customtkinter** library for the GUI.

## Installation

- Clone this repository.
- Install Python dependencies:

pip install customtkinter

- Follow the Whisper installation instructions and install ffmpeg.

## Usage

### Graphical User Interface (GUI)

- Run the compiled executable (MP4SubtitleGenerator.exe) or execute the Python script:

python main.py

- Select the folder containing your MP4 files.
- Choose the subtitle language (e.g., en, es).
- Click **Start** to generate and embed subtitles. Progress and logs will be displayed in the GUI.

### Command‑Line Interface (CLI)

You can also run the generator from the CLI:

python main.py --input /path/to/videos --lang en --output /path/to/output

- \--input - directory with MP4 files
- \--lang - language code (supported by Whisper)
- \--output - directory where subtitled videos and .srt files will be saved

#### Example

Given a directory with travel.mp4 and interview.mp4, running:

python main.py --input ./videos --lang es --output ./subtitled

will produce travel_subtitled.mp4, travel.srt, interview_subtitled.mp4 and interview.srt inside the ./subtitled directory.

## Project Structure

- main.py - entry point that routes to CLI or GUI.
- controller.py - orchestrates the generation and embedding processes.
- generator.py - wraps Whisper calls for transcription.
- embedder.py - handles ffmpeg commands to embed subtitles.
- cleaner.py - removes temporary files.
- view/cli_view.py - CLI interface.
- view/gui_view.py - GUI built with CustomTkinter.

## Troubleshooting

- Ensure whisper and ffmpeg commands are available in your PATH.
- Verify your audio/video has clear speech; noisy audio may reduce transcription accuracy.
- Check the generated videos.txt file paths; incorrect paths will cause processing errors.
- Consult the logs (displayed in the GUI or console) for more details.

## Contributing

Pull requests are welcome! If you have feature suggestions or bug reports, please open an issue or submit a PR. For major changes, please discuss them in an issue first.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech‑to‑text engine.
- [FFmpeg](https://ffmpeg.org/) for media processing.
