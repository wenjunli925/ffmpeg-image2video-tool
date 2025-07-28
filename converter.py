import os
import subprocess
import shutil

FFMPEG_BINARY = shutil.which("ffmpeg")

if not FFMPEG_BINARY:
    # Fall back to bundled path or show error
    FFMPEG_BINARY = "/usr/local/bin/ffmpeg"


# def convert_sequence_to_video(input_pattern, output_path, fps=24):
#     command = [FFMPEG_BINARY, "-framerate", str(fps), "-i", input_pattern, "-c:v", "libx264", "-pix_fmt", "yuv420p", output_path]

#     try:
#         subprocess.run(command, check=True)
#         return True, None
#     except subprocess.CalledProcessError as e:
#         return False, str(e)


def convert_sequence_to_video(input_pattern, output_path, fps=24):
    ffmpeg_path = os.path.join(os.path.dirname(__file__), "resources", "ffmpeg")
    
    cmd = [
        ffmpeg_path,
        "-framerate", str(fps),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-y",  # Overwrite output if it exists
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, str(e)