import numpy as np


def board_init():  # initialize game board
    board = np.zeros([1, 26], None, 'F')
    board[0][1] = 2
    board[0][24] = -2
    board[0][6] = -5
    board[0][19] = 5
    board[0][8] = -3
    board[0][17] = 3
    board[0][12] = 5
    board[0][13] = -5
    return board


def game_is_on(board):  # check if game is not over
    return any(i > 0 for i in board) & any(i < 0 for i in board)


def run_game(player1, player2):
