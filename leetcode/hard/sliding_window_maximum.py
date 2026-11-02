"""LeetCode 239 — Sliding Window Maximum (Hard)

Question:
Given an integer list and a window size ``k``, return the largest value in
each contiguous window of that size.

Solution:
Keep indices in a deque whose values decrease from front to back. Remove
expired indices from the front and smaller values from the back; the front
then identifies the maximum for each complete window.

Time: O(n). Space: O(k), where n is the length of the input list.
"""

from collections import deque
from typing import Deque, List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if not nums or k <= 0 or k > len(nums):
            return []

        candidates: Deque[int] = deque()
        maxima: List[int] = []

        for index, value in enumerate(nums):
            while candidates and candidates[0] <= index - k:
                candidates.popleft()

            while candidates and nums[candidates[-1]] <= value:
                candidates.pop()

            candidates.append(index)
            if index >= k - 1:
                maxima.append(nums[candidates[0]])

        return maxima
