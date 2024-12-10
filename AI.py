import time
from functools import lru_cache
import random
import copy


class AI:
    def __init__(self, player=2):
        self.player = player
        self.opponent = 3 - player
        self.max_time = 5  # Time limit for thinking (seconds)
        self.evaluate_board = lru_cache(maxsize=10000)(self.evaluate_board)
        self.transposition_table = {}
        self.opening_book = {
            (5, 5): [(2, 2), (2, 3), (3, 2), (3, 3)],  # Center and adjacent moves
            (7, 7): [(3, 3), (3, 4), (4, 3), (4, 4)]  # Center and adjacent moves
        }

    def eval(self, main_board):
        start_time = time.time()

        # Check opening book
        if main_board.marked_sqrs < 2 and (main_board.size, main_board.size) in self.opening_book:
            return random.choice(self.opening_book[(main_board.size, main_board.size)])

        empty_sqrs = main_board.get_empty_sqrs()

        # Quick evaluation for early game
        if len(empty_sqrs) > main_board.size * main_board.size - 4:
            return self.quick_eval(main_board, empty_sqrs)

        # Check for immediate winning moves and blocks
        for row, col in empty_sqrs:
            if self.is_winning_move(main_board, row, col, self.player):
                return (row, col)
        for row, col in empty_sqrs:
            if self.is_winning_move(main_board, row, col, self.opponent):
                return (row, col)

        # Check for open threes and other complex threats
        threat_move = self.check_complex_threats(main_board)
        if threat_move:
            return threat_move

        # Use iterative deepening within time limit
        return self.iterative_deepening(main_board, 10, self.max_time - (time.time() - start_time))

    def quick_eval(self, board, empty_sqrs):
        center = board.size // 2
        best_move = None
        best_score = -float('inf')

        for row, col in empty_sqrs:
            score = -(abs(row - center) + abs(col - center))
            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move

    def is_winning_move(self, board, row, col, player):
        temp_board = copy.deepcopy(board)
        temp_board.mark_sqr(row, col, player)
        return temp_board.final_state(row, col) == player

    def check_complex_threats(self, board):
        for row in range(board.size):
            for col in range(board.size):
                if board.empty_sqr(row, col):
                    if self.is_open_three(board, row, col, self.player):
                        return (row, col)
                    if self.is_open_three(board, row, col, self.opponent):
                        return (row, col)
        return None

    def is_open_three(self, board, row, col, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            line = self.get_line(board, row, col, dr, dc)
            if self.is_open_three_pattern(line, player):
                return True
        return False

    def is_open_three_pattern(self, line, player):
        pattern = [0, player, player, player, 0]
        return pattern in [line[i:i + 5] for i in range(len(line) - 4)]

    def get_line(self, board, row, col, dr, dc):
        line = []
        for i in range(-board.max_item_win + 1, board.max_item_win):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < board.size and 0 <= c < board.size:
                line.append(board.squares[r][c])
            else:
                break
        return line

    # Giữ lại các phương thức hiện có từ caro 1.txt
    def evaluate_board(self, board):
        score = 0
        if self.check_win(board, self.player):
            score += 10000
        if self.check_win(board, self.opponent):
            score -= 10000
        for row in range(board.size):
            for col in range(board.size):
                if board.squares[row][col] == self.player:
                    score += self.evaluate_position(board, row, col, self.player)
                elif board.squares[row][col] == self.opponent:
                    score -= self.evaluate_position(board, row, col, self.opponent)
        return score

    def evaluate_position(self, board, row, col, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            block_count = 0
            for delta in range(-3, 4):
                r = row + delta * dr
                c = col + delta * dc
                if 0 <= r < board.size and 0 <= c < board.size:
                    if board.squares[r][c] == player:
                        count += 1
                    elif board.squares[r][c] != 0:
                        block_count += 1
                        break
                else:
                    block_count += 1
                    break
            if block_count < 2:
                score += count ** 2
        return score

    def check_win(self, board, player):
        for row in range(board.size):
            for col in range(board.size):
                if board.squares[row][col] == player:
                    if self.win_condition(board, row, col, player):
                        return True
        return False

    def win_condition(self, board, row, col, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            for delta in range(-board.max_item_win + 1, board.max_item_win):
                r = row + delta * dr
                c = col + delta * dc
                if 0 <= r < board.size and 0 <= c < board.size:
                    if board.squares[r][c] == player:
                        count += 1
                        if count == board.max_item_win:
                            return True
                    else:
                        count = 0
        return False

    # Update đoạn code mới
    def evaluate_sequences(self, board, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(board.size):
            for col in range(board.size):
                for dr, dc in directions:
                    score += self.evaluate_direction(board, row, col, dr, dc, player)
        return score

    def evaluate_direction(self, board, row, col, dr, dc, player):
        score = 0
        max_win = board.max_item_win
        line = []
        for i in range(max_win):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < board.size and 0 <= c < board.size:
                line.append(board.squares[r][c])
            else:
                break
        if len(line) >= max_win:
            score += self.score_window(line, player, max_win)
        return score

    def score_window(self, window, player, max_win):
        score = 0
        opponent = 3 - player

        player_count = window.count(player)
        opponent_count = window.count(opponent)
        empty_count = window.count(0)

        if opponent_count == max_win - 1 and empty_count == 1:
            score -= 2000  # Prioritize blocking opponent's winning move
        elif player_count == max_win - 1 and empty_count == 1:
            score += 1000
        elif opponent_count == max_win - 2 and empty_count == 2:
            score -= 500  # Prioritize blocking opponent's potential threats
        elif player_count == max_win - 2 and empty_count == 2:
            score += 100
        elif player_count > 0 and opponent_count == 0:
            score += 10 * player_count
        elif opponent_count > 0 and player_count == 0:
            score -= 15 * opponent_count

        return score

    def evaluate_potential_threats(self, board, player):
        score = 0
        opponent = 3 - player
        for row in range(board.size):
            for col in range(board.size):
                if board.squares[row][col] == 0:
                    score += self.evaluate_future_threat(board, row, col, player)
                    score -= self.evaluate_future_threat(board, row, col, opponent)
        return score

    def evaluate_future_threat(self, board, row, col, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            line = self.get_line(board, row, col, dr, dc)
            score += self.score_potential_threat(line, player, board.max_item_win)
        return score

    def score_potential_threat(self, line, player, max_win):
        score = 0
        opponent = 3 - player
        player_count = line.count(player)
        empty_count = line.count(0)

        if player_count == max_win - 2 and empty_count == 2:
            score += 50  # Potential future threat
        elif player_count == max_win - 3 and empty_count == 3:
            score += 10  # Developing threat

        return score

    def iterative_deepening(self, board, max_depth, max_time):
        best_move = None
        start_time = time.time()
        for depth in range(1, max_depth + 1):
            if time.time() - start_time > max_time:
                break
            score, move = self.minimax(board, depth, -float('inf'), float('inf'), True, start_time)
            if move:
                best_move = move
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing, start_time):
        if depth == 0 or board.is_full() or time.time() - start_time > self.max_time:
            return self.evaluate_board(board), None

        empty_sqrs = board.get_empty_sqrs()
        empty_sqrs.sort(key=lambda move: self.move_ordering_score(board, move[0], move[1]), reverse=maximizing)

        if maximizing:
            max_eval = -float('inf')
            best_move = None
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval, _ = self.minimax(temp_board, depth - 1, alpha, beta, False, start_time)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.opponent)
                eval, _ = self.minimax(temp_board, depth - 1, alpha, beta, True, start_time)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def move_ordering_score(self, board, row, col):
        score = 0
        center = board.size // 2
        score += 10 - (abs(row - center) + abs(col - center))

        # Prioritize moves that form or block potential threats
        temp_board = copy.deepcopy(board)
        temp_board.mark_sqr(row, col, self.player)
        score += self.evaluate_potential_threats(temp_board, self.player)

        temp_board = copy.deepcopy(board)
        temp_board.mark_sqr(row, col, self.opponent)
        score += self.evaluate_potential_threats(temp_board, self.opponent)

        return score
