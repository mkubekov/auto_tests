"""Access to binary fixtures shipped with the package (images, video, text)."""

from __future__ import annotations

from pathlib import Path

RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"

IMAGE_PNG = "image.png"
IMAGE_JPG = "image.jpg"
IMAGE_WEBP = "image.webp"
VIDEO_MP4 = "video.mp4"
ICON_SVG = "icon.svg"
SAMPLE_TXT = "sample.txt"


def resource_path(name: str) -> Path:
    """Absolute path of a fixture file; raises early instead of failing inside Playwright."""
    path = RESOURCES_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Fixture file not found: {path}")
    return path
