# ffmpeg-converters

A collection of Python scripts that provide a simple wrapper around `ffmpeg.exe` for common audio, image, and video conversion tasks.

## Technical Approach

- Uses `subprocess` to call `ffmpeg.exe` with pre-built command templates

## File Structure

```
ffmpeg-converters/
├── main.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Installation (Recommended: Virtual Environment)

### On Linux / macOS

```bash
git clone https://github.com/drew-codes-things/ffmpeg-converters.git
cd ffmpeg-converters

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### On Windows

```bash
git clone https://github.com/drew-codes-things/ffmpeg-converters.git
cd ffmpeg-converters

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Requirements

- Python 3.8+
- FFmpeg installed

## License

MIT License