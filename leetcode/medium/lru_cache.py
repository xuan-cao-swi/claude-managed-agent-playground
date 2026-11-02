"""LeetCode 146 — LRU Cache (Medium)

Question:
Build a cache with a fixed capacity. ``get`` returns a stored value or ``-1``,
and ``put`` inserts or updates a value. Whenever the cache is full, inserting
an item evicts the one that has gone unused for the longest time.

Both operations should run in O(1) time.

Solution:
Combine a dictionary for key lookup with a doubly linked list ordered from
least recently used to most recently used.

Time: O(1) per operation. Space: O(capacity).
"""

from typing import Dict, Optional


class _Node:
    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value
        self.previous: Optional[_Node] = None
        self.next: Optional[_Node] = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("capacity must not be negative")

        self.capacity = capacity
        self.nodes: Dict[int, _Node] = {}
        self.least_recent = _Node(0, 0)
        self.most_recent = _Node(0, 0)
        self.least_recent.next = self.most_recent
        self.most_recent.previous = self.least_recent

    def _remove(self, node: _Node) -> None:
        node.previous.next = node.next
        node.next.previous = node.previous

    def _add_as_most_recent(self, node: _Node) -> None:
        previous = self.most_recent.previous
        previous.next = node
        node.previous = previous
        node.next = self.most_recent
        self.most_recent.previous = node

    def _mark_as_most_recent(self, node: _Node) -> None:
        self._remove(node)
        self._add_as_most_recent(node)

    def get(self, key: int) -> int:
        node = self.nodes.get(key)
        if node is None:
            return -1

        self._mark_as_most_recent(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.nodes.get(key)
        if node is not None:
            node.value = value
            self._mark_as_most_recent(node)
            return

        node = _Node(key, value)
        self.nodes[key] = node
        self._add_as_most_recent(node)

        if len(self.nodes) > self.capacity:
            least_recent = self.least_recent.next
            self._remove(least_recent)
            del self.nodes[least_recent.key]
