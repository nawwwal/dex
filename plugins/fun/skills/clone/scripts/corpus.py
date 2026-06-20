#!/usr/bin/env python3
"""corpus.py - normalize the user's own material into a common shape.

Shared corpus-ingestion primitive for the `fun` plugin. Owned by `clone`;
reused by `cartography` (chat export -> shape of an intimacy), `seance`
(letters/texts -> idiolect), and `augury` (collection objects, when not coming
from the mymind MCP).

Stdlib only. Privacy contract: this script reads the files you point it at,
emits a normalized view, and writes nowhere except stdout or an explicit
--out path. It does not phone home and it does not persist anything on its own.

Usage:
  corpus.py FILE [FILE ...] [--kind auto|prose|chat] [--author NAME] [--out FILE]

Output: a JSON document
  {
    "sources": [...],
    "kind": "prose" | "chat",
    "samples": [ {"author": str|null, "ts": str|null, "text": str}, ... ],
    "stats": { ... }
  }
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# WhatsApp-style: "M/D/YY, HH:MM - Author: text"  and  "[D/M/YY, HH:MM:SS] Author: text"
WHATSAPP_DASH = re.compile(
    r"^(?P<ts>\d{1,2}[/.]\d{1,2}[/.]\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?\s*(?:[APap][Mm])?)\s*-\s*(?P<author>[^:]{1,60}):\s(?P<text>.*)$"
)
WHATSAPP_BRACKET = re.compile(
    r"^\[(?P<ts>[^\]]+)\]\s*(?P<author>[^:]{1,60}):\s(?P<text>.*)$"
)
# Generic "Author: text" with a short author label.
GENERIC_SPEAKER = re.compile(r"^(?P<author>[A-Za-z][\w .'-]{0,40}):\s(?P<text>.+)$")

WORD = re.compile(r"[A-Za-z']+")


def read_files(paths):
    blobs = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            sys.stderr.write(f"corpus: skipping missing file: {p}\n")
            continue
        blobs.append((str(path), path.read_text(encoding="utf-8", errors="replace")))
    return blobs


def try_json_chat(text):
    """Parse a JSON array of message objects into samples. Returns list or None."""
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return None
    if not isinstance(data, list):
        return None
    samples = []
    for item in data:
        if not isinstance(item, dict):
            return None
        author = item.get("author") or item.get("role") or item.get("from") or item.get("name")
        body = item.get("text") or item.get("content") or item.get("message") or item.get("body")
        ts = item.get("ts") or item.get("timestamp") or item.get("date") or item.get("time")
        if body is None:
            continue
        samples.append({"author": _s(author), "ts": _s(ts), "text": str(body).strip()})
    return samples or None


def parse_chat_lines(text):
    """Parse line-oriented chat exports. Continuation lines attach to the prior message."""
    samples = []
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        m = WHATSAPP_DASH.match(line) or WHATSAPP_BRACKET.match(line) or GENERIC_SPEAKER.match(line)
        if m:
            gd = m.groupdict()
            samples.append(
                {
                    "author": _s(gd.get("author")),
                    "ts": _s(gd.get("ts")),
                    "text": gd.get("text", "").strip(),
                }
            )
        elif samples:
            samples[-1]["text"] += "\n" + line.strip()
        # a non-matching first line with no prior sample is ignored as a header
    return samples


def parse_prose(text):
    """Split prose into paragraph samples (blank-line separated)."""
    chunks = re.split(r"\n\s*\n", text)
    return [{"author": None, "ts": None, "text": c.strip()} for c in chunks if c.strip()]


def looks_like_chat(text):
    lines = [l for l in text.splitlines() if l.strip()][:40]
    if not lines:
        return False
    hits = sum(
        1
        for l in lines
        if WHATSAPP_DASH.match(l) or WHATSAPP_BRACKET.match(l) or GENERIC_SPEAKER.match(l)
    )
    return hits >= max(2, len(lines) // 4)


def _s(v):
    if v is None:
        return None
    v = str(v).strip()
    return v or None


def compute_stats(samples):
    by_author = Counter()
    lengths = []
    vocab = Counter()
    total_words = 0
    for s in samples:
        by_author[s["author"] or "(unknown)"] += 1
        words = WORD.findall(s["text"].lower())
        lengths.append(len(words))
        total_words += len(words)
        vocab.update(words)
    n = len(samples)
    avg_len = round(total_words / n, 1) if n else 0
    ttr = round(len(vocab) / total_words, 3) if total_words else 0.0
    return {
        "samples": n,
        "authors": dict(by_author),
        "total_words": total_words,
        "avg_words_per_sample": avg_len,
        "type_token_ratio": ttr,
        "vocabulary_size": len(vocab),
        "top_words": vocab.most_common(20),
    }


def main():
    ap = argparse.ArgumentParser(description="Normalize personal material into a common shape.")
    ap.add_argument("files", nargs="+", help="input files (prose, chat export, or JSON)")
    ap.add_argument("--kind", choices=["auto", "prose", "chat"], default="auto")
    ap.add_argument("--author", help="filter samples to this author (substring match, case-insensitive)")
    ap.add_argument("--out", help="write JSON here instead of stdout")
    args = ap.parse_args()

    blobs = read_files(args.files)
    if not blobs:
        sys.stderr.write("corpus: no readable input files\n")
        return 1

    combined = "\n".join(b for _, b in blobs)
    kind = args.kind
    if kind == "auto":
        kind = "chat" if looks_like_chat(combined) else "prose"

    samples = []
    if kind == "chat":
        for src, text in blobs:
            js = try_json_chat(text)
            samples.extend(js if js is not None else parse_chat_lines(text))
    else:
        for src, text in blobs:
            samples.extend(parse_prose(text))

    if args.author:
        needle = args.author.lower()
        samples = [s for s in samples if s["author"] and needle in s["author"].lower()]

    doc = {
        "sources": [src for src, _ in blobs],
        "kind": kind,
        "samples": samples,
        "stats": compute_stats(samples),
    }

    out = json.dumps(doc, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(out + "\n", encoding="utf-8")
        sys.stderr.write(f"corpus: wrote {len(samples)} samples to {args.out}\n")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
