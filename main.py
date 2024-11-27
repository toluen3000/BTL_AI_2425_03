
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

player = 1 # 1 là người chơi X hai là O

# xay dung menu truoc khi bat dau
def drawMenu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)

    # Tiêu đề
    title = font.render("Tro Choi Co Caro", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    title2 = font.render("Nhom 13 - AI", True, BLACK)
    screen.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 200))

    # Nút bắt đầu
    pygame.draw.rect(screen, GREY, (WIDTH // 2 - 100, 300, 200, 50))
    play_text = font.render("Let's Start", True, RED)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 310))

    # Nút chọn X
    pygame.draw.rect(screen, GREY, (WIDTH // 2 - 100, 400, 90, 50))
    x_text = font.render("X", True, RED)
    screen.blit(x_text, (WIDTH // 2 - 100 + 45 - x_text.get_width() // 2, 410))

    # Nút chọn O
    pygame.draw.rect(screen, GREY, (WIDTH // 2 + 10, 400, 90, 50))
    o_text = font.render("O", True, GREEN)
    screen.blit(o_text, (WIDTH // 2 + 55 - o_text.get_width() // 2, 410))


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

# ALPHABET_MOVING


# GAME LOOP
running = True
menu_active = True
player_symbol = None
player = None
skip_next_click = False  # Để bỏ qua click sau khi chuyển trạng thái

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if menu_active and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos

            # Nút "Let's Start"
            if WIDTH // 2 - 100 <= mouseX <= WIDTH // 2 + 100 and 300 <= mouseY <= 350:
                if player_symbol is not None:
                    menu_active = False
                    skip_next_click = True

            # Nút chọn X
            elif WIDTH // 2 - 100 <= mouseX <= WIDTH // 2 - 10 and 400 <= mouseY <= 450:
                player_symbol = "X"
                player = 2

            # Nút chọn O
            elif WIDTH // 2 + 10 <= mouseX <= WIDTH // 2 + 100 and 400 <= mouseY <= 450:
                player_symbol = "O"
                player = 1

        # Xử lý khi chơi game
        if not menu_active and event.type == pygame.MOUSEBUTTONDOWN:
            if skip_next_click:
                skip_next_click = False
                continue

            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE


            if 0 <= clicked_row < BOARD_ROWS and 0 <= clicked_col < BOARD_COLS:
                if available_square(clicked_row, clicked_col):
                    board[clicked_row][clicked_col] = player
                    if checkWin(player):
                        print(f"Player {player_symbol} wins!")
                        running = False
                    player = 1 if player == 2 else 2  # Chuyển lượt

    if menu_active:
        drawMenu()
        if player_symbol:
            font = pygame.font.Font(None, 40)
            symbol_text = font.render(f"Ban da chon {player_symbol}!", True, BLACK)
            screen.blit(symbol_text, (WIDTH // 2 - symbol_text.get_width() // 2, 500))
    else:
        screen.fill(WHITE)
        drawLines()
        drawFigures()

    pygame.display.update()

pygame.quit()