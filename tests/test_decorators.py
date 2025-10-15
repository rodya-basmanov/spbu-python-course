import pytest
import copy
from project.Task3.decorators import (
    curry_explicit,
    uncurry_explicit,
    smart_args,
    Isolated,
    Evaluated,
)


@pytest.fixture
def adder():
    return lambda a, b: a + b


@pytest.fixture
def multiplier():
    return lambda a, b, c: a * b * c


@pytest.fixture
def constant_func():
    return lambda: 100


class TestCurryExplicit:
    def test_basic_curry(self, adder):
        curried = curry_explicit(adder, 2)
        assert curried(3)(4) == 7

    def test_curry_with_three_args(self, multiplier):
        curried = curry_explicit(multiplier, 3)
        assert curried(2)(3)(4) == 24

    def test_curry_zero_arity(self, constant_func):
        curried = curry_explicit(constant_func, 0)
        assert curried() == 100

    def test_curry_negative_arity(self, adder):
        with pytest.raises(ValueError):
            curry_explicit(adder, -1)

    def test_curry_too_many_args(self, adder):
        curried = curry_explicit(adder, 2)
        with pytest.raises(ValueError):
            curried(1, 2, 3)

    def test_curry_only_one_arg_at_a_time(self, adder):
        curried = curry_explicit(adder, 2)
        with pytest.raises(ValueError):
            curried(1, 2)

    def test_curry_builtin_function(self):
        curried_max = curry_explicit(max, 2)
        assert curried_max(5)(3) == 5
        assert curried_max(2)(8) == 8

    def test_curry_builtin_pow(self):
        curried_pow = curry_explicit(pow, 2)
        assert curried_pow(2)(10) == 1024
        assert curried_pow(3)(3) == 27

    def test_curry_unlimited_arity_function(self):
        def var_args(*args):
            return sum(args)

        curried = curry_explicit(var_args, 4)
        assert curried(1)(2)(3)(4) == 10

    def test_curry_string_concat(self):
        def concat(a, b, c):
            return a + b + c

        curried = curry_explicit(concat, 3)
        assert curried("Hello")(" ")("World") == "Hello World"


class TestUncurryExplicit:
    def test_uncurry_basic(self, adder):
        curried = curry_explicit(adder, 2)
        uncurried = uncurry_explicit(curried, 2)
        assert uncurried(5, 6) == 11

    def test_uncurry_three_args(self, multiplier):
        curried = curry_explicit(multiplier, 3)
        uncurried = uncurry_explicit(curried, 3)
        assert uncurried(2, 2, 5) == 20

    def test_uncurry_zero_arity(self, constant_func):
        curried = curry_explicit(constant_func, 0)
        uncurried = uncurry_explicit(curried, 0)
        assert uncurried() == 100

    def test_uncurry_negative_arity(self, adder):
        curried = curry_explicit(adder, 2)
        with pytest.raises(ValueError):
            uncurry_explicit(curried, -1)

    def test_uncurry_wrong_arg_count(self, adder):
        curried = curry_explicit(adder, 2)
        uncurried = uncurry_explicit(curried, 2)
        with pytest.raises(ValueError):
            uncurried(1)

    def test_uncurry_builtin_function(self):
        curried_min = curry_explicit(min, 2)
        uncurried_min = uncurry_explicit(curried_min, 2)
        assert uncurried_min(7, 3) == 3

    def test_uncurry_var_args_function(self):
        def multiply_all(*args):
            result = 1
            for arg in args:
                result *= arg
            return result

        curried = curry_explicit(multiply_all, 5)
        uncurried = uncurry_explicit(curried, 5)
        assert uncurried(1, 2, 3, 4, 5) == 120


class TestSmartArgsIsolated:
    def test_isolated_copy(self):
        @smart_args
        def f(*, d=Isolated()):
            d["a"] = 0
            return d

        d = {"a": 5}
        res = f(d=d)
        assert res == {"a": 0}
        assert d == {"a": 5}

    def test_isolated_deep_copy(self):
        @smart_args
        def f(*, x=Isolated()):
            x["b"]["c"] = 9
            return x

        data = {"b": {"c": 1}}
        res = f(x=data)
        assert res["b"]["c"] == 9
        assert data["b"]["c"] == 1

    def test_isolated_requires_arg(self):
        @smart_args
        def f(*, d=Isolated()):
            return d

        with pytest.raises(TypeError):
            f()


class TestSmartArgsEvaluated:
    def test_evaluated_each_time(self):
        counter = {"n": 0}

        def inc():
            counter["n"] += 1
            return counter["n"]

        @smart_args
        def f(*, x=Evaluated(inc)):
            return x

        a = f()
        b = f()
        assert a == 1 and b == 2

    def test_evaluated_override(self):
        @smart_args
        def f(*, x=Evaluated(lambda: 10)):
            return x

        assert f(x=99) == 99

    def test_evaluated_with_constant_func(self):
        @smart_args
        def f(*, n=Evaluated(lambda: 50)):
            return n

        assert f() == 50


class TestSmartArgsValidation:
    def test_positional_args_not_allowed(self):
        def bad(a):
            return a

        with pytest.raises(AssertionError):
            smart_args(bad)

    def test_mix_isolated_and_evaluated_not_allowed(self):
        @smart_args
        def f(*, x=Isolated()):
            return x

        param = Isolated()
        assert not isinstance(param, Evaluated)

    def test_evaluated_must_have_callable(self):
        with pytest.raises(AssertionError):
            Evaluated(123)


class TestIntegrationSmartArgs:
    def test_combined_isolated_and_evaluated(self):
        counter = {"v": 0}

        def inc():
            counter["v"] += 1
            return counter["v"]

        @smart_args
        def f(*, cfg=Isolated(), num=Evaluated(inc)):
            cfg["n"] = num
            return cfg, num

        base = {"n": 0}
        a, n1 = f(cfg=base)
        b, n2 = f(cfg=base)
        assert base["n"] == 0
        assert n1 != n2
        assert a["n"] != b["n"]
