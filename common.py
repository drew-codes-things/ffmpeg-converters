"""Shared utilities used by audio.py, video.py, and image.py."""
import os
import shutil
import datetime


def clean_path(path):
    return path.strip().strip('"').strip("'")


def find_ffmpeg(script_dir):
    """Look for ffmpeg bundled next to the script, then fall back to PATH."""
    candidates = [
        os.path.join(script_dir, "ffmpeg", "ffmpeg.exe"),
        os.path.join(script_dir, "ffmpeg", "ffmpeg"),
    ]
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return shutil.which("ffmpeg")


def write_log(path, text):
    with open(path, "a", encoding="utf-8") as log:
        log.write(text + "\n")


def init_log(path, title):
    with open(path, "w", encoding="utf-8") as log:
        log.write(f"=== {title} — Made by Drew ===\n")
        log.write(f"Started: {datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}\n\n")


def print_progress(current, total, filename):
    bar_length = 40
    filled = int(bar_length * current // total)
    bar = "█" * filled + "-" * (bar_length - filled)
    display_name = (filename[:36] + "...") if len(filename) > 39 else filename
    print(f"\r[{bar}] {current}/{total}  {display_name:42}", end="", flush=True)


def get_files(folder, extensions):
    files = []
    for f in sorted(os.listdir(folder)):
        if os.path.isfile(os.path.join(folder, f)):
            if os.path.splitext(f)[1].lower() in extensions:
                files.append(f)
    return files


def prompt_folders(log_file):
    """Ask for input/output folders, validate, create output if needed."""
    input_folder = clean_path(input("Input folder path: "))
    output_folder = clean_path(input("Output folder path: "))
    write_log(log_file, f"Input:  {input_folder}")
    write_log(log_file, f"Output: {output_folder}")
    if not os.path.isdir(input_folder):
        print(f"ERROR: Input folder not found: {input_folder}")
        return None, None
    if not os.path.isdir(output_folder):
        print(f"Creating output folder: {output_folder}")
        os.makedirs(output_folder, exist_ok=True)
    return input_folder, output_folder


def pick_format(formats, log_file):
    """Print numbered format list and return chosen key, or None on bad input."""
    keys = list(formats.keys())
    print("\nAvailable output formats:")
    for i, k in enumerate(keys, 1):
        print(f"  {i}. {k}")
    raw = input("Choose format number: ").strip()
    try:
        idx = int(raw) - 1
        if not (0 <= idx < len(keys)):
            raise ValueError
        chosen = keys[idx]
        write_log(log_file, f"Output format: .{chosen}")
        return chosen
    except ValueError:
        print("Invalid choice.")
        return None


def run_batch(ffmpeg_path, build_cmd, files, input_folder, output_folder, output_ext, log_file):
    """Run ffmpeg on every file, track success/failure, print summary."""
    total = len(files)
    ok = 0
    failed = []

    import subprocess
    for idx, filename in enumerate(files, 1):
        input_file = os.path.join(input_folder, filename)
        base = os.path.splitext(filename)[0]
        output_file = os.path.join(output_folder, base + "." + output_ext)

        if os.path.exists(output_file):
            write_log(log_file, f"[{idx}/{total}] SKIPPED (exists): {output_file}")
            print_progress(idx, total, filename + " [skip]")
            ok += 1
            continue

        print_progress(idx, total, filename)
        write_log(log_file, f"[{idx}/{total}] {input_file} -> {output_file}")

        cmd = build_cmd(ffmpeg_path, input_file, output_file)
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stderr_text = result.stderr.decode("utf-8", errors="replace").strip()
            if stderr_text:
                write_log(log_file, stderr_text)
            write_log(log_file, f"[{idx}/{total}] OK\n")
            ok += 1
        except subprocess.CalledProcessError as e:
            err = e.stderr.decode("utf-8", errors="replace") if e.stderr else str(e)
            write_log(log_file, f"[{idx}/{total}] ERROR:\n{err}\n")
            failed.append(filename)
        except Exception as e:
            write_log(log_file, f"[{idx}/{total}] UNEXPECTED: {e}\n")
            failed.append(filename)

    print()
    print(f"\nDone. {ok}/{total} converted successfully.")
    if failed:
        print(f"Failed ({len(failed)}):")
        for f in failed:
            print(f"  - {f}")
    write_log(log_file, f"\nFinished: {datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}")
    write_log(log_file, f"Result: {ok}/{total} OK, {len(failed)} failed")
