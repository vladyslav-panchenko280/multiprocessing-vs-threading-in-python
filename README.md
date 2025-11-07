# Parallel Processing of Text Files

An application for searching keywords in text files using multithreading and multiprocessing approaches.

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

