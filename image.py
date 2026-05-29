import os
import sys
from common import (
    find_ffmpeg, init_log, write_log, prompt_folders,
    get_files, pick_format, run_batch
)

FORMATS = {
    "jpg":  "mjpeg",
    "png":  "png",
    "bmp":  "bmp",
    "tiff": "tiff",
    "webp": "webp",
    "avif": "libaom-av1",
}

INPUT_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp", ".gif", ".ppm", ".tga", ".avif"}


def build_cmd(ffmpeg_path, input_file, output_file):
    ext = os.path.splitext(output_file)[1].lstrip(".")
    codec = FORMATS[ext]
    return [ffmpeg_path, "-y", "-i", input_file, "-vcodec", codec, output_file]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_folder, output_folder = prompt_folders()
    if not input_folder:
        sys.exit(1)

    log_file = os.path.join(output_folder, "logs_image.txt")
    init_log(log_file, "Batch Image Converter")

    ffmpeg_path = find_ffmpeg(script_dir)
    if not ffmpeg_path:
        print("ERROR: ffmpeg not found. Install it or put it in ./ffmpeg/")
        sys.exit(1)
    write_log(log_file, f"ffmpeg: {ffmpeg_path}")
    write_log(log_file, f"Input:  {input_folder}")
    write_log(log_file, f"Output: {output_folder}")

    files = get_files(input_folder, INPUT_EXTS)
    if not files:
        print("No image files found in input folder.")
        sys.exit(0)
    print(f"Found {len(files)} image file(s).")
    write_log(log_file, f"Files: {files}")

    output_ext = pick_format(FORMATS, log_file)
    if not output_ext:
        sys.exit(1)

    run_batch(ffmpeg_path, build_cmd, files, input_folder, output_folder, output_ext, log_file)


if __name__ == "__main__":
    main()
