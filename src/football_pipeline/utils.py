import re


def sanitize_url(url: str) -> str:
    """Creates a short, valid dictionary key from a URL."""
    return re.sub(r"https?://|www\.|[^a-zA-Z0-9]", "_", url).strip("_")
