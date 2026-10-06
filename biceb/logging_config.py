"""Application logging in the user's writable data directory."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(directory: str | Path) -> Path:
    log_directory = Path(directory)
    log_directory.mkdir(parents=True, exist_ok=True)
    log_path = log_directory / "biceb.log"
    handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root = logging.getLogger("biceb")
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    return log_path
