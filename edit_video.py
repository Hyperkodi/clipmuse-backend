import subprocess

def cut_video(input_path, start_time, duration, output_path):
    command = [
        "ffmpeg",
        "-ss", str(start_time),
        "-i", input_path,
        "-t", str(duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-y",
        output_path
    ]
    subprocess.run(command, check=True)
