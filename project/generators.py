from typing import Iterable, Callable
from functools import reduce as functools_reduce


def data_generator(start: int, end: int, step: int = 1) -> Iterable[int]:
    """Generate sequence of numbers from start to end with step.

    Args:
        start (int): Starting value of the sequence.
        end (int): End value of the sequence (exclusive).
        step (int, optional): Step between values. Defaults to 1.

    Yields:
        int: Next number in the sequence.
    """
    current = start
    while current < end:
        yield current
        current += step


def map_gen(func: Callable, source: Iterable) -> Iterable:
    """Apply function to each element in the stream.

    Args:
        func (Callable): Function to apply to each element.
        source (Iterable): Input stream.

    Yields:
        Transformed elements.
    """
    for item in source:
        yield func(item)


def filter_gen(func: Callable, source: Iterable) -> Iterable:
    """Filter elements by predicate function.

    Args:
        func (Callable): Predicate function returning bool.
        source (Iterable): Input stream.

    Yields:
        Filtered elements that satisfy the predicate.
    """
    for item in source:
        if func(item):
            yield item


def zip_gen(source: Iterable, other: Iterable) -> Iterable:
    """Combine two streams into stream of tuples.

    Args:
        source (Iterable): First stream.
        other (Iterable): Second stream to zip with.

    Yields:
        tuple: Tuples of paired elements.
    """
    for a, b in zip(source, other):
        yield (a, b)


def apply_gen(func: Callable, source: Iterable) -> Iterable:
    """Apply custom function to the entire stream.

    Args:
        func (Callable): Function that takes iterable and returns iterable.
        source (Iterable): Input stream.

    Yields:
        Elements from the transformed stream.
    """
    for item in func(source):
        yield item


def reduce_gen(func: Callable, source: Iterable, initial=None):
    """Reduce elements to single value using binary function.

    Args:
        func (Callable): Binary function for reduction.
        source (Iterable): Input stream.
        initial (optional): Initial value for reduction. Defaults to None.

    Returns:
        Result of reduction.
    """
    if initial is None:
        return functools_reduce(func, source)
    return functools_reduce(func, source, initial)


def to_list(source: Iterable) -> list:
    """Collect all elements into list.

    Args:
        source (Iterable): Input stream.

    Returns:
        list: List containing all elements.
    """
    return list(source)


def to_set(source: Iterable) -> set:
    """Collect all elements into set.

    Args:
        source (Iterable): Input stream.

    Returns:
        set: Set containing all unique elements.
    """
    return set(source)


def count_gen(source: Iterable) -> int:
    """Count number of elements in the stream.

    Args:
        source (Iterable): Input stream.

    Returns:
        int: Total number of elements.
    """
    return sum(1 for _ in source)
