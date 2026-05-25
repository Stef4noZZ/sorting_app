# Sorting App

CLI T-shirt builder that demonstrates classical sorting algorithms and the
Strategy design pattern (for payment methods). This started as a junior
practice project and has been refactored into a small, well-tested Python
package.

## Features

- Build a T-shirt by picking a color, size, and fabric — each attribute
  contributes to the price.
- Generate a random collection of T-shirts.
- Sort with any of seven algorithms: quick, bubble, bucket, merge, insertion,
  selection, and Python's built-in Timsort.
- Sort by a single key (color / size / fabric) or by multiple keys at once.
- Sort ascending or descending.
- Benchmark all algorithms against the same input to compare runtimes.
- Show collection statistics (count, total/avg/min/max price, attribute
  breakdown).
- Save / load collections to JSON.
- Checkout with one of three payment strategies (card, transfer, cash) —
  each strategy applies its own price adjustment.

## Project layout

```
sorting_app/
├── main.py                 # Thin entry point (works without install)
├── pyproject.toml          # Build / tooling config (ruff, mypy, pytest)
├── requirements-dev.txt    # Dev dependencies
├── data/                   # Saved collections (gitignored)
├── src/sorting_app/
│   ├── app.py              # CLI orchestrator
│   ├── stats.py            # Collection statistics
│   ├── models/             # Domain entities (TShirt, Color, Size, Fabric)
│   ├── sorting/            # Algorithms, service, benchmark
│   ├── payment/            # Strategy pattern: card / transfer / cash
│   ├── persistence/        # JSON repository
│   └── ui/                 # Colors, prompts, menus
└── tests/                  # Pytest suite
```

## Requirements

- Python 3.10+

## Getting started

```bash
# 1. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate

# 2. Install the package + dev dependencies
pip install -e ".[dev]"

# 3. Run the app
sorting-app                       # via the console script
# or
python main.py                    # without installing
```

## Running the tests

```bash
pytest                            # all 51 tests
pytest --cov=sorting_app          # with coverage
```

## Code quality

```bash
ruff check .                      # lint
mypy                              # type-check (strict mode)
```

## Design notes

- **Domain layer** (`models/`) is pure data — `TShirt` is a frozen dataclass
  and attributes are enums carrying both an ordinal (for sorting) and a
  price (for checkout). No I/O, no UI concerns.
- **Sorting algorithms** (`sorting/algorithms.py`) are generic: each accepts
  any sequence and a `key` callable. They return a new list and never mutate
  the input. `SortService` is the high-level façade the CLI talks to.
- **Strategy pattern** (`payment/strategies.py`) — each payment method is a
  subclass of `PaymentStrategy`. Adding a new method is a one-class change.
- **UI layer** (`ui/`) is the only module that talks to `stdin`/`stdout`.
  The rest of the codebase is decoupled from terminal I/O, which is why
  every non-UI module is easy to unit-test.
- **Persistence** is a thin JSON repository — swap in a database by
  implementing the same `save` / `load` / `list_collections` surface.

## License

MIT
