# -*- coding: UTF-8 -*-
# coding=utf-8
from typing import List


class Solution1:

    # 合并区间 merged[-1] 代表访问列表最后一个元素
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = []
        for interval in intervals:
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                merged[-1][1] = max(merged[-1][1], interval[1])
        return merged

    # 移动0 [0,1,5,3,2,0,4] -> [1,5,3,2,4,0,0]
    def moveZeroes(self, nums: List[int]) -> List[int]:
        n = len(nums)
        left = right = 0
        while right < n:
            if nums[right] != 0:
                if left < right:
                    temp = nums[right]
                    nums[right] = nums[left]
                    nums[left] = temp
                left += 1
            right += 1
        return nums

    # 盛水最多的容器
    def maxArea(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        capacity = 0
        while left < right:
            capacity = max(capacity, min(nums[left], nums[right]) * (right - left))
            if (nums[left] < nums[right]):
                left += 1
            else:
                right -= 1
        return capacity


s1 = Solution1()
intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
merged_intervals = s1.merge(intervals)
print('合并区间结果: {}'.format(merged_intervals))

moveZeroes = s1.moveZeroes([0, 1, 5, 3, 2, 0, 4])
print('移动0结果: {}'.format(moveZeroes))

maxArea = s1.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7])
print('盛水最多的容器结果: {}'.format(maxArea))
