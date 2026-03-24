#!/usr/bin/env python3
"""Extract content from web articles."""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import html2text
import requests
from bs4 import BeautifulSoup
from readability import Document

from utils import clean_text, estimate_reading_time, load_json, save_json


def extract_article_content(url: str, timeout: int = 10) -> Dict:
    """Extract readable content from a web article.

    Args:
        url: Article URL
        timeout: Request timeout in seconds

    Returns:
        Dictionary with article metadata and content
    """
    result = {
        'url': url,
        'success': False,
        'error': None,
        'title': '',
        'content': '',
        'word_count': 0,
        'reading_time': 0,
    }

    try:
        # Fetch URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, headers=headers, timeout=timeout, verify=False)
        response.raise_for_status()

        # Extract main content using readability
        doc = Document(response.text)

        # Get title
        result['title'] = doc.title()

        # Parse HTML and convert to text
        soup = BeautifulSoup(doc.summary(), 'html.parser')

        # Convert to markdown for better formatting
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.ignore_emphasis = False
        h.body_width = 0  # Don't wrap text

        content = h.handle(str(soup))
        content = clean_text(content)

        result['content'] = content
        result['word_count'] = len(content.split())
        result['reading_time'] = estimate_reading_time(result['word_count'])
        result['success'] = True

    except requests.exceptions.Timeout:
        result['error'] = 'Request timeout'
    except requests.exceptions.HTTPError as e:
        result['error'] = f'HTTP error: {e.response.status_code}'
    except Exception as e:
        result['error'] = str(e)

    return result


def process_urls(
    urls: List[str],
    min_words: int = 300,
) -> Dict:
    """Process multiple URLs and extract content.

    Args:
        urls: List of article URLs
        min_words: Minimum word count to include article

    Returns:
        Dictionary with successful and failed extractions
    """
    successful = []
    failed = []

    for i, url in enumerate(urls, 1):
        print(f"Processing {i}/{len(urls)}: {url}", file=sys.stderr)

        result = extract_article_content(url)

        if result['success'] and result['word_count'] >= min_words:
            successful.append(result)
            print(f"  ✓ {result['word_count']} words", file=sys.stderr)
        else:
            failed.append(result)
            error_msg = result.get('error', 'too short')
            print(f"  ✗ {error_msg}", file=sys.stderr)

    return {
        'successful': successful,
        'failed': failed,
        'total_processed': len(urls),
        'success_count': len(successful),
        'fail_count': len(failed),
    }


def main():
    parser = argparse.ArgumentParser(
        description='Extract content from web articles'
    )
    parser.add_argument('urls_file', help='JSON file with URLs to process')
    parser.add_argument('output', help='Output JSON file path')
    parser.add_argument(
        '--min-words',
        type=int,
        default=300,
        help='Minimum word count (default: 300)',
    )

    args = parser.parse_args()

    # Load URLs from input file
    input_data = load_json(args.urls_file)
    urls = input_data.get('urls', [])

    if not urls:
        print("No URLs found in input file", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(urls)} URLs...", file=sys.stderr)

    # Process URLs
    results = process_urls(urls, min_words=args.min_words)

    # Add metadata
    results['timestamp'] = datetime.now().isoformat()
    results['query'] = input_data.get('query', '')

    # Save results
    save_json(results, args.output)

    # Print summary
    print(f"\n✓ {results['success_count']} articles extracted", file=sys.stderr)
    print(f"✗ {results['fail_count']} failed", file=sys.stderr)
    total_words = sum(a['word_count'] for a in results['successful'])
    print(f"✓ Total words: {total_words:,}", file=sys.stderr)
    print(f"✓ Saved to: {args.output}", file=sys.stderr)


if __name__ == '__main__':
    main()
