"""Shared utilities for YouTube Research skill."""

import re
import json
from pathlib import Path
from typing import Any, Dict


def generate_slug(query: str) -> str:
    """Convert a search query into a filesystem-safe slug.

    Args:
        query: Search query (e.g., "API Design Best Practices")

    Returns:
        Slugified string (e.g., "api-design-best-practices")
    """
    # Convert to lowercase
    slug = query.lower()

    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)

    # Remove leading/trailing hyphens
    slug = slug.strip('-')

    # Collapse multiple hyphens
    slug = re.sub(r'-+', '-', slug)

    return slug


def save_json(data: Dict[str, Any], filepath: Path | str) -> None:
    """Save data to JSON file with formatting.

    Args:
        data: Dictionary to save
        filepath: Output file path
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(filepath: Path | str) -> Dict[str, Any]:
    """Load JSON file with error handling.

    Args:
        filepath: Input file path

    Returns:
        Parsed JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def clean_text(text: str) -> str:
    """Remove excess whitespace and control characters.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    # Remove control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

    # Normalize whitespace (collapse multiple spaces/newlines)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\n+', '\n\n', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def truncate_text(text: str, max_chars: int = 100000) -> str:
    """Truncate text to maximum character count.

    Args:
        text: Input text
        max_chars: Maximum character count

    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_chars:
        return text

    return text[:max_chars - 3] + "..."


def format_duration(seconds: int) -> str:
    """Convert seconds to MM:SS or HH:MM:SS format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def estimate_reading_time(word_count: int, words_per_minute: int = 200) -> int:
    """Estimate reading time in minutes.

    Args:
        word_count: Number of words
        words_per_minute: Reading speed (default 200 wpm)

    Returns:
        Estimated reading time in minutes
    """
    return max(1, word_count // words_per_minute)
