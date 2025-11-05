# Паралельна обробка текстових файлів

Програма для пошуку ключових слів у текстових файлах з використанням багатопотокового та багатопроцесорного підходів.

## Використання

```bash
python main.py --keywords ERROR WARNING --workers 4
```

## Параметри

- `--keywords` — ключові слова для пошуку (обов'язково)
- `--workers` — кількість воркерів (за замовчуванням: 4)
- `--mode` — режим: `threading` або `multiprocessing` (за замовчуванням: threading)
- `--dir` — директорія з файлами (за замовчуванням: ./logs)
- `--sample` — обмежити кількість файлів для тестування
- `--case-sensitive` — враховувати регістр
- `--glob` — шаблон файлів (за замовчуванням: *.log)

## Приклади

```bash
# Threading з 4 потоками
python main.py --keywords Macintosh Windows --workers 4 --mode threading

# Multiprocessing з 8 процесами
python main.py --keywords ERROR WARN --workers 8 --mode multiprocessing

# Обробка 50 файлів для швидкого тесту
python main.py --keywords Linux --sample 50
```

## Результат

Програма повертає словник, де ключ — ключове слово, значення — список файлів, де воно знайдено.
Виводиться час виконання для порівняння продуктивності різних підходів.

