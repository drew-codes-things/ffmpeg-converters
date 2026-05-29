# ffmpeg-converters

A collection of Python scripts that provide a simple wrapper around `ffmpeg.exe` for common audio, image, and video conversion tasks.

## Technical Approach

- Uses `subprocess` to call `ffmpeg.exe` with pre-built command templates
- No need to remember complex FFmpeg flags
- Batch processing support
- Simple Python interface for common operations

## Supported Operations (Typical)

- Video conversion (MP4 ↔ MKV, etc.)
- Audio extraction and format conversion (MP3, WAV, AAC)
- Image format conversion and resizing (PNG, JPG, WebP)
- Compression presets
- Thumbnail generation

## File Structure

```
ffmpeg-converters/
├── main.py                 # Interactive menu or direct script calls
├── convert_video.py        # Video-specific wrapper
├── convert_audio.py        # Audio extraction/conversion
├── requirements.txt
├── README.md
└── LICENSE
```

## Installation

1. Place `ffmpeg.exe` in your PATH or project folder
2. `pip install -r requirements.txt`
3. Run `python main.py` or individual scripts

## Usage Example

```bash
python convert_video.py input.mp4 output.mkv --preset compress
```

## Requirements

- Python 3.8+
- FFmpeg (https://ffmpeg.org)

## License

MIT License