from __future__ import annotations

import multiprocessing as mp
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple
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


def find_keywords_in_file_wrapper(
    args: Tuple[Path, Set[str], bool],
) -> Tuple[Path, Set[str]]:
    """
    Wrapper function for multiprocessing Pool.
    Pool internally uses Queue for task distribution and result collection.
    """
    file_path, keywords, case_sensitive = args
    found: Set[str] = set()

    if not file_path.is_file():
        return (file_path, found)

    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            try:
                for line in f:
                    line_found = _check_keywords_in_text(line, keywords, case_sensitive)
                    found.update(line_found)
                    if found == keywords:
                        break
            except Exception:
                pass
    except (OSError, IOError, PermissionError, Exception):
        pass

    return (file_path, found)


def process_files_in_processes(
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

    args_list = [(path, keyset, case_sensitive) for path in paths]

    with mp.Pool(processes=max_workers) as pool:
        results = pool.map(find_keywords_in_file_wrapper, args_list)

    for file_path, found_keywords in results:
        for kw in found_keywords:
            result[kw].append(file_path)

    return result
