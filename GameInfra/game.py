import numpy as np
from plot_game import plot_game, animate_move, plot_dice, show_whos_turn
from throwDice import throwDice
from apply_move import apply_move
from RandomPlayer import RandomPlayer
from MUIPlayer import MUIPlayer
import game_scoring

def board_init():  # initialize game board
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


def run_game(player1, player2, board=None):
    from time import sleep

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
        plot_game(board.flatten().tolist())
        plot_dice(dice)
        illegal_move = [1]
        retry = 5
        while any(illegal_move) and retry:
            board_prev_state = board.copy()
            show_whos_turn(turn)
            if (turn > 0):
                moves = player1.offer_move(board, turn, dice)
            else:
                moves = player2.offer_move(board, turn, dice)
            board, illegal_move = apply_move(board, turn, dice, moves)
            retry -= 1
        if retry == 0 and any(illegal_move):
            raise('NoGame')

        #drawMoves(moves)
        animate_move(board_prev_state, moves)
        # sleep(0)
        move_log.append(moves)
        turn_count += 1
        plot_game(board.flatten().tolist())
        score = game_scoring.position_sum(board)

    return move_log, turn_count, board


if __name__ == '__main__':
    board = board_init()
    plot_game(board.flatten().tolist())

    player = RandomPlayer('RandomPlayer')
    human_player = MUIPlayer()
    move_log, turn_count, end_board = run_game(player, human_player, board)

    winner = sum(end_board) > 0

    print(f'Winner: {1 if winner else -1}, turn_count:{turn_count}')

    plot_game(end_board, plt_block=11)


