"""Utility functions for apriscout."""

import re


def is_valid_username(username: str, max_length=32) -> bool:
    """Username alphanumberic and underscores only."""
    return re.fullmatch(rf"[A-Za-z0-9_]{{1,{max_length}}}", username) is not None
