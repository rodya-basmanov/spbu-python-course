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
        else:

            def next_func(next_arg, *extra_args):
                if extra_args:
                    raise ValueError("Too many arguments passed")
                return curry(*args, next_arg)

            return next_func

    def initial_func(arg, *extra_args):
        if extra_args:
            raise ValueError("Too many arguments passed")
        return curry(arg)

    return initial_func


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
    """
    Decorator that processes default arguments marked with Evaluated and Isolated.
    For Evaluated: calls the provided function to get the default value at call time
    For Isolated: makes a deep copy of the provided argument value
    Only supports keyword-only arguments. All parameters must be keyword-only.
    Args:
        func: The function to be decorated
    Returns:
        A decorated version of the input function with smart argument processing
    Raises:
        AssertionError: If used with non-keyword-only arguments or if both
        Evaluated and Isolated are used on the same parameter
    """
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
