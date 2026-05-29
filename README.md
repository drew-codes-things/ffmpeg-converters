# ffmpeg-converters

A collection of Python scripts that wrap `ffmpeg.exe` for easy audio, image, and video conversion without needing to remember complex command-line flags.

## Features

- Convert between common formats (MP4, MKV, MP3, WAV, PNG, JPG, etc.)
- Batch processing support
- Simple Python interface — no need to write raw FFmpeg commands
- Presets for common tasks (compress, resize, extract audio, etc.)

## Installation

```bash
git clone https://github.com/drew-codes-things/ffmpeg-converters.git
cd ffmpeg-converters
pip install -r requirements.txt
```

Make sure `ffmpeg.exe` is in your PATH or place it in the project folder.

## Usage

```bash
python convert_video.py input.mp4 output.mkv
# or use the interactive mode
python main.py
```

## Requirements

- Python 3.8+
- FFmpeg (download from https://ffmpeg.org)

## License

MIT License