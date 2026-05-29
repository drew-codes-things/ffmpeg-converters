# ffmpeg-converters

A collection of Python scripts that provide a simple wrapper around `ffmpeg` for common audio, image, and video conversion tasks. All scripts batch-process an entire input folder.

## Requirements

- **Python 3.8+**
- **ffmpeg** -> must be installed separately and available on your `PATH`, **or** placed next to the scripts as `ffmpeg/ffmpeg.exe` (Windows) / `ffmpeg/ffmpeg` (Linux/macOS).

Install ffmpeg:

| Platform | Command |
|---|---|
| Ubuntu/Debian | `sudo apt install ffmpeg` |
| macOS | `brew install ffmpeg` |
| Windows | Download from [ffmpeg.org](https://ffmpeg.org/download.html) |

No Python packages are required -> all scripts use the standard library only.

## File Structure

```
ffmpeg-converters/
    main.py          # unified entry point
    audio.py
    video.py
    image.py
    common.py
    requirements.txt
    README.md
    LICENSE
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

Each script prompts for an input folder and an output folder, scans all matching files, then converts them all in one batch. Log files are written to your output folder.

## Supported Formats

### Audio (audio.py)

| Input formats | Output formats |
|---|---|
| `.flac`, `.mp3`, `.wav`, `.aac`, `.opus`, `.m4a`, `.wma`, `.ogg`, `.m4b` | `mp3`, `aac`, `wav`, `opus`, `flac`, `m4a`, `ogg` |

### Video (video.py)

| Input formats | Output formats |
|---|---|
| `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.ts`, `.vob` | `mp4`, `mkv`, `avi`, `mov`, `webm` |

Video conversion includes a quality selector (CRF 16-28) or source bitrate mode.

### Image (image.py)

| Input formats | Output formats |
|---|---|
| `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`, `.webp`, `.gif`, `.ppm`, `.tga`, `.avif` | `jpg`, `png`, `bmp`, `tiff`, `webp`, `avif` |

## License

MIT License
