import random

import numpy as np
from tic_tac_toe import RandomAgent, OneStepLookaheadAgent, MinMaxTicTacToeAgent


class TicTocBoard(object):
    def __init__(self, board_size):
        self.board = np.zeros(board_size**2)
        self.agent = None
        self.p1 = 0
        self.p2 = 0
        self.boardart = ['\n', '', '', '', '', '|', '', '', '', '', '|', '', '', '', '', '\n', '', '-', '', '|', '',
                         '-', '', '|', '', '-', '', '\n_____|_____|_____\n', '', '', '', '', '|', '', '', '', '', '|',
                         '', '', '', '', '\n', '', '-', '', '|', '', '-', '', '|', '', '-', '', '\n_____|_____|_____\n',
                         '', '', '', '', '|', '', '', '', '', '|', '', '', '', '', '\n', '', '-', '', '|', '', '-', '',
                         '|', '', '-', '', '\n', '', '', '', '', '|', '', '', '', '', '|', '', '', '', '', '']
        self.positions = [i for i, x in enumerate(self.boardart) if x == "-"]
        self.mapping = dict(zip(range(1, (board_size ** 2)+1), self.positions))

    def endgame(self):
        matrix = self.board.reshape(3, 3)

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

    def make_play(self, player, cell):
        # print(F"Parameters entered for make_play: {player}, {cell}")
        # print(f"type of parameters: {type(player)}, {type(cell)}")
        if player == 1:
            pos = "O"
        elif player == 2:
            pos = "X"
        else:
            raise ValueError("Not valid player")
        self.board[cell-1] = player
        self.update_art()

    def update_art(self):
        for index, move in enumerate(self.board):
            if move == 1:
                self.boardart[self.mapping[index+1]] = "O"
            elif move == 2:
                self.boardart[self.mapping[index+1]] = "X"
            else:continue

    def show_board(self):
        print(" ".join(self.boardart))

    def select_player(self):
        opponent = int(input(
            "Hello!, choose your Opponent:\n"
            "1.RandomAgent\n"
            "2.One-Step LookaheadAgent\n"
            "3.N-Step LookaheadAgent\n4.Human"))
        players = [1, 2]
        self.p1 = players.pop((random.randint(0, 1)))
        self.p2 = players[0]
        match opponent:
            case 1:
                self.agent = RandomAgent(board=self.board, piece=self.p2)
            case 2:
                self.agent = OneStepLookaheadAgent(board=self.board, piece=self.p2, size=3)
            case 3:
                self.agent = MinMaxTicTacToeAgent(board=self.board, piece=self.p2)
            case 4:
                self.agent = None


    def instructions(self):
        print("""Hi, for you to play you will be given  the choice of numbers
        from 1 to nine to pick the cell you want to play, beware that occupied cells
        will not be available nor numbers outside of that range""")

    def available_moves(self):
        moves = [str(index + 1) for index, cell in enumerate(self.board) if cell == 0]
        print(f"Your available moves are: {'-'.join(moves)}")
        return moves

    def human_playing(self, piece):
        print(self.available_moves())
        if not self.available_moves():
            return False
        p1_move = input("Pick a move")
        while p1_move not in self.available_moves():
            print("Not a valid move")
            p1_move = input("Pick a move")
        self.make_play(piece, int(p1_move))
        return True


    def agent_playing(self):
        self.board = self.agent.make_play()
        self.update_art()

    def play(self):
        winner = 0
        while True:
            if self.p1 == 1:
                print("You play with 'O'")
                # print(f"Human playing player: {self.p1}")
                is_winner = self.endgame()
                while not is_winner:
                    self.human_playing(self.p1)
                    self.show_board()
                    is_winner = self.endgame()
                    if is_winner:
                        if is_winner == self.p1:
                            print("You win!")
                        else:
                            print("You lose")
                    cls()
                    self.agent_playing()
                    self.show_board()
                    is_winner = self.endgame()
                    if is_winner:
                        if is_winner == self.p1:
                            print("You win!")
                        else:
                            print("You lose")

            else:
                print("You play with X")
                is_winner = self.endgame()
                while not is_winner:
                    self.agent_playing()
                    self.show_board()
                    is_winner = self.endgame()
                    if is_winner:
                        if is_winner == self.p1:
                            print("You win!")
                        else:
                            print("You lose")
                    cls()
                    self.human_playing(self.p1)
                    is_winner = self.endgame()
                    if is_winner:
                        if is_winner == self.p1:
                            print("You win!")
                        else:
                            print("You lose")
            break

if __name__ == "__main__":
    from pyfiglet import Figlet
    from os import name, system


    def cls():
        command = "clear"
        if name in ("nt", "dos"):
            command = "cls"
        system(command)


    f = Figlet(font='slant')
    print(f.renderText('MauNi\'s Tic-Tac-Toe'))

    game_over = False
    while not game_over:
        new_board = TicTocBoard(3)
        new_board.select_player()
        new_board.instructions()
        new_board.show_board()
        new_board.play()
        answer = input("Do you want to continue? [Y/N]").upper()
        while answer not in ["Y", "N"]:
            answer = input("Do you want to continue? [Y/N]").upper()
        if answer == "Y":
            game_over = False
        elif answer == "N":
            game_over = True
            print("Good bye!")
        else:
            print("Answer not valid")
