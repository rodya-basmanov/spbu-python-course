from typing import Any, Iterator, List, Tuple, Optional


class Hash_Table:
    def __init__(self, size: int = 64) -> None:
        """
        Initialize hash table with specified number of buckets.

        Args:
            size: Total number of buckets (default is 64)
        """
        self.size = size
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(size)]

    def _hash(self, key: Any) -> int:
        """
        Calculate hash index for given key.

        Args:
            key: Key to be hashed

        Returns:
            Bucket index for the key
        """
        return hash(key) % self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Args:
            Key: Key to set
            Value: Value to set
        """
        bucket_idx = self._hash(key)
        current_bucket = self.buckets[bucket_idx]

        for idx, (existing_key, _) in enumerate(current_bucket):
            if existing_key == key:
                current_bucket[idx] = (key, value)
                return

        current_bucket.append((key, value))

    def __getitem__(self, key: Any) -> Any:
        """
        Retrieve value associated with key.

        Args:
            key: Key to look up

        Returns:
            Value corresponding to the key

        Raises:
            KeyError: When key is not present in table
        """
        bucket_idx = self._hash(key)

        for stored_key, stored_value in self.buckets[bucket_idx]:
            if stored_key == key:
                return stored_value

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        """
        Remove key-value pair from table.

        Args:
            key: Key of item to remove

        Raises:
            KeyError: When key does not exist
        """
        bucket_idx = self._hash(key)
        target_bucket = self.buckets[bucket_idx]

        for idx, (stored_key, _) in enumerate(target_bucket):
            if stored_key == key:
                target_bucket.pop(idx)
                return

        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        """
        Check if key exists in table.

        Args:
            key: Key to check

        Returns:
            True if key is present, False otherwise
        """
        bucket_idx = self._hash(key)

        for stored_key, _ in self.buckets[bucket_idx]:
            if stored_key == key:
                return True

        return False

    def __len__(self) -> int:
        """Return total number of key-value pairs stored."""
        total = 0
        for bucket in self.buckets:
            total += len(bucket)
        return total

    def __iter__(self) -> Iterator[Any]:
        """Return iterator over all keys in table."""
        for bucket in self.buckets:
            for stored_key, _ in bucket:
                yield stored_key

    def __repr__(self) -> str:
        """Return string representation of hash table."""
        entries = []
        for bucket in self.buckets:
            for stored_key, stored_value in bucket:
                entries.append(f"{stored_key}: {stored_value}")
        return "HashTable({" + ", ".join(entries) + "})"

    def keys(self) -> Iterator[Any]:
        """Return iterator over all keys."""
        return iter(self)

    def values(self) -> Iterator[Any]:
        """Return iterator over all values."""
        for bucket in self.buckets:
            for _, stored_value in bucket:
                yield stored_value

    def items(self) -> Iterator[Tuple[Any, Any]]:
        """Return iterator over key-value pairs."""
        for bucket in self.buckets:
            for pair in bucket:
                yield pair

    def get(self, key: Any, default: Any = None) -> Any:
        """
        Retrieve value for key with fallback default.

        Args:
            key: Key to look up
            default: Value returned if key not found

        Returns:
            Value for key or default value
        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        """
        Remove and return value for key.

        Args:
            key: Key of item to remove

        Returns:
            Value of removed item

        Raises:
            KeyError: When key does not exist
        """
        if key not in self:
            raise KeyError(key)

        result = self[key]
        del self[key]
        return result

    def clear(self) -> None:
        """Remove all key-value pairs from table."""
        for idx in range(self.size):
            self.buckets[idx] = []
