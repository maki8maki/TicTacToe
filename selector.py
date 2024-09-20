import random as rnd
from typing import List, Set, Union

import numpy as np


class Selector:
    def __init__(self) -> None:
        pass

    def select(self, rest: List[int]) -> int:
        """
        残りの数字から選択する

        Args:
            rest (List[int]): 残りの数字

        Returns:
            int: 選択した数字
        """
        return NotImplementedError


class RandomSelector(Selector):
    def __init__(self) -> None:
        """
        ランダムに数字を選択する
        """
        super().__init__()

    def select(self, rest: List[int]) -> int:
        idx = rnd.randrange(len(rest))
        num = rest[idx]
        return num


class StandardInputSelector(Selector):
    def __init__(self, num_cells: int) -> None:
        """
        標準入力で数字を選択する

        Args:
            num_cells (int): マスの総数
        """
        super().__init__()

        self.num_cells = num_cells

    def select(self, rest: List[int]) -> int:
        print(f"Remaining numbers: {rest}")
        while True:
            num = int(input("Select number from above: "))
            if num in rest:
                break
            elif num < 0 or self.num_cells - 1 < num:
                print(f"{num} is a number of out of range")
            else:
                print(f"{num} is already selected")
        return num


class BitStrategicSelector(Selector):
    def __init__(self, size: int, num_cells: int, candidates: List[List[int]]) -> None:
        """
        少し戦略的に数字を選択する

        Args:
            size (int): 1辺のサイズ
            num_cells (int): マスの総数
            candidates (List[List[int]]): 初期の候補
        """
        super().__init__()

        self.threshold = size - int((size + 1) / 2)
        self.priority = np.zeros((num_cells))
        for candidate in candidates:
            for num in candidate:
                self.priority[num] += 1

    def _select_by_priority(self, nums: Union[Set[int], List[int]]) -> int:
        """
        与えられた候補から優先度が高いものを選択する

        Args:
            nums (Union[Set[int], List[int]]): 候補

        Returns:
            int: 選択した数字
        """
        if isinstance(nums, set):
            nums = list(nums)
        max_idx = np.argmax(self.priority[nums])
        return nums[max_idx]

    def select(self, rest: List[int], my_candidates: List[List[int]], opponent_candidates: List[List[int]]) -> int:
        # リーチのものがあればそれを選択する
        for elem in my_candidates[1]:
            for num in elem:
                if num in rest:
                    return num

        s = set([])

        # 相手が半分以上埋めている列の残りから選択する
        for i in range(1, self.threshold + 1):
            for elem in opponent_candidates[i]:
                for num in elem:
                    if num in rest:
                        s.add(num)
            if len(s) != 0:
                return self._select_by_priority(s)

        # 埋めている数が多い列から選択する
        for i in range(2, len(my_candidates)):
            for elem in my_candidates[i]:
                for num in elem:
                    if num in rest:
                        s.add(num)
            if len(s) != 0:
                return self._select_by_priority(s)

        return self._select_by_priority(rest)
