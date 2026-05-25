"""Generic sorting algorithms.

All algorithms have signature `(items, key) -> list[T]` and return a new list,
leaving the input untouched. `key` extracts an integer-comparable ordering value
from each element.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Protocol, TypeVar

T = TypeVar("T")
KeyFunc = Callable[[T], int]


class SortAlgorithm(Protocol):
    def __call__(self, items: Sequence[T], key: KeyFunc[T]) -> list[T]: ...


def bubble_sort(items: Sequence[T], key: KeyFunc[T]) -> list[T]:
    result = list(items)
    n = len(result)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if key(result[j]) > key(result[j + 1]):
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def insertion_sort(items: Sequence[T], key: KeyFunc[T]) -> list[T]:
    result = list(items)
    for i in range(1, len(result)):
        current = result[i]
        current_key = key(current)
        j = i - 1
        while j >= 0 and key(result[j]) > current_key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result


def selection_sort(items: Sequence[T], key: KeyFunc[T]) -> list[T]:
    result = list(items)
    n = len(result)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if key(result[j]) < key(result[min_idx]):
                min_idx = j
        if min_idx != i:
            result[i], result[min_idx] = result[min_idx], result[i]
    return result


def quick_sort(items: Sequence[T], key: KeyFunc[T]) -> list[T]:
    result = list(items)
    _quick_sort_inplace(result, 0, len(result) - 1, key)
    return result


def _quick_sort_inplace(arr: list[T], low: int, high: int, key: KeyFunc[T]) -> None:
    if low >= high:
        return
    # Median-of-three pivot to avoid worst-case on sorted input.
    mid = (low + high) // 2
    pivot_idx = _median_of_three(arr, low, mid, high, key)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    pivot = key(arr[high])
    i = low - 1
    for j in range(low, high):
        if key(arr[j]) <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    p = i + 1
    _quick_sort_inplace(arr, low, p - 1, key)
    _quick_sort_inplace(arr, p + 1, high, key)


def _median_of_three(arr: list[T], a: int, b: int, c: int, key: KeyFunc[T]) -> int:
    ka, kb, kc = key(arr[a]), key(arr[b]), key(arr[c])
    if (ka <= kb <= kc) or (kc <= kb <= ka):
        return b
    if (kb <= ka <= kc) or (kc <= ka <= kb):
        return a
    return c


def merge_sort(items: Sequence[T], key: KeyFunc[T]) -> list[T]:
    arr = list(items)
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return _merge(left, right, key)


def _merge(left: list[T], right: list[T], key: KeyFunc[T]) -> list[T]:
    merged: list[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def bucket_sort(items: Sequence[T], key: KeyFunc[T]) -> list[T]:
    """Stable bucket sort. Works for any non-negative integer key.

    Bucket count is derived from the data, so it isn't tied to a fixed domain.
    """
    arr = list(items)
    if not arr:
        return arr
    keys = [key(x) for x in arr]
    min_k, max_k = min(keys), max(keys)
    if min_k < 0:
        raise ValueError("bucket_sort requires non-negative keys")
    buckets: list[list[T]] = [[] for _ in range(max_k - min_k + 1)]
    for item, k in zip(arr, keys, strict=True):
        buckets[k - min_k].append(item)
    return [item for bucket in buckets for item in bucket]


def timsort(items: Sequence[T], key: KeyFunc[T]) -> list[T]:
    """Python's built-in Timsort via `sorted`. Included for benchmarking."""
    return sorted(items, key=key)


ALGORITHMS: dict[str, SortAlgorithm] = {
    "quick": quick_sort,
    "bubble": bubble_sort,
    "bucket": bucket_sort,
    "merge": merge_sort,
    "insertion": insertion_sort,
    "selection": selection_sort,
    "timsort": timsort,
}
