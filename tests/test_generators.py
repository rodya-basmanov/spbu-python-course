import pytest
from project.generators import (
    data_generator,
    map_gen,
    filter_gen,
    zip_gen,
    apply_gen,
    reduce_gen,
    to_list,
    to_set,
    count_gen,
)


@pytest.fixture
def numbers():
    return [1, 2, 3, 4, 5]


@pytest.fixture
def strings():
    return ["apple", "banana", "cherry"]


class TestGenerator:
    def test_generator_basic(self):
        result = list(data_generator(0, 5))
        assert result == [0, 1, 2, 3, 4]

    def test_generator_with_step(self):
        result = list(data_generator(0, 10, 2))
        assert result == [0, 2, 4, 6, 8]


class TestMap:
    @pytest.mark.parametrize(
        "input_list, func, expected",
        [
            ([1, 2, 3], lambda x: x * 2, [2, 4, 6]),
            ([1, 2, 3], lambda x: x + 10, [11, 12, 13]),
            ([5], lambda x: x**2, [25]),
        ],
    )
    def test_map_parametrize(self, input_list, func, expected):
        result = to_list(map_gen(func, input_list))
        assert result == expected

    def test_map_with_fixture(self, numbers):
        result = to_list(map_gen(lambda x: x * 2, numbers))
        assert result == [2, 4, 6, 8, 10]

    def test_map_string(self, strings):
        result = to_list(map_gen(lambda s: s.upper(), strings))
        assert result == ["APPLE", "BANANA", "CHERRY"]


class TestFilter:
    @pytest.mark.parametrize(
        "input_list, predicate, expected",
        [
            ([1, 2, 3, 4, 5], lambda x: x > 3, [4, 5]),
            ([1, 2, 3, 4, 5], lambda x: x % 2 == 0, [2, 4]),
            ([1, 2, 3], lambda x: x < 0, []),
        ],
    )
    def test_filter_parametrize(self, input_list, predicate, expected):
        result = to_list(filter_gen(predicate, input_list))
        assert result == expected

    def test_filter_with_fixture(self, numbers):
        result = to_list(filter_gen(lambda x: x > 2, numbers))
        assert result == [3, 4, 5]


class TestCombinations:
    def test_map_filter(self, numbers):
        result = to_list(filter_gen(lambda x: x > 5, map_gen(lambda x: x * 2, numbers)))
        assert result == [6, 8, 10]

    def test_filter_map(self, numbers):
        result = to_list(
            map_gen(lambda x: x**2, filter_gen(lambda x: x > 2, numbers))
        )
        assert result == [9, 16, 25]

    def test_multiple_operations(self, numbers):
        result = to_list(
            map_gen(
                lambda x: x + 1,
                filter_gen(lambda x: x > 2, map_gen(lambda x: x * 2, numbers)),
            )
        )
        assert result == [5, 7, 9, 11]


class TestZip:
    def test_zip_basic(self, numbers):
        result = to_list(zip_gen(numbers, [10, 20, 30, 40, 50]))
        assert result == [(1, 10), (2, 20), (3, 30), (4, 40), (5, 50)]

    def test_zip_different_lengths(self, numbers):
        result = to_list(zip_gen(numbers, [10, 20]))
        assert result == [(1, 10), (2, 20)]


class TestReduce:
    @pytest.mark.parametrize(
        "func, initial, expected",
        [
            (lambda x, y: x + y, None, 15),
            (lambda x, y: x * y, None, 120),
            (lambda x, y: x + y, 10, 25),
        ],
    )
    def test_reduce_parametrize(self, numbers, func, initial, expected):
        result = reduce_gen(func, numbers, initial)
        assert result == expected


class TestCustomFunctions:
    def test_apply_custom(self, numbers):
        def double_gen(iterable):
            for item in iterable:
                yield item * 2

        result = to_list(apply_gen(double_gen, numbers))
        assert result == [2, 4, 6, 8, 10]

    def test_apply_reversed(self, numbers):
        result = to_list(apply_gen(reversed, numbers))
        assert result == [5, 4, 3, 2, 1]


class TestAggregators:
    def test_to_list(self, numbers):
        result = to_list(numbers)
        assert result == [1, 2, 3, 4, 5]

    def test_to_set(self):
        result = to_set([1, 2, 2, 3, 3])
        assert result == {1, 2, 3}

    def test_count(self, numbers):
        result = count_gen(numbers)
        assert result == 5


# Тесты ленивых вычислений
class TestLazy:
    def test_lazy_evaluation(self):
        executed = []

        def track(x):
            executed.append(x)
            return x * 2

        # Создаём генератор без терминальной операции
        gen = map_gen(track, [1, 2, 3])
        assert len(executed) == 0  # Ещё не выполнено

        # Вызываем терминальную операцию
        result = to_list(gen)
        assert len(executed) == 3
        assert result == [2, 4, 6]

    def test_chaining_generators(self):
        gen = data_generator(0, 10)
        gen = filter_gen(lambda x: x % 2 == 0, gen)
        gen = map_gen(lambda x: x**2, gen)

        result = to_list(gen)
        assert result == [0, 4, 16, 36, 64]


class TestExamples:
    def test_example_pipeline(self):
        result = to_list(
            map_gen(
                lambda x: x * 3, filter_gen(lambda x: x % 2 == 0, data_generator(0, 10))
            )
        )
        assert result == [0, 6, 12, 18, 24]
