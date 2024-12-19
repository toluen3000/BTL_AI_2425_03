import numpy as np


class Board:
    #Chức năng: Khởi tạo một bảng cờ mới.
    def __init__(self, size):
        self.size = size
        self.squares = np.zeros((size, size), dtype=int)
        self.marked_sqrs = 0
        self.max_item_win = 5

    #Chức năng: Kiểm tra xem sau khi đánh dấu ô (marked_row, marked_col), người chơi có chiến thắng không.
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

    #Chức năng: Đánh dấu một ô trên bảng bởi một người chơi.
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    #Chức năng: Kiểm tra xem ô (row, col) có trống hay không.
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    #Chức năng: Lấy danh sách tất cả các ô trống trên bảng.
    def get_empty_sqrs(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.empty_sqr(r, c)]

    # Chức năng: Kiểm tra xem bàn cờ đã full chưa.
    def is_full(self):
        return self.marked_sqrs == self.size * self.size

