import pytest
from multiprocessing import Process
from project.Task6.multi_hash_table import Hash_Table


def worker_insert(ht, start, end):
    for i in range(start, end):
        ht[i] = i * 2


class TestBasicOperations:
    def test_basic_operations(self):
        ht = Hash_Table()
        ht["key1"] = "value1"
        assert ht["key1"] == "value1"

        ht["key1"] = "value2"
        assert ht["key1"] == "value2"

        assert "key1" in ht

        ht["key2"] = "value2"
        assert len(ht) == 2

        del ht["key1"]
        assert "key1" not in ht

        assert ht.get("missing", "default") == "default"

        ht.clear()
        assert len(ht) == 0


class TestParallelOperations:
    def test_parallel_inserts_no_data_loss(self):
        ht = Hash_Table(size=128)

        processes = []
        num_processes = 4
        items_per_process = 25

        for i in range(num_processes):
            start = i * items_per_process
            end = start + items_per_process
            p = Process(target=worker_insert, args=(ht, start, end))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        expected_count = num_processes * items_per_process
        assert len(ht) == expected_count

        for i in range(expected_count):
            assert ht[i] == i * 2

    def test_locks_work_correctly(self):
        ht = Hash_Table()

        def update_same_key(ht, value):
            for _ in range(10):
                ht["shared"] = value

        processes = []
        for i in range(3):
            p = Process(target=update_same_key, args=(ht, i))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        assert "shared" in ht
        assert ht["shared"] in range(3)


def print_recipe():
    recipe = """

Ingredients:
- 4-5 apples
- 1 cup flour
- 1 cup sugar
- 3 eggs
- 1 tsp baking powder
- pinch of salt
- vanilla to taste

Instructions:
1. Beat eggs with sugar until fluffy
2. Add flour, baking powder, salt and vanilla
3. Slice apples thinly
4. Pour half the batter into a baking pan
5. Layer apples on top
6. Pour remaining batter over apples
7. Bake at 180°C for about 40 minutes
8. Check doneness with a toothpick

Enjoy!
    """
    print(recipe)


print_recipe()
