import random as rnd
from typing import List


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
