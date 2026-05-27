import os
import sys
from common import (
    find_ffmpeg, init_log, write_log, prompt_folders,
    get_files, pick_format, run_batch
)

FORMATS = {
    "mp4":  ("libx264",    "aac",      "2000k"),
    "mkv":  ("libx264",    "aac",      "2000k"),
    "avi":  ("libx264",    "aac",      "2000k"),
    "mov":  ("libx264",    "aac",      "2000k"),
    "webm": ("libvpx-vp9", "libopus",  "1500k"),
}

INPUT_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".ts", ".vob"}


def build_cmd(ffmpeg_path, input_file, output_file):
    ext = os.path.splitext(output_file)[1].lstrip(".")
    vcodec, acodec, bitrate = FORMATS[ext]
    return [
        ffmpeg_path, "-y", "-i", input_file,
        "-c:v", vcodec, "-b:v", bitrate,
        "-c:a", acodec,
        output_file,
    ]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, "logs_video.txt")
    init_log(log_file, "Batch Video Converter")

    ffmpeg_path = find_ffmpeg(script_dir)
    if not ffmpeg_path:
        print("ERROR: ffmpeg not found. Install it or put it in ./ffmpeg/")
        sys.exit(1)
    write_log(log_file, f"ffmpeg: {ffmpeg_path}")

    input_folder, output_folder = prompt_folders(log_file)
    if not input_folder:
        sys.exit(1)

    files = get_files(input_folder, INPUT_EXTS)
    if not files:
        print("No video files found in input folder.")
        sys.exit(0)
    print(f"Found {len(files)} video file(s).")
    write_log(log_file, f"Files: {files}")

    output_ext = pick_format(FORMATS, log_file)
    if not output_ext:
        sys.exit(1)

    run_batch(ffmpeg_path, build_cmd, files, input_folder, output_folder, output_ext, log_file)


if __name__ == "__main__":
    main()
