import os
import sys
from common import (
    find_ffmpeg, init_log, write_log, prompt_folders,
    get_files, pick_format, run_batch
)

FORMATS = {
    "mp4":  ("libx264",    "aac"),
    "mkv":  ("libx264",    "aac"),
    "avi":  ("libx264",    "aac"),
    "mov":  ("libx264",    "aac"),
    "webm": ("libvpx-vp9", "libopus"),
}

INPUT_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".ts", ".vob"}

# Quality scale: 1 (smallest/worst) → 5 (largest/best)
CRF_MAP = {1: 28, 2: 24, 3: 20, 4: 18, 5: 16}


def ask_bitrate_mode():
    print("\nVideo quality:")
    print("  s. Use source bitrate (CRF 18 — near-lossless)")
    print("  1. Quality 1 — smallest file  (CRF 28)")
    print("  2. Quality 2                   (CRF 24)")
    print("  3. Quality 3 — balanced        (CRF 20)")
    print("  4. Quality 4                   (CRF 18)")
    print("  5. Quality 5 — best quality    (CRF 16)")
    raw = input("Choose [s/1-5] [3]: ").strip().lower() or '3'
    if raw == 's':
        return None, None  # source bitrate → use CRF 18 lossless-quality
    try:
        q = int(raw)
        if 1 <= q <= 5:
            return q, CRF_MAP[q]
    except ValueError:
        pass
    print("Invalid, using quality 3 (CRF 20).")
    return 3, 20


def build_cmd_factory(use_source_bitrate, crf):
    def build_cmd(ffmpeg_path, input_file, output_file):
        ext = os.path.splitext(output_file)[1].lstrip(".")
        vcodec, acodec = FORMATS[ext]
        if use_source_bitrate:
            video_args = ["-c:v", vcodec, "-b:v", "0", "-crf", "18"]
        else:
            video_args = ["-c:v", vcodec, "-crf", str(crf)]
        return [
            ffmpeg_path, "-y", "-i", input_file,
            *video_args,
            "-c:a", acodec,
            output_file,
        ]
    return build_cmd


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_folder, output_folder = prompt_folders()
    if not input_folder:
        sys.exit(1)

    log_file = os.path.join(output_folder, "logs_video.txt")
    init_log(log_file, "Batch Video Converter")

    ffmpeg_path = find_ffmpeg(script_dir)
    if not ffmpeg_path:
        print("ERROR: ffmpeg not found. Install it or put it in ./ffmpeg/")
        sys.exit(1)
    write_log(log_file, f"ffmpeg: {ffmpeg_path}")
    write_log(log_file, f"Input:  {input_folder}")
    write_log(log_file, f"Output: {output_folder}")

    files = get_files(input_folder, INPUT_EXTS)
    if not files:
        print("No video files found in input folder.")
        sys.exit(0)
    print(f"Found {len(files)} video file(s).")
    write_log(log_file, f"Files: {files}")

    output_ext = pick_format(FORMATS, log_file)
    if not output_ext:
        sys.exit(1)

    q, crf = ask_bitrate_mode()
    use_source = (q is None)
    if use_source:
        print("Using source bitrate mode (CRF 18).")
        write_log(log_file, "Bitrate mode: source (CRF 18)")
    else:
        print(f"Using quality {q} (CRF {crf}).")
        write_log(log_file, f"Bitrate mode: quality {q} (CRF {crf})")

    build_cmd = build_cmd_factory(use_source, crf if not use_source else 18)
    run_batch(ffmpeg_path, build_cmd, files, input_folder, output_folder, output_ext, log_file)


if __name__ == "__main__":
    main()
