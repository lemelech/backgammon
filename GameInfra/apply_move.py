import numpy as np


def apply_move(board, turn, dice, moves):
    board = board.copy()  # don't change board in caller space
    board1 = board.copy()  # save initial board state
    prison_idx = int(12.5 - turn * 12.5)
    opponentPrisonIdx = int(12.5 + turn * 12.5)
    opponentSlots = -turn * board > 1

    skips = [m[1] for m in moves]  # movements, (= +- dice)
    destinations = [sum(m) if (m[0] is not None) else None for m in moves]
    illegalMove = np.zeros(len(dice), np.int8, 'F')

    for ii in range(len(moves)):  # iterate over moves
        playersSlots = turn * board > 0
        playersSlotsIdx = playersSlots.nonzero()[0]
        canRemovePegs = all((playersSlotsIdx - 12.5) * turn >= 6.5)

        # check if move is permitted by Dice
        num_dice = len(dice)
        for dice_idx in range(num_dice):
            if turn * skips[ii] == dice[dice_idx]:
                dice = np.delete(dice, dice_idx) # remove from dice
                break
        if num_dice == len(dice):  # no matching dice found
                #illegalMove[ii] = np.bitwise_or(illegalMove(ii), 1)
                illegalMove[ii] |= 1

        if moves[ii][0] is None: # player claims he can't move
            # verify no moves after this
            if ii < len(moves)-1:
                if not all([m[0] is None for m in moves[ii+1:]]):
                    illegalMove[ii] |= 64  # immobility claims must come last

            # verify immobility
            if board[prison_idx]:
                if opponentSlots[prison_idx + skips[ii]]: # ok, prison block
                    continue
                else:
                    illegalMove[ii] |= 32 # must move

            else: # check if all moves are blocked
                for jj in playersSlotsIdx:
                    dest_check = jj + skips[ii]
                    if dest_check > 0 and dest_check < 25: # destination within board
                        if opponentSlots[dest_check]:    # & occupied
                            continue
                        else:
                            illegalMove[ii] |= 32  # must move
                            break

                    elif canRemovePegs:
                        illegalMove[ii] |= 32  # must move
                        break
        else:  # player claims a move
            if board[prison_idx] and moves[ii][0] != prison_idx:
                illegalMove[ii] |= 16 # must free prisoners

            if playersSlots[moves[ii][0]]:  # is player's pegs
                board[moves[ii][0]] -= turn  # pick up your peg...
            else:
                illegalMove[ii] |= 2  # Not your's

            if destinations[ii] <= 0 or destinations[ii] >= 25:
                if not canRemovePegs:  # check if allowed to remove pegs
                    illegalMove[ii] |= 4  # can't remove

            else:  # check if destination occupied
                if opponentSlots[destinations[ii]]:
                    illegalMove[ii] |= 8  # occupied
                else:
                    if board[destinations[ii]] == -turn:  # take prisoner
                        # add one to prison
                        board[opponentPrisonIdx] -= turn
                        board[destinations[ii]] = turn  # land in destination
                    else:
                        # land in destination
                        board[destinations[ii]] += turn  # land in destination

    if any(illegalMove):
        board = board1  # recover previous board state

    return board, illegalMove

