import os
import subprocess

CODECS = {
    "mp3":   ("libmp3lame", "192k"),
    "aac":   ("aac", "192k"),
    "wav":   ("pcm_s16le", None),    # No bitrate for WAV
    "opus":  ("libopus", "128k"),
    "flac":  ("flac", None),          # Lossless
}

INPUT_EXTENSIONS = [".flac", ".mp3", ".wav", ".aac", ".opus", ".m4a", ".wma", ".ogg"]

def clean_path(path):
    return path.strip().strip('"').strip("'")

def get_audio_files(folder):
    files = []
    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, f)):
            ext = os.path.splitext(f)[1].lower()
            if ext in INPUT_EXTENSIONS:
                files.append(f)
    return files

def main():
    print("Batch Audio Converter — Made by Drew\n")

    input_folder = clean_path(input("Enter input folder path: "))
    output_folder = clean_path(input("Enter output folder path: "))

    ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe")
    if not os.path.isfile(ffmpeg_path):
        print(f"ffmpeg executable not found at {ffmpeg_path}")
        return

    if not os.path.isdir(input_folder):
        print(f"Input folder does not exist: {input_folder}")
        return

    if not os.path.isdir(output_folder):
        print(f"Output folder does not exist, creating: {output_folder}")
        os.makedirs(output_folder, exist_ok=True)

    audio_files = get_audio_files(input_folder)
    if not audio_files:
        print("No audio files found in input folder.")
        return

    print("Detected audio files:")
    for f in audio_files:
        print(f" - {f}")

    print("\nAvailable output formats:")
    for i, ext in enumerate(CODECS.keys(), 1):
        print(f"{i}. {ext}")

    choice = input("Choose output format by number (e.g. 1): ")
    try:
        choice_index = int(choice) - 1
        output_ext = list(CODECS.keys())[choice_index]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    codec, bitrate = CODECS[output_ext]
    print(f"\nConverting all audio files to .{output_ext} using codec {codec}...\n")

    for filename in audio_files:
        input_file = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_file = os.path.join(output_folder, base_name + "." + output_ext)

        print(f"Converting: {filename} -> {base_name}.{output_ext}")

        cmd = [
            ffmpeg_path,
            "-y",  # overwrite output
            "-i", input_file,
            "-codec:a", codec,
        ]

        if bitrate:
            cmd.extend(["-b:a", bitrate])

        cmd.append(output_file)

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"Error converting {filename}")

    print("\nBatch conversion complete!")
    print("Thank you for using the converter! Made by Drew")

if __name__ == "__main__":
    main()
