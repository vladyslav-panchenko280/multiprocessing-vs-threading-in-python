from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, List, Set
import re


def _check_keywords_in_text(
    text: str, keywords: Set[str], case_sensitive: bool
) -> Set[str]:
    """Check which keywords are found in the text."""
    if not keywords:
        return set()

    flags = 0 if case_sensitive else re.IGNORECASE
    found_keywords = set()

    for kw in keywords:
        escaped = re.escape(kw)
        pattern = re.compile(escaped, flags)
        if pattern.search(text):
            found_keywords.add(kw)

    return found_keywords


def find_keywords_in_file(
    file_path: Path | str, keywords: Iterable[str], case_sensitive: bool = False
) -> Set[str]:
    """Returns set of keywords found in the file."""
    path = Path(file_path)
    keyset: Set[str] = set(keywords)
    found: Set[str] = set()

    if not path.is_file():
        return found

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            try:
                for line in f:
                    line_found = _check_keywords_in_text(line, keyset, case_sensitive)
                    found.update(line_found)
                    if found == keyset:
                        break
            except Exception:
                pass
    except (OSError, IOError, PermissionError, Exception):
        pass

    return found


def process_files_in_threads(
    file_paths: Iterable[Path | str],
    keywords: Iterable[str],
    max_workers: int | None = None,
    case_sensitive: bool = False,
) -> Dict[str, List[Path]]:
    """
    Returns dictionary: keyword -> list of file paths where keyword was found.
    """
    paths: List[Path] = [Path(p) for p in file_paths]
    keyset: Set[str] = set(keywords)

    result: Dict[str, List[Path]] = {k: [] for k in keyset}

    if not paths or not keyset:
        return result

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {
            executor.submit(find_keywords_in_file, p, keyset, case_sensitive): p
            for p in paths
        }
        for future in as_completed(future_to_path):
            p = future_to_path[future]
            try:
                found_keywords = future.result()
            except Exception:
                found_keywords = set()

            for kw in found_keywords:
                result[kw].append(p)

    return result
