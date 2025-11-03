import subprocess
import cv2
import base64
from pathlib import Path
import shutil

def execute_manim(file_path: str):
    manim_path = shutil.which("manim")
    if not manim_path:
        return {
            "stdout": "",
            "stderr": "Manim not found in current environment",
            "returncode": -1
        }

    cmd = f"{manim_path} -pqh {file_path}"

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        executable="/bin/bash"
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

def get_frames_from_video(video_path: str, stride: int = 25) -> list[str]:
    """Extract every Nth frame from a video as base64-encoded JPEGs."""
    if not Path(video_path).exists():
        return []
    video = cv2.VideoCapture(video_path)
    frames = []
    i = 0
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        if i % stride == 0:
            _, buffer = cv2.imencode(".jpg", frame)
            frames.append(base64.b64encode(buffer).decode("utf-8"))
        i += 1
    video.release()
    return frames
