from typing import Callable, List, Union

import numpy as np

from selector import RandomSelector, Selector, StandardInputSelector


class Player:
    def __init__(self, size: int, candidates: List[List[int]], selector: Selector) -> None:
        """
        Args:
            size (int): 盤の1辺の大きさ
            candidates (List[List[int]]): 初期の候補
            selector (Selector): マスの選択方法
        """
        self.size = size

        # self.candidates: 候補リスト、self.candidates[i]は (size-i) 個選択されている候補
        self.candidates = [[] for _ in range(size + 1)]
        self.candidates[-1] = candidates

        self.selector = selector

    def my_turn_update(self, num: int) -> bool:
        """
        自身の操作による候補リストの更新
        選択した数字が含まれる候補をずらす

        Args:
            num (int): 自分が選択した数字

        Returns:
            bool: 今回の操作で勝利条件を満たしたか
        """
        for i in range(self.size):
            removed_num = 0  # 削除された個数、for文の中のpopによる整合性を保つ
            for j in range(len(self.candidates[i + 1])):
                idx = j - removed_num
                elem = self.candidates[i + 1][idx]
                if num in elem:
                    self.candidates[i].append(elem)
                    self.candidates[i + 1].pop(idx)
                    removed_num += 1
        return len(self.candidates[0]) > 0

    def opponent_turn_update(self, num: int) -> None:
        """
        相手の操作による候補リストの更新
        選択した数字が含まれる候補を削除する

        Args:
            num (int): 相手が選択した数字
        """
        for i in range(self.size):
            removed_num = 0  # 削除された個数、for文の中のpopによる整合性を保つ
            for j in range(len(self.candidates[i])):
                idx = j - removed_num
                elem = self.candidates[i][idx]
                if num in elem:
                    self.candidates[i].pop(idx)
                    removed_num += 1


class TicTacToe:
    size: int
    num_cells: int
    players: List[Player]
    rest: List[int]
    board: List[str]

    def __init__(self, size: int, num_cells: int, selectors: List[Selector]) -> None:
        """
        Args:
            size (int): 1辺の大きさ
            num_cells (int): マスの総数
            selectors (List[Selector]): マスの選択方法のリスト
        """
        self.size = size
        self.num_cells = num_cells
        candidates = self.get_candidates()
        self.players = [Player(size, candidates, selectors[i]) for i in range(2)]
        self.rest = np.arange(num_cells).tolist()
        self.board = ["_" for _ in range(num_cells)]

    def get_plane_candidates(self, grid: np.ndarray) -> List[List[int]]:
        """
        与えられたグリッドから縦横斜めの取り出し、リストにして返す

        Args:
            grid (np.ndarray): self.size x self.sizeの平面、要素はインデックス

        Returns:
            List[List[int]]: 候補のリスト
        """
        assert grid.shape == (self.size, self.size)
        candidates = []
        diagonal1 = []
        diagonal2 = []
        for i in range(self.size):
            candidates.append(grid[i, :].tolist())
            candidates.append(grid[:, i].tolist())
            diagonal1.append(int(grid[i, i]))
            diagonal2.append(int(grid[i, -1 - i]))
        candidates.append(diagonal1)
        candidates.append(diagonal2)

        return candidates

    def get_candidates(self) -> List[List[int]]:
        """
        盤面全体に対する候補のリストを返す

        Returns:
            List[List[int]]: 候補のリスト
        """
        return NotImplementedError

    def apply_select(self, turn: int, num: int) -> bool:
        """
        あるターンでの選択を盤面に反映し、勝利条件を満たしたか確認する

        Args:
            turn (int): ターン数
            num (int): 選択された数字

        Returns:
            bool: 勝利条件を満たしたか
        """
        assert num in self.rest
        self.rest.remove(num)
        is_win = self.players[turn % 2].my_turn_update(num)
        self.players[(turn + 1) % 2].opponent_turn_update
        t.board[num] = str(turn % 2)
        return is_win

    def execute(self, display_func: Union[str, Callable[[], None]]) -> int:
        """ゲームの実行

        Args:
            display_func (Union[str, Callable[[], None]]): 表示用関数

        Returns:
            int: 勝者（-1: 引き分け、0 or 1: 勝者のインデックス）
        """
        display = self.select_display_function(display_func)
        display()
        for i in range(self.num_cells):
            num = self.players[i % 2].selector.select(self.rest)
            is_win = self.apply_select(i, num)
            display()
            if is_win:
                return i % 2
        return -1

    def std_output(self) -> None:
        """
        標準出力での表示
        """
        return NotImplementedError

    def select_display_function(self, display_func: Union[str, Callable[[], None]]) -> Callable[[], None]:
        """
        表示用関数の選択

        Args:
            display_func (Union[str, Callable[[], None]]): 表示用関数の指定

        Returns:
            Callable[[], None]: 表示用関数
        """
        if isinstance(display_func, Callable):
            return display_func
        elif display_func == "std_output":
            return self.std_output
        elif display_func == "pass":
            return lambda: None
        elif isinstance(display_func, str):
            raise ValueError(f"Invalid string: {display_func}")
        else:
            raise TypeError(f"Invalid argument type: {type(display_func)}")


class PlaneTicTacToe(TicTacToe):
    def __init__(self, size: int, selectors: List[Selector]) -> None:
        num_cells = size**2
        super().__init__(size, num_cells, selectors)

    def get_candidates(self) -> List[List[int]]:
        return self.get_plane_candidates(np.arange(self.num_cells).reshape(self.size, self.size))

    def std_output(self) -> None:
        out = ""
        for i in range(self.num_cells):
            out += self.board[i]
            if (i + 1) % self.size == 0:
                out += "\n"
        print(out)


class CubeTicTacToe(TicTacToe):
    def __init__(self, size: int, selectors: List[Selector]) -> None:
        num_cells = size**3
        super().__init__(size, num_cells, selectors)

    def get_candidates(self) -> List[List[int]]:
        cube = np.arange(self.num_cells).reshape(self.size, self.size, self.size)
        candidates = []
        diagonals = [[] for _ in range(4)]
        for i in range(self.size):
            candidates += self.get_plane_candidates(cube[:, :, i])
            candidates += self.get_plane_candidates(cube[:, i, :])
            candidates += self.get_plane_candidates(cube[i, :, :])
            diagonals[0].append(int(cube[i, i, i]))
            diagonals[1].append(int(cube[i, -1 - i, i]))
            diagonals[2].append(int(cube[-1 - i, i, i]))
            diagonals[3].append(int(cube[-1 - i, -1 - i, i]))
        print(diagonals)
        candidates += diagonals
        return candidates

    def std_output(self) -> None:
        out = ""
        for i in range(self.num_cells):
            out += self.board[i]
            if (i + 1) % self.size == 0:
                out += "\n"
            if (i + 1) % (self.size**2) == 0:
                out += "\n"
        print(out)


if __name__ == "__main__":
    size = 3
    print(PlaneTicTacToe.__name__)
    selectors = [RandomSelector(), StandardInputSelector(size**2)]
    t = PlaneTicTacToe(size, selectors)
    winner = t.execute(display_func="std_output")
    if winner == -1:
        print("draw")
    else:
        print(f"winner is {winner}")

    print(CubeTicTacToe.__name__)
    selectors = [RandomSelector(), StandardInputSelector(size**3)]
    t = CubeTicTacToe(size, selectors)
    winner = t.execute(display_func="std_output")
    if winner == -1:
        print("draw")
    else:
        print(f"winner is {winner}")
