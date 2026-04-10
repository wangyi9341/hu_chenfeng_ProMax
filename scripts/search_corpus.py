#!/usr/bin/env python3
"""
Search the local Hu Chenfeng transcript corpus with simple keyword scoring.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

DEFAULT_ROOT = Path(os.environ.get("HUCHENFENG_CORPUS", "HuChenFeng-main"))
SKIP_FILES = {
    "README.md",
    "SUMMARY.md",
    "Preface.md",
    "Acknowledgements.md",
    "videos.md",
    "LICENSE",
}


@dataclass
class Hit:
    path: Path
    score: int
    snippets: list[str]
    date_value: date | None
    matched_terms: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search the Hu Chenfeng transcript corpus."
    )
    parser.add_argument("query", help="Keyword phrase or space-separated anchor terms.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--max-hits", type=int, default=6)
    parser.add_argument("--context", type=int, default=70)
    parser.add_argument("--from-date", dest="from_date")
    parser.add_argument("--to-date", dest="to_date")
    parser.add_argument(
        "--match-mode",
        choices=("any", "all"),
        default="any",
        help="Require any term or all terms to appear in a file.",
    )
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def extract_file_date(path: Path) -> date | None:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None


def build_terms(query: str) -> list[str]:
    split_terms = [part.strip() for part in re.split(r"\s+", query) if part.strip()]
    raw_terms = split_terms[:]
    if len(split_terms) <= 1:
        raw_terms.insert(0, query.strip())
    unique_terms: list[str] = []
    for term in raw_terms:
        if len(term) < 2:
            continue
        if term not in unique_terms:
            unique_terms.append(term)
    return unique_terms


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.md")):
        if path.name in SKIP_FILES:
            continue
        yield path


def score_text(
    text: str, terms: list[str]
) -> tuple[int, list[tuple[int, int, str]], list[str]]:
    lowered = text.lower()
    score = 0
    matches: list[tuple[int, int, str]] = []
    matched_terms: list[str] = []
    for term in terms:
        term_lower = term.lower()
        start = 0
        local_hits = 0
        while True:
            index = lowered.find(term_lower, start)
            if index == -1:
                break
            local_hits += 1
            matches.append((index, index + len(term), term))
            start = index + len(term)
        if local_hits:
            matched_terms.append(term)
            weight = 5 if term == terms[0] else 2
            score += local_hits * weight
    if matched_terms:
        score += len(matched_terms) * 3
    return score, matches, matched_terms


def merge_matches(matches: list[tuple[int, int, str]], gap: int = 24) -> list[tuple[int, int]]:
    if not matches:
        return []
    ordered = sorted((start, end) for start, end, _ in matches)
    merged: list[tuple[int, int]] = [ordered[0]]
    for start, end in ordered[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + gap:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def make_snippets(text: str, matches: list[tuple[int, int, str]], context: int) -> list[str]:
    snippets: list[str] = []
    for start, end in merge_matches(matches)[:3]:
        left = max(0, start - context)
        right = min(len(text), end + context)
        chunk = text[left:right].replace("\r", " ").replace("\n", " ")
        chunk = re.sub(r"\s+", " ", chunk).strip()
        snippets.append(chunk)
    return snippets


def search(
    root: Path,
    terms: list[str],
    from_date: date | None,
    to_date: date | None,
    max_hits: int,
    context: int,
    match_mode: str,
) -> list[Hit]:
    results: list[Hit] = []
    for path in iter_files(root):
        file_date = extract_file_date(path)
        if from_date and file_date and file_date < from_date:
            continue
        if to_date and file_date and file_date > to_date:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        score, matches, matched_terms = score_text(text, terms)
        if not score:
            continue
        if match_mode == "all" and len(matched_terms) != len(terms):
            continue
        snippets = make_snippets(text, matches, context)
        results.append(
            Hit(
                path=path,
                score=score,
                snippets=snippets,
                date_value=file_date,
                matched_terms=matched_terms,
            )
        )
    results.sort(
        key=lambda item: (
            item.score,
            item.date_value or date.min,
            item.path.name,
        ),
        reverse=True,
    )
    return results[:max_hits]


def serialize(hit: Hit) -> dict[str, object]:
    return {
        "path": str(hit.path),
        "date": hit.date_value.isoformat() if hit.date_value else None,
        "score": hit.score,
        "matched_terms": hit.matched_terms,
        "snippets": hit.snippets,
    }


def main() -> int:
    args = parse_args()
    root = args.root
    if not root.exists():
        raise SystemExit(f"Corpus root not found: {root}")
    terms = build_terms(args.query)
    if not terms:
        raise SystemExit("Query produced no usable terms.")
    hits = search(
        root=root,
        terms=terms,
        from_date=parse_date(args.from_date),
        to_date=parse_date(args.to_date),
        max_hits=args.max_hits,
        context=args.context,
        match_mode=args.match_mode,
    )
    if args.json:
        print(json.dumps([serialize(hit) for hit in hits], ensure_ascii=False, indent=2))
        return 0
    print(f"root: {root}")
    print(f"query: {args.query}")
    print(f"terms: {', '.join(terms)}")
    print(f"hits: {len(hits)}")
    for index, hit in enumerate(hits, start=1):
        date_label = hit.date_value.isoformat() if hit.date_value else "unknown-date"
        print("")
        print(f"[{index}] score={hit.score} date={date_label}")
        print(hit.path)
        print(f"matched_terms: {', '.join(hit.matched_terms)}")
        for snippet in hit.snippets:
            print(f"- {snippet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
