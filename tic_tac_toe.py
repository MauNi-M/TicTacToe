import random
from MinMax import MinMaxTicTacToeAgent
import numpy as np
from random import choice


class TicTacToe(object):
    def __init__(self, size):
        if size < 3:
            raise ValueError("I'm sorry, I think boards with less than 3x3 squares aren't fun")
        self.size = size
        self.board = np.zeros(self.size * self.size)
        self.nought = 1
        self.cross = 2
        self.empty = 0

    def endgame(self):
        matrix = self.board.reshape(self.size, self.size)

        def check_row(inline):
            if len(list(set(inline))) == 1:
                if list(set(inline))[0] == 1:
                    return 1
                if list(set(inline))[0] == 2:
                    return 2
            return 0

        for row in matrix:
            if check_row(row):
                return check_row(row)
        for row in matrix.T:
            if check_row(row):
                return check_row(row)
        if check_row(matrix.diagonal()):
            return check_row(matrix.diagonal())
        flipped_mat = np.fliplr(matrix)
        if check_row(flipped_mat.diagonal()):
            return check_row(flipped_mat.diagonal())
        return 0


    def out_of_moves(self):
        if 0 not in self.board:
            return True
        else:
            return False
    def random_board(self):
        rng = np.random.default_rng()

        def make_number_piece(number):
            if str(number) == "1":
                return "O"
            elif str(number) == "2":
                return "X"
            else:
                return None

        board_numbers = rng.integers(self.size, size=self.size ** 2)
        board_pieces = list(map(make_number_piece, board_numbers))
        return np.asarray(board_pieces).reshape(self.size, self.size)


class RandomAgent(object):

    def __init__(self, board, piece):
        self.board = board
        if piece == "X":
            self.piece = 2
        else:
            self.piece = 1

    def make_play(self):
        valid_moves = [cell for cell in range(self.board.size) if self.board[cell] == 0]
        if not valid_moves:
            print(valid_moves)
            print(self.board.reshape(3,3))
            print(f"player: {self.piece}")
            raise ValueError("something went wrong with makeplay")
        self.board[choice(valid_moves)] = self.piece
        return self.board


class OneStepLookaheadAgent(object):
    def __init__(self, board, piece, size):
        self.board = board
        if piece == "X":
            self.piece = 2
        else:
            self.piece = 1
        self.size = size

    def make_play(self):
        valid_moves = [cell for cell in range(self.board.size) if self.board[cell] == 0]
        scores = dict(zip(valid_moves, [score_move(self.board, cell, self.piece, self.size) for cell in valid_moves]))
        # Get a list of cells that maximize score
        max_cells = [key for key in scores.keys() if scores[key] == max(scores.values())]
        self.board[choice(max_cells)] = self.piece
        return self.board


# Helper functions
def score_move(board, cell, piece, size):
    next_board = make_move(board, cell, piece)
    score = get_heuristic(next_board, piece, size)
    return score


def make_move(board, cell, piece):
    next_board = board.copy()
    next_board[cell] = piece
    return next_board


def get_heuristic(board, piece, size):
    num_twos = count_windows(board, 2, piece, size)
    num_threes = count_windows(board, 3, piece, size)
    num_twos_opp = count_windows(board, 2, piece%2+1, size)
    score = num_twos - 1e2*num_twos_opp + 1e6*num_threes
    return score


def check_window(window, num_pieces, piece):
    return window.count(piece) == num_pieces and window.count(0) == 3-num_pieces


def count_windows(board, num_pieces, piece, size) -> int:
    num_windows = 0
    matrix = board.reshape(size, size)
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


def play():
    TicTacT = TicTacToe(3)
    size = TicTacT.size
    pieces = ["X", "O"]
    p1_piece = pieces.pop(random.randint(0,1))
    p2_piece = pieces[0]
    agent_1 = RandomAgent(board=TicTacT.board, piece=p1_piece)
    agent_2 = MinMaxTicTacToeAgent(board=TicTacT.board, piece=p2_piece)
    endgame = TicTacT.endgame()
    while not endgame:
        if TicTacT.endgame() != 0:
            return TicTacT.endgame()
        else:
            if TicTacT.out_of_moves():
                break
            else:
                TicTacT.board = agent_1.make_play()
                agent_2.board = TicTacT.board
        print(f"Player 1 turn piece ->{agent_1.piece}:\n {TicTacT.board.reshape(TicTacT.size, TicTacT.size)}")
        if TicTacT.endgame() != 0:
            return TicTacT.endgame()
        else:
            if TicTacT.out_of_moves():
                break
            else:
                TicTacT.board = agent_2.make_play()
                agent_1.board = agent_2.board
        print(f"Player 2 turn piece ->{agent_2.piece}:\n {TicTacT.board.reshape(TicTacT.size, TicTacT.size)}")
        if TicTacT.endgame() != 0:
            return TicTacT.endgame()

        endgame = TicTacT.endgame()
    print("Match played")
    return 0


def get_percentage():
    p1 = 0
    p2 = 0
    draws = 0
    for counter in range(10):
        result = play()
        # print(result)
        if result:
            if result == 1:
                p1 += 1
            if result == 2:
                p2 += 2
        else:
            draws += 1
    print(f"P1 = {(p1/(p1+p2+draws))*100}\nP2 = {(p2/(p1+p2+draws))*100}\nDraws = {(draws/(p1+p2+draws))*100}")
