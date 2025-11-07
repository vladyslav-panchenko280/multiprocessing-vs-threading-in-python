from __future__ import annotations

import argparse
from pathlib import Path
from typing import List
import time

from threading_search import process_files_in_threads
from multiprocessing_search import process_files_in_processes


def _list_log_files(directory: Path | str, glob_pattern: str = "*.log") -> List[Path]:
    base = Path(directory)
    return [p for p in base.rglob(glob_pattern) if p.is_file()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Parallel processing of text files to search for specified keywords"
        )
    )
    parser.add_argument(
        "--dir",
        dest="directory",
        default=str(Path(__file__).parent / "logs"),
        help="Path to the directory with log files (default: ./logs)",
    )
    parser.add_argument(
        "--keywords",
        dest="keywords",
        nargs="+",
        required=True,
        help="List of keywords to search for",
    )
    parser.add_argument(
        "--workers",
        dest="workers",
        type=int,
        default=None,
        help="Number of workers (default: determined automatically)",
    )
    parser.add_argument(
        "--case-sensitive",
        dest="case_sensitive",
        action="store_true",
        help="Make the search case-sensitive",
    )
    parser.add_argument(
        "--sample",
        dest="sample",
        type=int,
        default=0,
        help="Limit the number of files for a quick check (0 = no limit)",
    )
    parser.add_argument(
        "--glob",
        dest="glob",
        default="*.log",
        help="File pattern to search for (default: *.log)",
    )
    parser.add_argument(
        "--mode",
        dest="mode",
        choices=["threading", "multiprocessing"],
        default="threading",
        help="Parallel processing mode: threading or multiprocessing (default: threading)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = Path(args.directory).resolve()

    if args.mode == "threading":
        process_files = process_files_in_threads
        worker_type = "threads"
    else:
        process_files = process_files_in_processes
        worker_type = "processes"

    files: List[Path] = _list_log_files(base_dir, args.glob)
    if args.sample and args.sample > 0:
        files = files[: args.sample]

    if not files:
        print("No files found. Check the path or the glob pattern.")
        return

    actual_workers = args.workers if args.workers else 4

    start_time = time.time()
    results = process_files(
        files,
        args.keywords,
        max_workers=actual_workers,
        case_sensitive=args.case_sensitive,
    )
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Found {len(files)} file(s) to analyze in directory: {base_dir}")
    print("Keywords:", ", ".join(args.keywords))
    print(f"Processing mode: {args.mode}")
    print(f"Number of workers ({worker_type}): {actual_workers}")
    print("Case-sensitive" if args.case_sensitive else "Case-insensitive")
    print(f"Execution time: {elapsed_time:.4f} seconds")

    print("\nSearch results (keyword -> list of files):")
    for keyword in args.keywords:
        file_list = results.get(keyword, [])
        print(f"\n'{keyword}': found in {len(file_list)} file(s)")
        if file_list:
            for file_path in file_list[:10]:  # Show first 10 files
                print(f"  - {file_path}")
            if len(file_list) > 10:
                print(f"  ... and {len(file_list) - 10} more file(s)")


if __name__ == "__main__":
    main()
