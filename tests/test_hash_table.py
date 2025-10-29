import pytest
from project.Task5.hash_table import Hash_Table


class TestHashTable:
    def test_initialization(self):
        ht = Hash_Table()
        assert ht.size == 64
        assert len(ht.buckets) == 64

        custom_ht = Hash_Table(100)
        assert custom_ht.size == 100
        assert len(custom_ht.buckets) == 100

    def test_insert_and_retrieve(self):
        ht = Hash_Table()
        ht["apple"] = 5
        assert ht["apple"] == 5

    def test_update_existing_key(self):
        ht = Hash_Table()
        ht["apple"] = 5
        assert ht["apple"] == 5

        ht["apple"] = 10
        assert ht["apple"] == 10

    def test_retrieve_missing_key(self):
        ht = Hash_Table()
        with pytest.raises(KeyError):
            _ = ht["apple"]

    def test_remove_item(self):
        ht = Hash_Table()
        ht["apple"] = 5
        ht["banana"] = 3

        del ht["apple"]

        with pytest.raises(KeyError):
            _ = ht["apple"]

        assert ht["banana"] == 3

    def test_remove_nonexistent_item(self):
        ht = Hash_Table()
        with pytest.raises(KeyError):
            del ht["missing"]

    def test_membership_check(self):
        ht = Hash_Table()
        ht["apple"] = 5

        assert "apple" in ht
        assert "banana" not in ht

    def test_table_length(self):
        ht = Hash_Table()
        assert len(ht) == 0

        ht["apple"] = 5
        assert len(ht) == 1

    def test_iteration_in_loop(self):
        ht = Hash_Table()
        ht["apple"] = 5
        ht["banana"] = 3

        found_keys = []
        found_values = []

        for k in ht:
            found_keys.append(k)
            found_values.append(ht[k])

        assert len(found_keys) == 2
        assert "apple" in found_keys
        assert "banana" in found_keys
        assert 5 in found_values
        assert 3 in found_values

    def test_collision_handling(self):
        ht = Hash_Table(1)

        test_data = [("a", 1), ("b", 2), ("c", 3), ("d", 4)]

        for k, v in test_data:
            ht[k] = v

        for k, expected_v in test_data:
            assert ht[k] == expected_v

        assert len(ht) == 4

    def test_keys_method(self):
        ht = Hash_Table()
        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3

        key_list = list(ht.keys())
        assert sorted(key_list) == ["a", "b", "c"]

    def test_values_method(self):
        ht = Hash_Table()
        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3

        value_list = list(ht.values())
        assert sorted(value_list) == [1, 2, 3]

    def test_items_method(self):
        ht = Hash_Table()
        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3

        item_list = list(ht.items())
        assert sorted(item_list) == [("a", 1), ("b", 2), ("c", 3)]

    def test_get_with_existing_key(self):
        ht = Hash_Table()
        ht["a"] = 1
        assert ht.get("a") == 1

    def test_get_with_missing_key(self):
        ht = Hash_Table()
        assert ht.get("missing") is None

    def test_pop_with_existing_key(self):
        ht = Hash_Table()
        ht["a"] = 1
        returned_value = ht.pop("a")
        assert returned_value == 1
        assert "a" not in ht

    def test_pop_with_missing_key(self):
        ht = Hash_Table()
        with pytest.raises(KeyError):
            ht.pop("missing")

    def test_clear_method(self):
        ht = Hash_Table()
        ht["a"] = 1
        ht["b"] = 2
        ht.clear()
        assert len(ht) == 0
        assert list(ht.items()) == []
