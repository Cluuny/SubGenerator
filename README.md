# Subtitle Generator and Embedder

This script automates the process of generating subtitles for videos using Whisper, embedding them into the videos with ffmpeg, and organizing the output. It processes multiple directories of videos and applies consistent subtitle styling.

## Features

- **Subtitle Generation**: Automatically creates subtitles for `.mp4` videos using Whisper.
- **Subtitle Embedding**: Embeds generated `.srt` subtitles into videos with ffmpeg, applying custom styling options.
- **Directory Processing**: Processes all `.mp4` videos listed in directories specified in `videos.txt`.
- **File Cleanup**: Removes unnecessary old files (e.g., `.json`, `.tsv`, `.srt`) except those specified in the exclusion list.

## Requirements

- Python 3.x

## Installation

1. Clone the repository or download the script.
2. Install the required tools:

     ```bash
     pip install -r requiremets.txt
     ```

3. Ensure the script is executable:

   ```bash
   chmod +x script.py
   ```

## Usage

1. Create a `videos.txt` file in the same directory as the script. List the directories containing videos to process, one per line.

   Example `videos.txt`:

   ```bash
   /path/to/directory1
   /path/to/directory2
   ```

2. Run the script:

   ```bash
   python subgenerator.py
   ```

3. The script will:
   - Clean old subtitle files (unless excluded).
   - Generate subtitles for all `.mp4` videos without `-sub` in their name.
   - Embed the subtitles into the videos.

## Configuration

### Exclusion List

You can modify the `exclude_files` list in the script to specify files that should not be deleted during cleanup. By default, it includes:

- `requirements.txt`
- `videos.txt`

### Subtitle Styling

The subtitles are styled using the following ffmpeg filter:

```bash
BackColour=&HA0000000, BorderStyle=4, Fontsize=6
```

You can adjust these styles in the `embed_subtitles` function.

## Script Workflow

1. **Clean Old Files**: Deletes the `sub` folder and any subtitle-related files that are not excluded.
2. **Process Videos**: Iterates through each directory listed in `videos.txt`.
   - Checks if the video has already been processed (e.g., `-sub` version exists).
   - Generates subtitles using Whisper.
   - Embeds the subtitles into the video with ffmpeg.
3. **Save Outputs**: Saves subtitled videos with a `-sub` suffix in the same directory as the original video.

## Error Handling

The script includes error handling for:

- Missing `videos.txt` or directories.
- Issues during subtitle generation or embedding.
- Unexpected file or directory errors.

## License

This script is open-source. You can modify and distribute it as needed, also you can made a PR for adding features :).
