import numpy as np


class Board:
    def __init__(self, size):
        self.size = size
        self.squares = np.zeros((size, size), dtype=int)
        self.marked_sqrs = 0
        self.max_item_win = 3 if size == 5 else 5

    def final_state(self, marked_row, marked_col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        player = self.squares[marked_row][marked_col]

        for dr, dc in directions:
            count = 0
            for delta in range(-self.max_item_win + 1, self.max_item_win):
                r = marked_row + delta * dr
                c = marked_col + delta * dc
                if 0 <= r < self.size and 0 <= c < self.size:
                    if self.squares[r][c] == player:
                        count += 1
                        if count == self.max_item_win:
                            return player
                    else:
                        count = 0
                else:
                    count = 0
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.empty_sqr(r, c)]

    def is_full(self):
        return self.marked_sqrs == self.size * self.size

    def longest_sequence(self, player):
        longest = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for row in range(self.size):
            for col in range(self.size):
                if self.squares[row][col] == player:
                    for dr, dc in directions:
                        count = 0
                        for delta in range(-self.max_item_win + 1, self.max_item_win):
                            r = row + delta * dr
                            c = col + delta * dc
                            if 0 <= r < self.size and 0 <= c < self.size and self.squares[r][c] == player:
                                count += 1
                                longest = max(longest, count)
                            else:
                                count = 0
        return longest
