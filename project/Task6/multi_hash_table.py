from typing import Any, Iterator, Tuple
from typing import MutableMapping
from multiprocessing import Manager


class HashTable(MutableMapping):
    def __init__(self, size: int = 64) -> None:
        self.size = size
        self.manager = Manager()
        self.buckets = self.manager.list([self.manager.list() for _ in range(size)])
        self.locks = [self.manager.Lock() for _ in range(size)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        bucket_idx = self._hash(key)
        with self.locks[bucket_idx]:
            bucket = self.buckets[bucket_idx]
            for idx, (existing_key, _) in enumerate(bucket):
                if existing_key == key:
                    bucket[idx] = (key, value)
                    return
            bucket.append((key, value))

    def __getitem__(self, key: Any) -> Any:
        bucket_idx = self._hash(key)
        for stored_key, stored_value in self.buckets[bucket_idx]:
            if stored_key == key:
                return stored_value
        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        bucket_idx = self._hash(key)
        with self.locks[bucket_idx]:
            bucket = self.buckets[bucket_idx]
            for idx, (stored_key, _) in enumerate(bucket):
                if stored_key == key:
                    del bucket[idx]
                    return
            raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        bucket_idx = self._hash(key)
        for stored_key, _ in self.buckets[bucket_idx]:
            if stored_key == key:
                return True
        return False

    def __len__(self) -> int:
        total = 0
        for idx in range(self.size):
            with self.locks[idx]:
                total += len(self.buckets[idx])
        return total

    def __iter__(self) -> Iterator[Any]:
        for idx in range(self.size):
            lock = self.locks[idx]
            bucket = self.buckets[idx]
            with lock:
                for key, _ in bucket:
                    yield key

    def __repr__(self) -> str:
        entries = []
        for idx in range(self.size):
            lock = self.locks[idx]
            bucket = self.buckets[idx]
            with lock:
                for key, value in bucket:
                    entries.append(f"{key}: {value}")
        return f"HashTable({{{', '.join(entries)}}})"

    def keys(self) -> Iterator[Any]:  # type: ignore[override]
        return iter(self)

    def values(self) -> Iterator[Any]:  # type: ignore[override]
        for idx in range(self.size):
            lock = self.locks[idx]
            bucket = self.buckets[idx]
            with lock:
                for _, value in bucket:
                    yield value

    def items(self) -> Iterator[Tuple[Any, Any]]:  # type: ignore[override]
        for idx in range(self.size):
            lock = self.locks[idx]
            bucket = self.buckets[idx]
            with lock:
                for pair in bucket:
                    yield pair

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    # type: ignore[override]
    def pop(self, key: Any, default: Any = None) -> Any:
        idx = self._hash(key)
        lock = self.locks[idx]
        bucket = self.buckets[idx]
        with lock:
            for i, (k, v) in enumerate(bucket):
                if k == key:
                    del bucket[i]
                    return v
            if default is not None:
                return default
            raise KeyError(key)

    def clear(self) -> None:
        for idx in range(self.size):
            lock = self.locks[idx]
            with lock:
                self.buckets[idx] = self.manager.list()
