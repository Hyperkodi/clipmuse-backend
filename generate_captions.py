import subprocess

def add_captions(video_path, transcript_text, start_time, duration, output_path):
    subtitles_file = "subtitles.srt"

    with open(subtitles_file, "w") as f:
        f.write(f"1\n")
        f.write(f"00:00:00,000 --> 00:00:{duration:02d},000\n")
        f.write(transcript_text.strip())

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={subtitles_file}",
        "-c:a", "copy",
        "-y",
        output_path
    ]
    subprocess.run(command, check=True)
