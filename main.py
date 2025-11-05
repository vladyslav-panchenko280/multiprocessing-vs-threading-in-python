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
            "Паралельна обробка текстових файлів для пошуку визначених ключових слів"
        )
    )
    parser.add_argument(
        "--dir",
        dest="directory",
        default=str(Path(__file__).parent / "logs"),
        help="Шлях до каталогу з файлами журналів (за замовчуванням: ./logs)",
    )
    parser.add_argument(
        "--keywords",
        dest="keywords",
        nargs="+",
        required=True,
        help="Список ключових слів для пошуку",
    )
    parser.add_argument(
        "--workers",
        dest="workers",
        type=int,
        default=None,
        help="Кількість потоків (за замовчуванням: визначається автоматично)",
    )
    parser.add_argument(
        "--case-sensitive",
        dest="case_sensitive",
        action="store_true",
        help="Враховувати регістр під час пошуку",
    )
    parser.add_argument(
        "--sample",
        dest="sample",
        type=int,
        default=0,
        help="Обмежити кількість файлів для швидкої перевірки (0 = без обмежень)",
    )
    parser.add_argument(
        "--glob",
        dest="glob",
        default="*.log",
        help="Шаблон файлів для пошуку (за замовчуванням: *.log)",
    )
    parser.add_argument(
        "--mode",
        dest="mode",
        choices=["threading", "multiprocessing"],
        default="threading",
        help="Режим паралельної обробки: threading або multiprocessing (за замовчуванням: threading)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = Path(args.directory).resolve()

    if args.mode == "threading":
        process_files = process_files_in_threads
        worker_type = "потоків (threads)"
    else:
        process_files = process_files_in_processes
        worker_type = "процесів (processes)"

    files: List[Path] = _list_log_files(base_dir, args.glob)
    if args.sample and args.sample > 0:
        files = files[: args.sample]

    if not files:
        print("Файли не знайдено. Перевірте шлях або шаблон glob.")
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

    print(f"Знайдено {len(files)} файл(и/ів) для аналізу у каталозі: {base_dir}")
    print("Ключові слова:", ", ".join(args.keywords))
    print(f"Режим обробки: {args.mode}")
    print(f"Кількість воркерів ({worker_type}): {actual_workers}")
    print("Регістр чутливий" if args.case_sensitive else "Без врахування регістру")
    print(f"Час виконання: {elapsed_time:.4f} секунд")

    print("\nРезультати пошуку (ключове слово -> список файлів):")
    for keyword in args.keywords:
        file_list = results.get(keyword, [])
        print(f"\n'{keyword}': знайдено у {len(file_list)} файл(ах)")
        if file_list:
            for file_path in file_list[:10]:  # Show first 10 files
                print(f"  - {file_path}")
            if len(file_list) > 10:
                print(f"  ... та ще {len(file_list) - 10} файл(ів)")


if __name__ == "__main__":
    main()


