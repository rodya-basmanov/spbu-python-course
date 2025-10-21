from typing import Iterable, Callable, Any, Iterator
from functools import reduce


def data_generator(start: int, end: int, step: int = 1) -> Iterator[int]:
    """Generate sequence of numbers from start to end with step.

    Args:
        start: Starting value of the sequence
        end: End value of the sequence (exclusive)
        step: Step between values

    Yields:
        Next number in the sequence
    """
    current = start
    while current < end:
        yield current
        current += step


def pipeline(source: Iterable, *operations: Callable[[Iterable], Iterable]) -> Iterable:
    """Apply sequence of operations to data source sequentially.

    Args:
        source: Input data source
        *operations: Functions that take Iterable and return Iterable

    Returns:
        Result after applying all operations

    Example:
        >>> result = pipeline(
        ...     [1, 2, 3, 4, 5],
        ...     lambda x: map(lambda y: y * 2, x),
        ...     lambda x: filter(lambda y: y > 5, x)
        ... )
        >>> list(result)
        [6, 8, 10]
    """
    result = source
    for operation in operations:
        result = operation(result)
    return result


def apply_custom_operation(func: Callable[[Any], Any], source: Iterable) -> Iterable:
    """Apply custom function to stream (example of user-defined operation).

    Args:
        func: Custom transformation function
        source: Input stream

    Yields:
        Transformed elements
    """
    for item in source:
        yield func(item)
