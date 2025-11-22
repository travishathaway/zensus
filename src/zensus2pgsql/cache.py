"""
Functions for interacting with application cache
"""

import os
from pathlib import Path

import platformdirs

from .constants import APP_NAME
from .errors import Zensus2PgsqlError

CACHE = platformdirs.user_cache_dir(APP_NAME)


def create_cache_dir():
    """
    Ensures cache directory exists.
    """
    if not os.path.exists(CACHE):
        os.makedirs(CACHE)


def save_to_cache(path: Path, save_bytes: bool = False):
    """
    Saves file to cache directory.
    """
    try:
        if save_bytes:
            path.write_bytes(path.read_bytes())
        else:
            path.write_text(path.read_text())
    except OSError as exc:
        raise Zensus2PgsqlError("Unable to save file to cache") from exc
