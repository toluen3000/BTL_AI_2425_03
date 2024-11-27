
import sys
import pygame
import numpy as np

pygame.init()

#color

WHITE = (255,255,255)
GREY = (180,180,180)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

# kich thuoc va ti le
TOTAL_WIDTH = 800
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 3
BOARD_ROWS = 15
BOARD_COLS = 15

SQUARE_SIZE = WIDTH//BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 10

# create
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Tro Choi Co Caro')
screen.fill(WHITE)

# tao ban co
board = np.zeros((BOARD_ROWS,BOARD_COLS))

# Trạng thái trò chơi
game_state = "menu"  # menu hoặc playing

# xay dung menu truoc khi bat dau
def drawMenu():
    """Vẽ giao diện màn hình chính."""
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    title = font.render("Chào mừng đến với Cờ Caro", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    # Vẽ nút bắt đầu
    pygame.draw.rect(screen, GREY, (WIDTH // 2 - 100, 300, 200, 50))
    play_text = font.render("Bắt đầu", True, RED)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 310))

# ve ban co
def drawLines(color = BLACK):
    for i in range(1,BOARD_ROWS):
        pygame.draw.line(screen,color,(0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE*i),LINE_WIDTH)
        pygame.draw.line(screen,color,(SQUARE_SIZE * i,0), (SQUARE_SIZE*i,HEIGHT),LINE_WIDTH)

def drawOptions():
    font = pygame.font.Font(None, 40)  # Font chữ
    # Vẽ nút X ở bên phải của bàn cờ
    pygame.draw.rect(screen, GREY, (WIDTH + 10, 100, 80, 50))  # Nút hình chữ nhật
    text_X = font.render("X", True, RED)
    screen.blit(text_X, (WIDTH + 35, 110))  # Vẽ chữ X trên nút

    # Vẽ nút O ở bên phải của bàn cờ
    pygame.draw.rect(screen, GREY, (WIDTH + 10, 200, 80, 50))  # Nút hình chữ nhật
    text_O = font.render("O", True, GREEN)
    screen.blit(text_O, (WIDTH + 35, 210))  # Vẽ chữ O trên nút


#ve X va O
def drawFigures(color = BLACK):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen,GREEN,(int(col * SQUARE_SIZE + SQUARE_SIZE //2), int(row * SQUARE_SIZE + SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, RED,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 # Điểm bắt đầu
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 # Điểm kết thúc
                                 CROSS_WIDTH)
                pygame.draw.line(screen, RED,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 # Điểm bắt đầu
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 # Điểm kết thúc
                                 CROSS_WIDTH)


# danh dau vao o vuong
def mark(row,col,player):
    board[row,col] = player
# nhung o vuong con danh dau duoc
def available_square(row,col):
    return board[row][col] == 0

def isBoardFull(checkBoard = board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if checkBoard[row][col] == 0:
                return True
    return False

def checkWin(player):
    # Check rows, columns, and diagonals
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if np.all(board[row, col:col + 5] == player):
                return True
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 4):
            if np.all(board[row:row + 5, col] == player):
                return True
    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS - 4):
            if all(board[row + i, col + i] == player for i in range(5)):
                return True
            if all(board[row + i, col + 4 - i] == player for i in range(5)):
                return True
    return False



player = 1 #auto x
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]  # X coordinate
            mouseY = event.pos[1]  # Y coordinate

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark(clicked_row, clicked_col, player)
                if checkWin(player):
                    print(f"Player {player} wins!")
                    running = False
                player = 2 if player == 1 else 1

    drawOptions()
    drawLines()
    drawFigures()
    pygame.display.update()

pygame.quit()
