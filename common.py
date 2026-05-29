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
        log.write(f"=== {title} - Made by Drew ===\n")
        log.write(f"Started: {datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}\n\n")


def format_size(num_bytes):
    """Human-readable file size."""
    for unit in ("B", "KB", "MB", "GB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def print_size_estimate(files, input_folder):
    """Print total input size and a rough estimated output size before converting."""
    total_bytes = sum(
        os.path.getsize(os.path.join(input_folder, f))
        for f in files
        if os.path.isfile(os.path.join(input_folder, f))
    )
    # Rough estimate: output is typically 60-90% of input for most lossy conversions.
    # We show a range rather than a single number to be honest about uncertainty.
    low  = total_bytes * 0.5
    high = total_bytes * 1.1
    print(f"  Total input size :  {format_size(total_bytes)}")
    print(f"  Estimated output :  {format_size(low)} -> {format_size(high)}  (rough range)")
    print()


def print_progress(current, total, filename):
    bar_length = 40
    filled = int(bar_length * current // total)
    bar = "#" * filled + "-" * (bar_length - filled)
    display_name = (filename[:36] + "...") if len(filename) > 39 else filename
    print(f"\r[{bar}] {current}/{total}  {display_name:42}", end="", flush=True)


def get_files(folder, extensions):
    files = []
    for f in sorted(os.listdir(folder)):
        if os.path.isfile(os.path.join(folder, f)):
            if os.path.splitext(f)[1].lower() in extensions:
                files.append(f)
    return files


def prompt_folders(output_folder_override=None):
    """Ask for input/output folders, validate, create output if needed."""
    input_folder = clean_path(input("Input folder path: "))
    output_folder = clean_path(input("Output folder path: "))
    if not os.path.isdir(input_folder):
        print(f"ERROR: Input folder not found: {input_folder}")
        return None, None
    # Resolve to absolute paths before comparing so that e.g. "./foo" and
    # "foo" are correctly detected as the same directory.
    abs_in  = os.path.realpath(input_folder)
    abs_out = os.path.realpath(output_folder)
    if abs_in == abs_out:
        print(
            "WARNING: Input and output folders are the same path. "
            "This may overwrite or corrupt your source files. "
            "Please choose a different output folder."
        )
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
    """Show estimated output size, then run ffmpeg on every file."""
    print_size_estimate(files, input_folder)

    total = len(files)
    ok = 0
    skipped = 0
    failed = []

    import subprocess
    for idx, filename in enumerate(files, 1):
        input_file = os.path.join(input_folder, filename)
        base = os.path.splitext(filename)[0]
        output_file = os.path.join(output_folder, base + "." + output_ext)

        if os.path.exists(output_file):
            skip_reason = "output already exists"
            write_log(log_file, f"[{idx}/{total}] SKIPPED ({skip_reason}): {output_file}")
            print_progress(idx, total, filename + f" [skip -- {skip_reason}]")
            skipped += 1
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
    print(f"\nDone. {ok} converted, {skipped} skipped (already existed), {len(failed)} failed.")
    if failed:
        print(f"Failed ({len(failed)}):")
        for f in failed:
            print(f"  - {f}")
    write_log(log_file, f"\nFinished: {datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}")
    write_log(log_file, f"Result: {ok} converted, {skipped} skipped, {len(failed)} failed")
