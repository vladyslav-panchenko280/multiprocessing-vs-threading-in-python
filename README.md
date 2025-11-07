# Parallel Processing of Log Files

An CLI application for searching keywords in log files using multithreading and multiprocessing approaches. The tool lets you benchmark both strategies on the same dataset to understand how workload type and hardware affect throughput.

## Threading vs Multiprocessing

- **Threading** shares memory inside one process. It works best for I/O-bound tasks (reading files, waiting on network or disk), has lower startup overhead, and makes sharing data between workers straightforward.
- **Multiprocessing** runs each worker in a separate process. It avoids the Global Interpreter Lock (GIL), so it's preferred for CPU-bound workloads or heavy text processing, but comes with higher startup costs and additional inter-process communication overhead.
- Use `--mode threading` to quickly scan large collections of log files stored on disk or network shares.
- Use `--mode multiprocessing` when keyword matching involves CPU-heavy parsing, or when you want better isolation between workers.

## Usage

```bash
python main.py --keywords ERROR WARNING --workers 4
```

## Parameters

- `--keywords` — keywords to search for (required)
- `--workers` — number of workers (default: 4)
- `--mode` — mode: `threading` or `multiprocessing` (default: threading)
- `--dir` — directory with files (default: ./logs)
- `--sample` — limit the number of files for testing
- `--case-sensitive` — enable case-sensitive search
- `--glob` — file pattern (default: *.log)

## Examples

```bash
# Threading with 4 threads
python main.py --keywords Macintosh Windows --workers 4 --mode threading

# Multiprocessing with 8 processes
python main.py --keywords ERROR WARN --workers 8 --mode multiprocessing

# Process 50 files for a quick test
python main.py --keywords Linux --sample 50
```

## Result

The application returns a dictionary where each key is a keyword and the value is a list of files where it was found.
The execution time is displayed to compare the performance of different approaches.

