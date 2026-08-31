from pathlib import Path

def ensure_media_dirs(root):
    Path(root).mkdir(parents=True, exist_ok=True)
