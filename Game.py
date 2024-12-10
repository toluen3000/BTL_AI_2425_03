from Board import Board
from AI import AI
import random
import tkinter as tk
from tkinter import messagebox
import threading

# --- Constants ---
DEFAULT_WIDTH = 700
DEFAULT_HEIGHT = 700

BG_COLOR = "#FFFFFF"
LINE_COLOR = "#000000"
CIRC_COLOR = "#00FF00"
CROSS_COLOR = "#FF0000"


class Game(tk.Tk):
    def __init__(self, size=11, gamemode='ai'):
        super().__init__()
        self.title("Nhóm 13 - AI - HaUI")
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT + 100}")
        self.canvas = tk.Canvas(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        self.size = size
        self.sqsize = DEFAULT_WIDTH // self.size
        self.radius = self.sqsize // 4
        self.offset = self.sqsize // 4
        self.line_width = self.offset // 2
        self.circ_width = self.offset // 2
        self.cross_width = self.offset // 2

        self.board = Board(self.size)
        self.ai = AI()
        self.player = 1
        self.gamemode = gamemode
        self.running = True
        self.ai_thinking = False
        self.show_lines()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.reset_button = tk.Button(self, text="Chơi lại", command=self.reset, font=("Times New Roman", 16, "bold"),
                                      padx=20, pady=10)
        self.reset_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.status_label = tk.Label(self, text="", font=("Times New Roman", 14))
        self.status_label.pack(pady=10)

    def show_lines(self):
        self.canvas.delete("all")
        for col in range(1, self.size):
            x = col * self.sqsize
            self.canvas.create_line(x, 0, x, DEFAULT_HEIGHT, fill=LINE_COLOR, width=self.line_width)
        for row in range(1, self.size):
            y = row * self.sqsize
            self.canvas.create_line(0, y, DEFAULT_WIDTH, y, fill=LINE_COLOR, width=self.line_width)

    def draw_fig(self, row, col):
        if self.board.squares[row][col] == 1:
            start_desc = (col * self.sqsize + self.offset, row * self.sqsize + self.offset)
            end_desc = (col * self.sqsize + self.sqsize - self.offset, row * self.sqsize + self.sqsize - self.offset)
            self.canvas.create_line(*start_desc, *end_desc, fill=CROSS_COLOR, width=self.cross_width)

            start_asc = (col * self.sqsize + self.offset, row * self.sqsize + self.sqsize - self.offset)
            end_asc = (col * self.sqsize + self.sqsize - self.offset, row * self.sqsize + self.offset)
            self.canvas.create_line(*start_asc, *end_asc, fill=CROSS_COLOR, width=self.cross_width)
        elif self.board.squares[row][col] == 2:
            center = (col * self.sqsize + self.sqsize // 2, row * self.sqsize + self.sqsize // 2)
            self.canvas.create_oval(center[0] - self.radius, center[1] - self.radius,
                                    center[0] + self.radius, center[1] + self.radius,
                                    outline=CIRC_COLOR, width=self.circ_width)

    def make_move(self, row, col):
        if self.board.empty_sqr(row, col):
            self.board.mark_sqr(row, col, self.player)
            self.draw_fig(row, col)
            self.next_turn()
            return True
        return False

    def next_turn(self):
        self.player = self.player % 2 + 1
        self.status_label.config(text=f"Lượt của Người chơi {self.player}")

    def is_over(self, row, col):
        result = self.board.final_state(row, col)
        if result != 0:
            winner = "Người chơi 1" if result == 1 else "Người chơi 2"
            messagebox.showinfo("Kết quả", f"{winner} đã thắng")
            self.running = False
            self.status_label.config(text=f"{winner} đã thắng")
        elif self.board.is_full():
            messagebox.showinfo("Kết quả", "Hòa")
            self.running = False
            self.status_label.config(text="Hòa")

    def handle_click(self, event):
        if not self.running or self.ai_thinking:
            return

        col = event.x // self.sqsize
        row = event.y // self.sqsize

        if self.board.empty_sqr(row, col):
            if self.gamemode == 'pvp' or self.player == 1:
                if self.make_move(row, col):
                    if not self.is_over(row, col):
                        if self.gamemode == 'ai' and self.running:
                            self.status_label.config(text="AI đang suy nghĩ...")
                            self.after(100, self.ai_turn)
        else:
            self.status_label.config(text="Ô này đã được đánh!")

    def ai_turn(self):
        self.ai_thinking = True

        def ai_move():
            move = self.ai.eval(self.board)
            if move:
                self.after(0, lambda: self.make_ai_move(move))
            else:
                self.after(0, self.handle_ai_no_move)

        threading.Timer(0.5, ai_move).start()

    def make_ai_move(self, move):
        row, col = move
        self.make_move(row, col)
        self.is_over(row, col)
        self.ai_thinking = False
        self.status_label.config(text="Lượt của bạn")

    def handle_ai_no_move(self):
        print("AI không tìm được nước đi hợp lệ!")
        empty_sqrs = self.board.get_empty_sqrs()
        if empty_sqrs:
            move = random.choice(empty_sqrs)
            self.make_ai_move(move)
        else:
            self.status_label.config(text="Hòa - Không còn nước đi!")
            self.running = False
        self.ai_thinking = False

    def reset(self):
        self.board = Board(self.size)
        self.player = 1
        self.running = True
        self.ai_thinking = False
        self.show_lines()
        self.status_label.config(text="Bắt đầu trò chơi mới")

    def update(self):
        self.canvas.update()
        self.update_idletasks()


if __name__ == '__main__':
    game = Game()
    game.mainloop()
