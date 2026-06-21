#!/usr/bin/env python3
"""draw.py - an honest randomizer: draw K items uniformly from a collection.

Owned by `augury`. This is the deck-shuffler that makes the collision honest:
items are drawn uniformly at random, with no model in the loop choosing what
"should" come up. The model only reads the draw afterward and finds the thread.

By default the draw is seeded by the date, so a given day yields the same draw
(a stable daily ritual) but different days differ. Pass --seed to override.

Input: a collection file, either newline-delimited items or a JSON array of
strings/objects. Objects are rendered by their "title"/"name"/"text" field.

Usage:
  draw.py COLLECTION [--k 3] [--seed STR] [--date YYYY-MM-DD]
"""

import argparse
import datetime as dt
import json
import random
import sys
from pathlib import Path


def load_items(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    text_stripped = text.lstrip()
    if text_stripped.startswith("[") or text_stripped.startswith("{"):
        try:
            data = json.loads(text)
        except ValueError:
            data = None
        if isinstance(data, list):
            items = []
            for it in data:
                if isinstance(it, str):
                    items.append(it.strip())
                elif isinstance(it, dict):
                    label = (
                        it.get("title")
                        or it.get("name")
                        or it.get("text")
                        or it.get("note")
                        or json.dumps(it, ensure_ascii=False)
                    )
                    items.append(str(label).strip())
            return [i for i in items if i]
    # fall back to newline-delimited
    return [line.strip() for line in text.splitlines() if line.strip()]


def main():
    ap = argparse.ArgumentParser(description="Draw K items uniformly from a collection.")
    ap.add_argument("collection", help="newline-delimited or JSON-array collection file")
    ap.add_argument("--k", type=int, default=3, help="how many to draw (default 3)")
    ap.add_argument("--seed", help="explicit seed (overrides date seeding)")
    ap.add_argument("--date", help="date YYYY-MM-DD for daily-stable seeding (default today)")
    args = ap.parse_args()

    items = load_items(args.collection)
    if not items:
        sys.stderr.write("draw: collection is empty or unreadable\n")
        return 1

    k = min(args.k, len(items))
    seed = args.seed if args.seed is not None else (args.date or dt.date.today().isoformat())
    rng = random.Random(seed)
    drawn = rng.sample(items, k)

    out = {
        "seed": seed,
        "k": k,
        "collection_size": len(items),
        "draw": drawn,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
