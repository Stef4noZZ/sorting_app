"""Interactive CLI entry point.

The app is intentionally thin — it orchestrates the domain modules and handles
user I/O, but contains no business logic of its own.
"""

from __future__ import annotations

import sys
from pathlib import Path

from sorting_app.models import Color as TColor
from sorting_app.models import Fabric, Size, SortKey, TShirt
from sorting_app.payment import PaymentMethod, get_strategy
from sorting_app.persistence import TShirtRepository
from sorting_app.sorting import (
    ALGORITHMS,
    SortDirection,
    SortService,
    benchmark,
)
from sorting_app.stats import compute_stats
from sorting_app.ui import (
    choose_enum,
    choose_from_options,
    prompt_int,
    show_error,
    show_info,
    show_success,
    show_warning,
)


class App:
    def __init__(self, repository: TShirtRepository | None = None) -> None:
        self.my_tshirts: list[TShirt] = []
        self.random_tshirts: list[TShirt] = []
        self.repo = repository or TShirtRepository()

    def run(self) -> None:
        show_info("Welcome to the Sorting App — T-shirt edition")
        while True:
            choice = choose_from_options(
                "MAIN MENU",
                [
                    ("my", "My T-Shirts"),
                    ("random", "Random T-Shirts"),
                    ("load", "Load saved collection"),
                    ("exit", "Exit"),
                ],
            )
            match choice:
                case "my":
                    self._my_tshirt_menu()
                case "random":
                    self._random_tshirt_menu()
                case "load":
                    self._load_menu()
                case "exit":
                    show_info("Bye!")
                    return

    # ---- My T-Shirts ----------------------------------------------------

    def _my_tshirt_menu(self) -> None:
        while True:
            choice = choose_from_options(
                "MY T-SHIRTS",
                [
                    ("create", "Create a T-Shirt"),
                    ("view", "View list"),
                    ("pay", "Checkout"),
                    ("save", "Save list"),
                ],
                allow_back=True,
            )
            match choice:
                case None:
                    return
                case "create":
                    tshirt = self._create_tshirt_interactive()
                    self.my_tshirts.append(tshirt)
                    show_success(f"OK, added: {tshirt}")
                case "view":
                    self._display_collection(self.my_tshirts)
                case "pay":
                    self._checkout(self.my_tshirts)
                case "save":
                    self._save_collection(self.my_tshirts)

    def _create_tshirt_interactive(self) -> TShirt:
        color = choose_enum("PICK A COLOR", TColor)
        size = choose_enum("PICK A SIZE", Size)
        fabric = choose_enum("PICK A FABRIC", Fabric)
        return TShirt(color=color, size=size, fabric=fabric)

    # ---- Random T-Shirts ------------------------------------------------

    def _random_tshirt_menu(self) -> None:
        while True:
            choice = choose_from_options(
                "RANDOM T-SHIRTS",
                [
                    ("create", "Generate random T-Shirts"),
                    ("sort", "Sort / view list"),
                    ("stats", "Show statistics"),
                    ("bench", "Benchmark algorithms"),
                    ("pay", "Checkout"),
                    ("save", "Save list"),
                ],
                allow_back=True,
            )
            match choice:
                case None:
                    return
                case "create":
                    self._generate_random()
                case "sort":
                    self._sort_menu()
                case "stats":
                    self._show_stats(self.random_tshirts)
                case "bench":
                    self._benchmark()
                case "pay":
                    self._checkout(self.random_tshirts)
                case "save":
                    self._save_collection(self.random_tshirts)

    def _generate_random(self) -> None:
        max_combos = len(TColor) * len(Size) * len(Fabric)
        count = prompt_int(
            f"How many random T-Shirts? (1-{max_combos}) > ",
            minimum=1,
            maximum=max_combos,
        )
        self.random_tshirts = [TShirt.random() for _ in range(count)]
        show_success(f"OK, generated {count} random T-Shirts")

    # ---- Sorting --------------------------------------------------------

    def _sort_menu(self) -> None:
        while True:
            choice = choose_from_options(
                "SORTING MENU",
                [
                    ("single", "Single-key sort"),
                    ("multi", "Multi-key sort (color → size → fabric)"),
                    ("view", "View list"),
                ],
                allow_back=True,
            )
            match choice:
                case None:
                    return
                case "single":
                    self._single_sort()
                case "multi":
                    self._multi_sort()
                case "view":
                    self._display_collection(self.random_tshirts)

    def _single_sort(self) -> None:
        if not self.random_tshirts:
            show_warning(">> list is empty — generate some random T-shirts first")
            return
        algo = choose_from_options(
            "PICK ALGORITHM",
            [(name, name.capitalize()) for name in ALGORITHMS],
        )
        assert algo is not None
        key_name = choose_from_options(
            "SORT BY",
            [(k.value, k.value.capitalize()) for k in SortKey],
        )
        assert key_name is not None
        direction = self._choose_direction()
        self.random_tshirts = SortService.sort(
            self.random_tshirts,
            algorithm=algo,
            key=SortKey(key_name),
            direction=direction,
        )
        show_success(f"OK, sorted by {key_name} ({direction.value}) using {algo}")

    def _multi_sort(self) -> None:
        if not self.random_tshirts:
            show_warning(">> list is empty — generate some random T-shirts first")
            return
        direction = self._choose_direction()
        self.random_tshirts = SortService.multi_sort(
            self.random_tshirts,
            keys=[SortKey.COLOR, SortKey.SIZE, SortKey.FABRIC],
            direction=direction,
        )
        show_success(f"OK, multi-sorted ({direction.value})")

    def _choose_direction(self) -> SortDirection:
        choice = choose_from_options(
            "DIRECTION",
            [
                (SortDirection.ASCENDING.value, "Ascending"),
                (SortDirection.DESCENDING.value, "Descending"),
            ],
        )
        assert choice is not None
        return SortDirection(choice)

    # ---- Benchmark ------------------------------------------------------

    def _benchmark(self) -> None:
        if not self.random_tshirts:
            show_warning(">> list is empty — generate some random T-shirts first")
            return
        key_name = choose_from_options(
            "BENCHMARK SORT KEY",
            [(k.value, k.value.capitalize()) for k in SortKey],
        )
        assert key_name is not None
        results = benchmark(self.random_tshirts, SortKey(key_name))
        show_info(f"\nBenchmark on {results[0].items} items, key={key_name}")
        print(f"  {'algorithm':<12} {'elapsed (ms)':>14}")
        print(f"  {'-' * 12} {'-' * 14}")
        for r in results:
            print(f"  {r.algorithm:<12} {r.elapsed_ms:>14.3f}")

    # ---- Payments -------------------------------------------------------

    def _checkout(self, items: list[TShirt]) -> None:
        if not items:
            show_warning(">> list is empty — nothing to charge")
            return
        method_choice = choose_from_options(
            "CHOOSE PAYMENT METHOD",
            [(m.value, m.value.capitalize()) for m in PaymentMethod],
            allow_back=True,
        )
        if method_choice is None:
            return
        method = PaymentMethod(method_choice)
        strategy = get_strategy(method)
        show_info(f"\nFinal prices with {strategy.label}:")
        total = 0.0
        for t in items:
            final = strategy.charge(t.base_price)
            total += final
            print(f"  {t.color.name:<7} {t.size.name:<5} {t.fabric.name:<10} -> {final:.2f}€")
        show_success(f"Total: {total:.2f}€")

    # ---- Stats / view ---------------------------------------------------

    def _show_stats(self, items: list[TShirt]) -> None:
        stats = compute_stats(items)
        if stats is None:
            show_warning(">> list is empty")
            return
        show_info("\nStatistics")
        print(f"  count:     {stats.count}")
        print(f"  total:     {stats.total_price:.2f}€")
        print(f"  min:       {stats.min_price:.2f}€")
        print(f"  max:       {stats.max_price:.2f}€")
        print(f"  avg:       {stats.avg_price:.2f}€")
        print(f"  by color:  {stats.by_color}")
        print(f"  by size:   {stats.by_size}")
        print(f"  by fabric: {stats.by_fabric}")

    def _display_collection(self, items: list[TShirt]) -> None:
        if not items:
            show_warning(">> list is empty")
            return
        for i, t in enumerate(items, start=1):
            print(f"  {i:>3}. {t}")

    # ---- Persistence ----------------------------------------------------

    def _save_collection(self, items: list[TShirt]) -> None:
        if not items:
            show_warning(">> nothing to save")
            return
        name = input("Save as (no extension): ").strip()
        if not name:
            show_warning(">> empty name, aborting")
            return
        path = self.repo.save(name, items)
        show_success(f"Saved {len(items)} items to {path}")

    def _load_menu(self) -> None:
        collections = self.repo.list_collections()
        if not collections:
            show_warning(">> no saved collections found")
            return
        options = [(name, name) for name in collections]
        chosen = choose_from_options("LOAD COLLECTION", options, allow_back=True)
        if chosen is None:
            return
        try:
            loaded = self.repo.load(chosen)
        except (FileNotFoundError, KeyError, ValueError) as exc:
            show_error(f">> failed to load: {exc}")
            return
        self.random_tshirts = loaded
        show_success(f"Loaded {len(loaded)} items into the random list")


def main(argv: list[str] | None = None) -> int:
    _ = argv  # reserved for future flags
    try:
        App(TShirtRepository(Path("data"))).run()
    except (KeyboardInterrupt, EOFError):
        print()
        show_info("Interrupted — bye!")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
