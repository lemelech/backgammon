import numpy as np
from plot_game import plot_game, animate_move, plot_dice, show_whos_turn, counts_histogram
from throwDice import throwDice
from apply_move import apply_move
from RandomPlayer import RandomPlayer, BestRandomNPlayer
from MUIPlayer import MUIPlayer
import game_scoring

def board_init():  # initialize game board
    """ board is a 26 element array
     each slot indicates the amount of occupying pieces, either positive or negative
     the first [0] and last [25] slots are the jail slots, and [1:24] are the main game board
     positive pieces move from 1 to 24, and are jailed in 0,
     and negative pieces move from 24 to 1, and are jailed at 25"""

    board = np.zeros(26, np.int8, 'F')
    board[1] = 2
    board[24] = -2
    board[6] = -5
    board[19] = 5
    board[8] = -3
    board[17] = 3
    board[12] = 5
    board[13] = -5
    return board


def game_is_on(board):  # check if game is not over
    return (board > 0).any() and (board < 0).any()


def run_game(player1, player2, board=None, graphic_mode='all'):
    """main game loop"""
    np.random.seed()

    # Determine who starts
    turn = np.random.randint(0, 2) * 2 - 1
    turn_count = 0
    move_log = []
    if board is None:
        board = board_init()

    while game_is_on(board):
        turn = -turn
        dice = throwDice()
        if graphic_mode in ['all', 'state']:
            plot_game(board.flatten().tolist())
            plot_dice(dice)
        illegal_move = [1]
        retry = 5
        while any(illegal_move) and retry:
            board_prev_state = board.copy()
            if graphic_mode in ['all', 'state']:
                show_whos_turn(turn)
            if (turn > 0):
                moves = player1.offer_move(board, turn, dice)
            else:
                moves = player2.offer_move(board, turn, dice)
            board, illegal_move = apply_move(board, turn, dice, moves)
            retry -= 1
        if retry == 0 and any(illegal_move):
            raise('NoGame')

        if graphic_mode in ['all']:
            animate_move(board_prev_state, moves)
        move_log.append(moves)
        turn_count += 1
        if graphic_mode in ['all', 'state']:
            plot_game(board.flatten().tolist())
        score = game_scoring.position_sum(board, turn)
    if graphic_mode in ['all', 'state', 'end']:
        plot_game(board, plt_block=11)
    return move_log, turn_count, board


def run_n_games(player1, player2, board=None, graphic_mode=None, n_games=100):
    """game statistics"""
    games_log = []
    turn_counts_log = []

    for g in range(n_games):
        move_log, turn_count, end_board = run_game(player1, player2, board, graphic_mode)

        winner = sum(end_board) < 0
        # print(f'Winner: {player1.name if winner else player2.name}, turn_count:{turn_count}')

        games_log.append(int(winner))
        turn_counts_log.append(turn_count)

    print(f'Player1 {np.array(games_log).sum()} : {n_games - np.array(games_log).sum()} Player2')
    counts_histogram(np.array(turn_counts_log), np.array(games_log), player1.PlayerType, player2.PlayerType)
    return games_log, turn_counts_log


if __name__ == '__main__':

    # player1 = MUIPlayer() # human_player
    # player1 = RandomPlayer('RandomPlayer')
    player1 = BestRandomNPlayer('BestRandomNPlayer', n=3)
    player2 = BestRandomNPlayer('BestRandomNPlayer', n=5)

    wins_log, turn_counts_log = run_n_games(player1, player2, n_games=100)
    # move_log, turn_count, end_board = run_game(player1, player2, None, graphic_mode=None)
