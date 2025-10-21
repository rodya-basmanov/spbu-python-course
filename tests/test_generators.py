import pytest

from project.Task2.generators import data_generator, pipeline, apply_custom_operation


# Fixtures placed at the top as requested
@pytest.fixture
def numbers():
    return [1, 2, 3, 4, 5]


@pytest.fixture
def strings():
    return ["apple", "banana", "cherry"]


@pytest.fixture
def mixed_data():
    return [1, "hello", 3.14, True]


class TestPipelineFunction:
    """Tests for pipeline function that chains operations."""

    def test_pipeline_basic(self, numbers):
        """Test basic pipeline with built-in map and filter."""
        result = list(
            pipeline(
                numbers,
                lambda x: map(lambda y: y * 2, x),
                lambda x: filter(lambda y: y > 5, x),
            )
        )
        assert result == [6, 8, 10]

    def test_pipeline_multiple_operations(self):
        """Test pipeline with multiple sequential operations."""
        result = list(
            pipeline(
                data_generator(0, 10),
                lambda x: filter(lambda y: y % 2 == 0, x),
                lambda x: map(lambda y: y**2, x),
                lambda x: filter(lambda y: y < 50, x),
            )
        )
        assert result == [0, 4, 16, 36]

    @pytest.mark.parametrize(
        "operations, expected",
        [
            ([lambda s: map(lambda x: x + 1, s)], [2, 3, 4, 5, 6]),
            (
                [
                    lambda s: filter(lambda x: x > 2, s),
                    lambda s: map(lambda x: x * 10, s),
                ],
                [30, 40, 50],
            ),
            (
                [
                    lambda s: map(lambda x: x * 2, s),
                    lambda s: filter(lambda x: x % 4 == 0, s),
                    lambda s: map(lambda x: x // 2, s),
                ],
                [2, 4],
            ),
        ],
    )
    def test_pipeline_parametrize(self, numbers, operations, expected):
        """Parametrized tests for different pipeline configurations."""
        result = list(pipeline(numbers, *operations))
        assert result == expected

    def test_pipeline_with_zip(self):
        """Test pipeline with zip operation."""
        result = list(
            pipeline(
                [1, 2, 3],
                lambda x: zip(x, [10, 20, 30]),
                lambda x: map(lambda pair: pair[0] + pair[1], x),
            )
        )
        assert result == [11, 22, 33]


class TestDataGenerator:
    """Tests for data generator function."""

    @pytest.mark.parametrize(
        "start,end,step,expected",
        [
            (0, 5, 1, [0, 1, 2, 3, 4]),
            (0, 10, 2, [0, 2, 4, 6, 8]),
            (5, 8, 1, [5, 6, 7]),
            (-2, 3, 1, [-2, -1, 0, 1, 2]),
            (10, 5, -1, []),  # empty range
        ],
    )
    def test_data_generator_parametrized(self, start, end, step, expected):
        """Parametrized tests for data generator with different parameters."""
        result = list(data_generator(start, end, step))
        assert result == expected

    def test_data_generator_in_pipeline(self):
        """Test data generator used in pipeline."""
        result = list(
            pipeline(
                data_generator(1, 6),
                lambda x: map(lambda y: y * 3, x),
                lambda x: filter(lambda y: y % 2 == 0, x),
            )
        )
        assert result == [6, 12]


class TestApplyCustomOperation:
    """Tests for apply_custom_operation function."""

    @pytest.fixture
    def custom_doubler(self):
        """Fixture providing custom doubling function."""
        return lambda x: x * 2

    @pytest.fixture
    def custom_string_formatter(self):
        """Fixture providing custom string formatting function."""
        return lambda s: f"processed_{s}"

    @pytest.fixture
    def custom_type_converter(self):
        """Fixture providing custom type conversion function."""
        return lambda x: str(x) if isinstance(x, int) else x

    def test_apply_custom_operation_basic(self, numbers, custom_doubler):
        """Test basic usage of apply_custom_operation."""
        result = list(apply_custom_operation(custom_doubler, numbers))
        assert result == [2, 4, 6, 8, 10]

    def test_apply_custom_operation_strings(self, strings, custom_string_formatter):
        """Test apply_custom_operation with string data."""
        result = list(apply_custom_operation(custom_string_formatter, strings))
        assert result == ["processed_apple", "processed_banana", "processed_cherry"]

    def test_apply_custom_operation_mixed_data(self, mixed_data, custom_type_converter):
        """Test apply_custom_operation with mixed data types."""
        result = list(apply_custom_operation(custom_type_converter, mixed_data))
        assert result == ["1", "hello", 3.14, "True"]

    @pytest.mark.parametrize(
        "input_data, custom_func, expected",
        [
            ([1, 2, 3], lambda x: x**2, [1, 4, 9]),
            (["a", "b", "c"], lambda s: s.upper(), ["A", "B", "C"]),
            ([1.5, 2.5, 3.5], lambda x: int(x), [1, 2, 3]),
        ],
    )
    def test_apply_custom_operation_parametrized(
        self, input_data, custom_func, expected
    ):
        """Parametrized tests for apply_custom_operation."""
        result = list(apply_custom_operation(custom_func, input_data))
        assert result == expected
