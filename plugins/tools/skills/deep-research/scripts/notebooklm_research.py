#!/usr/bin/env python3
"""Conduct research using NotebookLM with YouTube and web sources."""

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from notebooklm import NotebookLMClient

from utils import load_json, truncate_text


def get_existing_notebook_id(output_file: Path) -> Optional[str]:
    """Check if a notebook already exists for this research topic.

    Args:
        output_file: Path to the output summary file

    Returns:
        Existing notebook ID if found, None otherwise
    """
    # Look for notebook_id.txt in the same directory as output file
    notebook_id_file = output_file.parent / "notebook_id.txt"

    if notebook_id_file.exists():
        try:
            notebook_id = notebook_id_file.read_text().strip()
            if notebook_id:
                print(f"✓ Found existing notebook ID: {notebook_id}", file=sys.stderr)
                print(f"  Will update existing notebook instead of creating new one", file=sys.stderr)
                return notebook_id
        except Exception as e:
            print(f"⚠️  Could not read existing notebook ID: {e}", file=sys.stderr)

    return None


def save_notebook_id(output_file: Path, notebook_id: str) -> None:
    """Save notebook ID for future research updates.

    Args:
        output_file: Path to the output summary file
        notebook_id: NotebookLM notebook ID
    """
    notebook_id_file = output_file.parent / "notebook_id.txt"
    notebook_id_file.write_text(notebook_id)
    print(f"✓ Saved notebook ID to: {notebook_id_file}", file=sys.stderr)


async def create_notebook(client, topic: str) -> str:
    """Create a new NotebookLM notebook.

    Args:
        client: NotebookLM client
        topic: Research topic

    Returns:
        Notebook ID
    """
    notebook_title = f"Research: {topic}"
    print(f"Creating notebook: {notebook_title}", file=sys.stderr)

    notebook = await client.notebooks.create(notebook_title)
    notebook_id = notebook.id

    print(f"✓ Notebook created: {notebook_id}", file=sys.stderr)
    print(f"  URL: https://notebooklm.google.com/notebook/{notebook_id}", file=sys.stderr)

    return notebook_id


async def upload_youtube_sources(
    client,
    notebook_id: str,
    videos: List[Dict],
    max_chars: int = 100000,
) -> int:
    """Upload YouTube video transcripts as text sources.

    Args:
        client: NotebookLM client
        notebook_id: Notebook ID
        videos: List of video dictionaries with transcripts
        max_chars: Maximum characters per source

    Returns:
        Number of sources uploaded
    """
    print(f"\nUploading {len(videos)} YouTube transcripts...", file=sys.stderr)
    uploaded = 0

    for i, video in enumerate(videos, 1):
        try:
            title = f"[YouTube] {video['title']}"
            content = truncate_text(video['transcript'], max_chars)

            # Format content with metadata header
            source_text = f"""# {video['title']}

**Channel:** {video['channel']}
**Duration:** {video['duration_formatted']}
**URL:** {video['url']}

---

{content}
"""

            await client.sources.add_text(
                notebook_id=notebook_id,
                content=source_text,
                title=title,
            )

            uploaded += 1
            print(f"  {i}/{len(videos)} ✓ {video['title'][:60]}...", file=sys.stderr)

            # Small delay to avoid rate limiting
            await asyncio.sleep(2)

        except Exception as e:
            print(f"  {i}/{len(videos)} ✗ Error: {e}", file=sys.stderr)

    print(f"✓ Uploaded {uploaded}/{len(videos)} YouTube transcript sources", file=sys.stderr)
    return uploaded


async def upload_youtube_urls(
    client,
    notebook_id: str,
    videos: List[Dict],
) -> int:
    """Upload YouTube video URLs directly for videos without transcripts.

    Args:
        client: NotebookLM client
        notebook_id: Notebook ID
        videos: List of video dictionaries without transcripts

    Returns:
        Number of sources uploaded
    """
    if not videos:
        return 0

    print(f"\nUploading {len(videos)} YouTube videos by URL (no transcripts)...", file=sys.stderr)
    uploaded = 0

    for i, video in enumerate(videos, 1):
        try:
            # Upload YouTube URL directly - NotebookLM will process the video
            await client.sources.add_url(
                notebook_id=notebook_id,
                url=video['url'],
            )

            uploaded += 1
            print(f"  {i}/{len(videos)} ✓ {video['title'][:60]}...", file=sys.stderr)

            # Small delay to avoid rate limiting
            await asyncio.sleep(2)

        except Exception as e:
            print(f"  {i}/{len(videos)} ✗ Error: {e}", file=sys.stderr)

    print(f"✓ Uploaded {uploaded}/{len(videos)} YouTube URL sources", file=sys.stderr)
    return uploaded


async def upload_web_sources(
    client,
    notebook_id: str,
    articles: List[Dict],
    max_chars: int = 100000,
) -> int:
    """Upload web article content as text sources.

    Args:
        client: NotebookLM client
        notebook_id: Notebook ID
        articles: List of article dictionaries with content
        max_chars: Maximum characters per source

    Returns:
        Number of sources uploaded
    """
    print(f"\nUploading {len(articles)} web articles...", file=sys.stderr)
    uploaded = 0

    for i, article in enumerate(articles, 1):
        try:
            title = f"[Article] {article['title']}"
            content = truncate_text(article['content'], max_chars)

            # Format content with metadata header
            source_text = f"""# {article['title']}

**URL:** {article['url']}
**Word Count:** {article['word_count']:,}
**Reading Time:** {article['reading_time']} min

---

{content}
"""

            await client.sources.add_text(
                notebook_id=notebook_id,
                content=source_text,
                title=title,
            )

            uploaded += 1
            print(f"  {i}/{len(articles)} ✓ {article['title'][:60]}...", file=sys.stderr)

            # Small delay to avoid rate limiting
            await asyncio.sleep(2)

        except Exception as e:
            print(f"  {i}/{len(articles)} ✗ Error: {e}", file=sys.stderr)

    print(f"✓ Uploaded {uploaded}/{len(articles)} web sources", file=sys.stderr)
    return uploaded


async def conduct_research(
    client,
    notebook_id: str,
    research_prompt: str,
    timeout: int = 1800,
) -> str:
    """Trigger NotebookLM research and wait for completion.

    Args:
        client: NotebookLM client
        notebook_id: Notebook ID
        research_prompt: Research prompt text
        timeout: Maximum wait time in seconds

    Returns:
        Research results text
    """
    print(f"\nStarting NotebookLM research...", file=sys.stderr)
    print(f"Timeout: {timeout}s ({timeout // 60} minutes)", file=sys.stderr)

    try:
        # Trigger research using chat
        response = await client.chat.ask(
            notebook_id=notebook_id,
            question=research_prompt,
        )

        result_text = response.text if hasattr(response, 'text') else str(response)

        print(f"✓ Research complete!", file=sys.stderr)
        print(f"  Response length: {len(result_text):,} characters", file=sys.stderr)

        return result_text

    except asyncio.TimeoutError:
        print(f"✗ Research timed out after {timeout}s", file=sys.stderr)
        raise
    except Exception as e:
        print(f"✗ Research error: {e}", file=sys.stderr)
        raise


def generate_summary_markdown(
    topic: str,
    research_text: str,
    notebook_id: str,
    youtube_count: int,
    web_count: int,
    output_file: Path,
) -> None:
    """Generate final markdown summary.

    Args:
        topic: Research topic
        research_text: NotebookLM research results
        notebook_id: Notebook ID
        youtube_count: Number of YouTube sources
        web_count: Number of web sources
        output_file: Output file path
    """
    summary = f"""# {topic}

**Research Date:** {datetime.now().strftime('%Y-%m-%d')}
**Sources:** {youtube_count} YouTube videos, {web_count} articles
**NotebookLM:** [View Notebook](https://notebooklm.google.com/notebook/{notebook_id})

---

{research_text}

---

## Research Metadata

- **YouTube Videos Analyzed:** {youtube_count}
- **Web Articles Analyzed:** {web_count}
- **Total Sources:** {youtube_count + web_count}
- **Research Tool:** NotebookLM
- **Generated:** {datetime.now().isoformat()}
"""

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"\n✓ Summary saved to: {output_file}", file=sys.stderr)


async def main():
    parser = argparse.ArgumentParser(
        description='Conduct research using NotebookLM'
    )
    parser.add_argument('topic', help='Research topic')
    parser.add_argument('youtube_file', help='YouTube sources JSON file')
    parser.add_argument('web_file', help='Web sources JSON file')
    parser.add_argument('prompt_file', help='Research prompt file')
    parser.add_argument('output', help='Output markdown file')
    parser.add_argument(
        '--timeout',
        type=int,
        default=1800,
        help='Research timeout in seconds (default: 1800)',
    )

    args = parser.parse_args()

    # Load sources
    youtube_data = load_json(args.youtube_file)
    web_data = load_json(args.web_file)
    videos_with_transcripts = youtube_data.get('videos', [])
    videos_without_transcripts = youtube_data.get('videos_no_transcript', [])
    articles = web_data.get('successful', [])

    # Load research prompt
    with open(args.prompt_file, 'r', encoding='utf-8') as f:
        research_prompt = f.read()

    print(f"Research Topic: {args.topic}", file=sys.stderr)
    print(f"YouTube videos with transcripts: {len(videos_with_transcripts)}", file=sys.stderr)
    print(f"YouTube videos without transcripts: {len(videos_without_transcripts)}", file=sys.stderr)
    print(f"Web sources: {len(articles)}", file=sys.stderr)

    output_path = Path(args.output)

    # Initialize NotebookLM client
    async with await NotebookLMClient.from_storage() as client:
        # Check for existing notebook or create new one
        existing_notebook_id = get_existing_notebook_id(output_path)

        if existing_notebook_id:
            notebook_id = existing_notebook_id
            print(f"  URL: https://notebooklm.google.com/notebook/{notebook_id}", file=sys.stderr)
        else:
            notebook_id = await create_notebook(client, args.topic)
            # Save notebook ID for future updates
            save_notebook_id(output_path, notebook_id)

        # Upload sources
        yt_transcript_uploaded = await upload_youtube_sources(client, notebook_id, videos_with_transcripts)
        yt_url_uploaded = await upload_youtube_urls(client, notebook_id, videos_without_transcripts)
        web_uploaded = await upload_web_sources(client, notebook_id, articles)

        total_uploaded = yt_transcript_uploaded + yt_url_uploaded + web_uploaded

        if total_uploaded == 0:
            print("\n✗ No sources uploaded successfully", file=sys.stderr)
            sys.exit(1)

        # Conduct research
        research_text = await conduct_research(
            client,
            notebook_id,
            research_prompt,
            timeout=args.timeout,
        )

        # Generate summary
        generate_summary_markdown(
            topic=args.topic,
            research_text=research_text,
            notebook_id=notebook_id,
            youtube_count=yt_transcript_uploaded + yt_url_uploaded,
            web_count=web_uploaded,
            output_file=Path(args.output),
        )


if __name__ == '__main__':
    asyncio.run(main())
