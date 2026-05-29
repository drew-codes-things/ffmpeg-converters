# ffmpeg-converters

A collection of Python scripts that provide a simple wrapper around `ffmpeg` for common audio, image, and video conversion tasks.

## Requirements

- **Python 3.8+**
- **ffmpeg** — must be installed separately and available on your `PATH`, **or** placed next to the scripts as `ffmpeg/ffmpeg.exe` (Windows) / `ffmpeg/ffmpeg` (Linux/macOS).

Install ffmpeg:

| Platform | Command |
|---|---|
| Ubuntu/Debian | `sudo apt install ffmpeg` |
| macOS | `brew install ffmpeg` |
| Windows | Download from [ffmpeg.org](https://ffmpeg.org/download.html) |

No Python packages are required — all scripts use the standard library only.

## File Structure

```
ffmpeg-converters/
├── main.py          # unified entry point
├── audio.py
├── video.py
├── image.py
├── common.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Usage

```bash
# Unified menu (recommended)
python main.py

# Or run each converter directly
python audio.py
python video.py
python image.py
```

Log files are written to your **output folder**.

## License

MIT License
