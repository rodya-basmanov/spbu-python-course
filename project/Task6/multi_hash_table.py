from typing import Any, Iterator, List, MutableMapping, Tuple, Optional
from multiprocessing import Manager


class HashTable(MutableMapping):
    def __init__(self, size: int = 64) -> None:
        """
        Initialize hash table with specified number of buckets.
        Args:
            size: Total number of buckets (default is 64)
        """
        self.size = size
        self.manager = Manager()
        self.buckets = self.manager.list([self.manager.list() for _ in range(size)])
        self.locks = [self.manager.Lock() for _ in range(size)]

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

        with self.locks[bucket_idx]:
            bucket = self.buckets[bucket_idx]
            for idx, (existing_key, _) in enumerate(bucket):
                if existing_key == key:
                    bucket[idx] = (key, value)
                    return
            bucket.append((key, value))

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
        Remove key-value pair from the hash table.

        Args:
            key: Key of item to remove

        Raises:
            KeyError: If key does not exist
        """
        bucket_idx = self._hash(key)

        with self.locks[bucket_idx]:
            bucket = self.buckets[bucket_idx]

            for idx, (stored_key, _) in enumerate(bucket):
                if stored_key == key:
                    del bucket[idx]
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
        for idx in range(self.size):
            with self.locks[idx]:
                total += len(self.buckets[idx])
        return total

    def __iter__(self) -> Iterator[Any]:
        """Return iterator over all keys in table."""
        for idx in range(self.size):
            lock = self.locks[idx]
            bucket = self.buckets[idx]
            with lock:
                for key, _ in bucket:
                    yield key

    def __repr__(self) -> str:
        """Return string representation of hash table."""
        entries = []
        for idx in range(self.size):
            lock = self.locks[idx]
            bucket = self.buckets[idx]
            with lock:
                for key, value in bucket:
                    entries.append(f"{key}: {value}")
        return f"HashTable({{{', '.join(entries)}}})"

    def keys(self) -> Iterator[Any]:
        """Return iterator over all keys."""
        return iter(self)

    def values(self) -> Iterator[Any]:
        """Return iterator over all values."""
        for idx in range(self.size):
            lock = self.locks[idx]
            bucket = self.buckets[idx]
            with lock:
                for _, value in bucket:
                    yield value

    def items(self) -> Iterator[Tuple[Any, Any]]:
        """Return iterator over key-value pairs."""
        for idx in range(self.size):
            lock = self.locks[idx]
            bucket = self.buckets[idx]
            with lock:
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
        idx = self._hash(key)
        lock = self.locks[idx]
        bucket = self.buckets[idx]
        with lock:
            for i, (k, v) in enumerate(bucket):
                if k == key:
                    del bucket[i]
                    return v
            raise KeyError(key)

    def clear(self) -> None:
        """Remove all key-value pairs from table."""
        for idx in range(self.size):
            lock = self.locks[idx]
            with lock:
                self.buckets[idx] = self.manager.list()
