# ffmpeg-converters

Three batch converter scripts for audio, video, and images — all powered by ffmpeg. Drop a folder of files in, pick an output format, and everything converts in one go.

No dependencies beyond Python and ffmpeg itself.

---

## Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html) — either installed system-wide (`ffmpeg` on PATH) or placed in a `./ffmpeg/` subfolder next to the scripts

---

## Usage

Download this repo and run whichever script matches your media type:

```bash
python audio.py
python video.py
python image.py
```

Each script will ask for:
1. **Input folder** — the folder containing your files
2. **Output folder** — where converted files are saved (created automatically if it doesn't exist)
3. **Output format** — pick from a numbered list

Already-converted files are skipped automatically so re-running is safe.

---

## Supported formats

### Audio (`audio.py`)

| Output | Codec | Bitrate |
|--------|-------|---------|
| mp3 | libmp3lame | 192k |
| aac | aac | 192k |
| wav | pcm_s16le | lossless |
| opus | libopus | 128k |
| flac | flac | lossless |
| m4a | aac | 192k |
| ogg | libvorbis | 160k |

**Input:** `.flac` `.mp3` `.wav` `.aac` `.opus` `.m4a` `.wma` `.ogg` `.m4b`

### Video (`video.py`)

| Output | Video codec | Audio codec | Bitrate |
|--------|-------------|-------------|---------|
| mp4 | libx264 | aac | 2000k |
| mkv | libx264 | aac | 2000k |
| avi | libx264 | aac | 2000k |
| mov | libx264 | aac | 2000k |
| webm | libvpx-vp9 | libopus | 1500k |

**Input:** `.mp4` `.mkv` `.avi` `.mov` `.wmv` `.flv` `.webm` `.m4v` `.ts` `.vob`

### Image (`image.py`)

| Output | Codec |
|--------|-------|
| jpg | mjpeg |
| png | png |
| bmp | bmp |
| tiff | tiff |
| webp | webp |
| avif | libaom-av1 |

**Input:** `.jpg` `.jpeg` `.png` `.bmp` `.tiff` `.tif` `.webp` `.gif` `.ppm` `.tga` `.avif`

---

## ffmpeg location

The scripts check for ffmpeg in this order:

1. `./ffmpeg/ffmpeg.exe` (Windows bundled)
2. `./ffmpeg/ffmpeg` (Linux/macOS bundled)
3. System PATH (`which ffmpeg`)

To bundle ffmpeg, download a static build from [ffmpeg.org](https://ffmpeg.org/download.html) and put the binary in a `ffmpeg/` folder next to the scripts.

---

## Logs

Each script writes a log file alongside the scripts:
- `logs_audio.txt`
- `logs_video.txt`
- `logs_image.txt`

Logs include the ffmpeg path used, every file processed, success/failure status, and a final summary.

---

## License

MIT
