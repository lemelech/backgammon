import numpy as np


def position_sum(board):  # sum of each player's positions
    board = np.array(board)
    positive = board > 0
    negative = board < 0
    positive_sum = (positive * board * np.arange(26)).sum()
    negative_sum = (negative * board * np.arange(25, -1, -1)).sum()
    return positive_sum, negative_sum


def risk(board, turn):
    board = np.array(board)
    positive = board == 1
    negative = board == -1
    positive[0] = False
    negative[-1] = False


d = np.arange(1, 7)
all_dice_combinations = np.array(np.meshgrid(d, d)).T.reshape(-1, 2)
all_dice_combinations = [np.tile(xi, (1, 2)).flatten() if xi[0]==xi[1] else xi for xi in all_dice_combinations]  # double the doubles
list(map(np.cumsum,all_dice_combinations))


