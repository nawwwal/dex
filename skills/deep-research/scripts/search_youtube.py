#!/usr/bin/env python3
"""Search YouTube and extract video transcripts using yt-dlp."""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from utils import clean_text, format_duration, save_json


def parse_vtt_transcript(vtt_path: Path) -> str:
    """Parse VTT subtitle file and extract plain text.

    Args:
        vtt_path: Path to .vtt subtitle file

    Returns:
        Plain text transcript with timestamps removed
    """
    if not vtt_path.exists():
        return ""

    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove VTT header
    content = re.sub(r'^WEBVTT.*?\n\n', '', content, flags=re.DOTALL)

    # Remove timestamp lines (00:00:00.000 --> 00:00:05.000)
    content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?\n', '', content)

    # Remove position/alignment tags
    content = re.sub(r'<c>|</c>|<\d{2}:\d{2}:\d{2}\.\d{3}>', '', content)

    # Remove sequence numbers
    content = re.sub(r'^\d+\n', '', content, flags=re.MULTILINE)

    # Clean up excess whitespace
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    text = ' '.join(lines)

    return clean_text(text)


def search_youtube(
    query: str,
    max_results: int = 50,
    min_duration: int = 120,
) -> tuple[List[Dict], List[Dict]]:
    """Search YouTube and extract video metadata with transcripts.

    Args:
        query: Search query
        max_results: Maximum number of results
        min_duration: Minimum video duration in seconds

    Returns:
        Tuple of (videos_with_transcripts, videos_without_transcripts)
    """
    videos_with_transcripts = []
    videos_without_transcripts = []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # yt-dlp command to search and download metadata + subtitles
        # Use venv yt-dlp if available, fall back to PATH
        import shutil, os as _os
        _venv_ytdlp = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), '.venv', 'bin', 'yt-dlp')
        _ytdlp_bin = _venv_ytdlp if _os.path.exists(_venv_ytdlp) else (shutil.which('yt-dlp') or 'yt-dlp')
        cmd = [
            _ytdlp_bin,
            f'ytsearch{max_results}:{query}',
            '--dump-json',
            '--write-auto-sub',
            '--sub-lang', 'en',
            '--skip-download',
            '--no-warnings',
            '--quiet',
            '--no-check-certificates',
            '-o', str(tmpdir_path / '%(id)s.%(ext)s'),
        ]

        print(f"Searching YouTube for: {query}", file=sys.stderr)
        print(f"Max results: {max_results}", file=sys.stderr)

        try:
            # Run yt-dlp and capture output
            # Note: check=False because yt-dlp exits non-zero when subtitles unavailable,
            # even if metadata was successfully extracted
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0 and not result.stdout.strip():
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)

            # Parse JSON output (one JSON object per line)
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue

                try:
                    video_data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                video_id = video_data.get('id')
                duration = video_data.get('duration', 0)

                # Skip videos shorter than minimum duration
                if duration < min_duration:
                    continue

                # Look for transcript file
                vtt_path = tmpdir_path / f"{video_id}.en.vtt"
                transcript = parse_vtt_transcript(vtt_path)

                video_info = {
                    'video_id': video_id,
                    'title': video_data.get('title', ''),
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'channel': video_data.get('channel', ''),
                    'duration': duration,
                    'duration_formatted': format_duration(duration),
                    'view_count': video_data.get('view_count', 0),
                    'upload_date': video_data.get('upload_date', ''),
                }

                if transcript:
                    # Video has transcript - add to transcript list
                    word_count = len(transcript.split())
                    video_info['transcript'] = transcript
                    video_info['word_count'] = word_count
                    videos_with_transcripts.append(video_info)
                else:
                    # No transcript - will upload URL directly to NotebookLM
                    videos_without_transcripts.append(video_info)

        except subprocess.CalledProcessError as e:
            print(f"Error running yt-dlp: {e}", file=sys.stderr)
            if e.stderr:
                print(f"stderr: {e.stderr}", file=sys.stderr)
            raise

    return videos_with_transcripts, videos_without_transcripts


def main():
    parser = argparse.ArgumentParser(
        description='Search YouTube and extract video transcripts'
    )
    parser.add_argument('query', help='Search query')
    parser.add_argument('output', help='Output JSON file path')
    parser.add_argument(
        '--max-results',
        type=int,
        default=50,
        help='Maximum number of results (default: 50)',
    )
    parser.add_argument(
        '--min-duration',
        type=int,
        default=120,
        help='Minimum video duration in seconds (default: 120)',
    )

    args = parser.parse_args()

    # Search YouTube
    videos_with_transcripts, videos_without_transcripts = search_youtube(
        query=args.query,
        max_results=args.max_results,
        min_duration=args.min_duration,
    )

    # Prepare output
    output_data = {
        'query': args.query,
        'total_found': len(videos_with_transcripts) + len(videos_without_transcripts),
        'with_transcripts': len(videos_with_transcripts),
        'without_transcripts': len(videos_without_transcripts),
        'timestamp': datetime.now().isoformat(),
        'videos': videos_with_transcripts,
        'videos_no_transcript': videos_without_transcripts,
    }

    # Save to file
    save_json(output_data, args.output)

    # Print summary
    print(f"✓ Found {len(videos_with_transcripts)} videos with transcripts", file=sys.stderr)
    if videos_with_transcripts:
        total_words = sum(v['word_count'] for v in videos_with_transcripts)
        print(f"✓ Total transcript words: {total_words:,}", file=sys.stderr)
    print(f"✓ Found {len(videos_without_transcripts)} videos without transcripts (will upload URLs)", file=sys.stderr)
    print(f"✓ Total videos: {len(videos_with_transcripts) + len(videos_without_transcripts)}", file=sys.stderr)
    print(f"✓ Saved to: {args.output}", file=sys.stderr)


if __name__ == '__main__':
    main()
