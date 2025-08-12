import os
import subprocess
import shutil
import datetime

CODECS = {
    "mp3":   ("libmp3lame", "192k"),
    "aac":   ("aac", "192k"),
    "wav":   ("pcm_s16le", None),
    "opus":  ("libopus", "128k"),
    "flac":  ("flac", None),
}

INPUT_EXTENSIONS = [".flac", ".mp3", ".wav", ".aac", ".opus", ".m4a", ".wma", ".ogg"]

def clean_path(path):
    return path.strip().strip('"').strip("'")

def get_audio_files(folder):
    files = []
    for f in sorted(os.listdir(folder)):
        full = os.path.join(folder, f)
        if os.path.isfile(full):
            ext = os.path.splitext(f)[1].lower()
            if ext in INPUT_EXTENSIONS:
                files.append(f)
    return files

def find_ffmpeg(script_dir):
    candidates = [
        os.path.join(script_dir, "ffmpeg", "ffmpeg.exe"),
        os.path.join(script_dir, "ffmpeg", "ffmpeg")
    ]
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    which = shutil.which("ffmpeg")
    return which

def write_log(path, text):
    with open(path, "a", encoding="utf-8") as log:
        log.write(text + "\n")

def print_progress(current, total, filename):
    bar_length = 40
    filled = int(bar_length * current // total)
    bar = "█" * filled + "-" * (bar_length - filled)
    display_name = (filename[:36] + "...") if len(filename) > 39 else filename
    print(f"\r[{bar}] {current}/{total} Converting: {display_name:40}", end="", flush=True)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, "logs.txt")

    with open(log_file, "w", encoding="utf-8") as log:
        log.write("=== Batch Audio Converter — Made by Drew ===\n")
        log.write(f"Started: {datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}\n")
        log.write(f"Script dir: {script_dir}\n\n")

    input_folder = clean_path(input("Enter input folder path: "))
    output_folder = clean_path(input("Enter output folder path: "))

    write_log(log_file, f"Input folder: {input_folder}")
    write_log(log_file, f"Output folder: {output_folder}")

    ffmpeg_path = find_ffmpeg(script_dir)
    if not ffmpeg_path:
        msg = "ERROR: ffmpeg executable not found (tried ./ffmpeg/ffmpeg.exe, ./ffmpeg/ffmpeg, and PATH)."
        print(msg)
        write_log(log_file, msg)
        return

    write_log(log_file, f"Using ffmpeg: {ffmpeg_path}")

    if not os.path.isdir(input_folder):
        msg = f"ERROR: Input folder does not exist: {input_folder}"
        print(msg)
        write_log(log_file, msg)
        return

    if not os.path.isdir(output_folder):
        msg = f"Output folder does not exist, creating: {output_folder}"
        print(msg)
        write_log(log_file, msg)
        os.makedirs(output_folder, exist_ok=True)

    audio_files = get_audio_files(input_folder)
    if not audio_files:
        msg = "No audio files found in input folder."
        print(msg)
        write_log(log_file, msg)
        return

    write_log(log_file, "Detected audio files:")
    for f in audio_files:
        write_log(log_file, f" - {f}")

    print("\nAvailable output formats:")
    for i, ext in enumerate(CODECS.keys(), 1):
        print(f"{i}. {ext}")
        write_log(log_file, f"Format option {i}: .{ext}")

    choice = input("Choose output format by number (e.g. 1): ")
    try:
        choice_index = int(choice) - 1
        output_ext = list(CODECS.keys())[choice_index]
    except (ValueError, IndexError):
        msg = "Invalid choice."
        print(msg)
        write_log(log_file, msg)
        return

    codec, bitrate = CODECS[output_ext]
    write_log(log_file, f"Chosen output format: .{output_ext} (codec={codec}, bitrate={bitrate})")
    write_log(log_file, "\nBeginning conversions...\n")

    total_files = len(audio_files)
    for idx, filename in enumerate(audio_files, start=1):
        input_file = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_file = os.path.join(output_folder, base_name + "." + output_ext)

        write_log(log_file, f"[{idx}/{total_files}] Converting: {input_file} -> {output_file}")
        print_progress(idx, total_files, filename)

        cmd = [
            ffmpeg_path,
            "-y",
            "-i", input_file,
            "-codec:a", codec,
        ]
        if bitrate:
            cmd.extend(["-b:a", bitrate])
        cmd.append(output_file)

        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stderr_text = result.stderr.decode("utf-8", errors="replace").strip()
            if stderr_text:
                write_log(log_file, f"ffmpeg output for {filename}:\n{stderr_text}\n")
            write_log(log_file, f"[{idx}/{total_files}] SUCCESS: {output_file}\n")
        except subprocess.CalledProcessError as e:
            err = e.stderr.decode("utf-8", errors="replace") if e.stderr else str(e)
            write_log(log_file, f"[{idx}/{total_files}] ERROR converting {filename}:\n{err}\n")
        except Exception as e:
            write_log(log_file, f"[{idx}/{total_files}] UNEXPECTED ERROR for {filename}: {e}\n")

    print()
    final_msg_console = "Thank you for using the converter! Made by Drew"
    print(final_msg_console)
    write_log(log_file, "\nBatch conversion complete!")
    write_log(log_file, final_msg_console)
    write_log(log_file, f"Finished: {datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}\n")

if __name__ == "__main__":
    main()
