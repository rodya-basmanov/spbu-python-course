import copy
from copy import deepcopy
import inspect
from typing import Callable, Any


def curry_explicit(func: Callable, arity: int) -> Callable:
    """
    Turning a function from several parameters into a function from one parameter that returns a function from the rest of the parameters.
    Args:
        func: The curried function
        arity: The number of arguments
    Returns:
        A curried version of the input function. If arity is 0, returns
        a function that takes no arguments. Otherwise, returns a function
        that takes one argument and returns another function until all
        arguments are collected.
    Raises:
        ValueError: If arity is negative or too many arguments are passed
        during function application
    """

    if arity < 0:
        raise ValueError("Negative arity is not possible")

    if arity == 0:

        def zero_arity() -> Any:
            return func()

        return zero_arity

    def curry(*args):
        if len(args) == arity:
            return func(*args)
        elif len(args) > arity:
            raise ValueError("Too many arguments passed")
        else:

            def next_func(next_arg):
                return curry(*args, next_arg)

            return next_func

    return curry


def uncurry_explicit(curry_func: Callable, arity: int) -> Callable:
    """
    Convert a curried function back to its normal form with specified arity.
    Args:
        curry_func: The curried function to be uncurried
        arity: The number of arguments
    Returns:
        An uncurried version of the input function. If arity is 0, returns
        a function that takes no arguments. Otherwise, returns a function
        that takes all arguments at once.
    Raises: ValueError: If arity is negative or the number of arguments passed
    doesn't match the specified arity
    """
    if arity < 0:
        raise ValueError("Negative arity is not possible")

    if arity == 0:

        def zero_arity() -> Any:
            return curry_func()

        return zero_arity

    def uncurried(*args):
        if len(args) != arity:
            raise ValueError("The number of arguments passed does not match")
        res = curry_func
        for arg in args:
            res = res(arg)
        return res

    return uncurried


# ---------------------------Smart args Decorator-----------------------------#


class Isolated:
    pass


class Evaluated:
    def __init__(self, func: Callable):
        assert callable(func), "Evaluated expects a callable"
        self.func = func


def smart_args(func):
    sig = inspect.signature(func)

    for name, param in sig.parameters.items():
        assert (
            param.kind == inspect.Parameter.KEYWORD_ONLY
        ), "smart_args supports named arguments only"

    def wrapper(**kwargs):
        for name, param in sig.parameters.items():
            default = param.default

            assert not (
                isinstance(default, Isolated) and isinstance(default, Evaluated)
            ), "You cant use Isolated and Evaluated together in an argument."

            if isinstance(default, Evaluated) and name not in kwargs:
                kwargs[name] = default.func()
            if isinstance(default, Isolated) and name in kwargs:
                kwargs[name] = copy.deepcopy(kwargs[name])
            if isinstance(default, Isolated) and name not in kwargs:
                raise TypeError("Argument marked as Isolated must be provided")

        return func(**kwargs)

    return wrapper
