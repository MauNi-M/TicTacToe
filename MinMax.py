# minmax function for the tic tac toe game ai
import numpy as np
from random import choice
N_STEPS = 3

class MinMaxTicTacToeAgent(object):

    def __init__(self, board, piece):
        self.board = board
        self.piece = piece

    def make_play(self) -> np.array:
        valid_moves = [cell for cell in range(self.board.size) if self.board[cell] == 0]
        scores = dict(zip(valid_moves, [score_move(self.board, cell, self.piece, N_STEPS) for cell in valid_moves]))
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        self.board[choice(max_cols)] = self.piece
        return self.board
# Helper functions

def score_move(board, cell, piece, nsteps):
    next_board = make_move(board, cell, piece)
    score = minmax(next_board, nsteps - 1, False, piece)
    return score


def is_terminal_window(window):
    return window.count(1) == 3 or window.count(2) == 3


def is_terminal_node(board):
    matrix = board.reshape(3, 3)
    # Check for a draw
    if list(board).count(0) == 0:
        return True
    # Check for win: horizontal, vertical, diagonal
    # Horizontal
    for row in matrix:
        window = list(row)
        if is_terminal_window(window):
            return True

    for row in matrix.T:
        window = list(row)
        if is_terminal_window(window):
            return True

    if is_terminal_window(list(matrix.diagonal())):
        return True

    if is_terminal_window(list(np.fliplr(matrix).diagonal())):
        return True

    return False


def minmax(node, depth, maximizingPlayer, piece):
    is_terminal = is_terminal_node(node)
    valid_moves = [c for c in range(3) if node.reshape(3, 3)[0][c] == 0]
    if depth == 0 or is_terminal:
        return get_heuristic(node, piece)
    if maximizingPlayer:
        value = -np.Inf
        for cell in valid_moves:
            child = make_move(node, cell, piece)
            value = max(value, minmax(child, depth - 1, False, piece))
        return value
    else:
        value = np.Inf
        for cell in valid_moves:
            child = make_move(node, cell, piece % 2 + 1)
            value = min(value, minmax(child, depth - 1, True, piece))
        return value


def make_move(board, cell, piece):
    next_board = board.copy()
    next_board[cell] = piece
    return next_board


def get_heuristic(board, piece):
    num_twos = count_windows(board, 2, piece)
    num_threes = count_windows(board, 3, piece)
    num_twos_opp = count_windows(board, 2, piece % 2 + 1)
    score = num_twos - 1e2 * num_twos_opp + 1e6 * num_threes
    return score


def check_window(window, num_pieces, piece):
    return window.count(piece) == num_pieces and window.count(0) == 3 - num_pieces


def count_windows(board, num_pieces, piece) -> int:
    num_windows = 0
    matrix = board.reshape(3, 3)
    # Horizontal
    for row in matrix:
        window = list(row)
        if check_window(window, num_pieces, piece):
            num_windows += 1
    # Vertical
    for row in matrix.T:
        window = list(row)
        if check_window(window, num_pieces, piece):
            num_windows += 1
    # Positive diagonal
    if check_window(list(matrix.diagonal()), num_pieces, piece):
        num_windows += 1

    # Negative diagonal
    if check_window(list(np.fliplr(matrix).diagonal()), num_pieces, piece):
        num_windows += 1

    return num_windows
