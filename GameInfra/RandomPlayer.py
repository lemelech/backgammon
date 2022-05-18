from BkgPlayer import BkgPlayer
import numpy as np
from apply_move import apply_move
import game_scoring as gs


class RandomPlayer(BkgPlayer):
    """Random backgammon player class"""
    def __init__(self, player_name):
        # super(RandomPlayer, self).__init__(player_name)
        self.name = player_name
        self.PlayerType = 'randPlayer'

    def offer_move(self, board, turn, dice):
        board = board.copy()  # don't change board in caller space
        moves = []
        my_slots = (board * turn) > 0
        others_slots = -turn * board > 1  # opponent's taken slots
        others_slots[[0,25]] = False  # prison slots are not 'Taken', as they're off board
        #  prison_idx = 0 + 25 * (1 - turn) / 2 # my prison
        prison_idx = 0 if turn > 0 else 25  # my prison
        escape_slots = (np.logical_not(others_slots[prison_idx + turn * (np.arange(6)+1)]) ).nonzero()[0] + 1 # valid prison brake slots

        # first deal with prisoners:
        while my_slots[prison_idx] and len(dice):
            escape_dice = np.isin(dice, escape_slots)
            if any(escape_dice):
                escape_dice = escape_dice.nonzero()[0]
                escape_dice = np.random.choice(escape_dice) # select one at random
                moves.append([prison_idx, turn * dice[escape_dice]]) # add  move
                # board(prison_idx) = board(prison_idx) - turn; % update board
                board, err = apply_move(board, turn, [dice[escape_dice]], [moves[-1]])
                if err:
                    print(err)  # keyboard
                dice = np.delete(dice, escape_dice)  # remove from dice
                my_slots = (board * turn) > 0  # update myslots
            else: # cant make no more moves
                for d in dice:
                    moves.append([None, turn * d])
                dice = []

        # rest of moves:
        my_slots = (board * turn) > 0
        my_slots_idx = my_slots.nonzero()[0]
        while len(dice) and len(my_slots_idx):
            can_remove_pegs = all((my_slots_idx - 12.5) * turn > 6) # removing stage
            destinations = my_slots_idx + turn * dice.reshape((dice.size, 1)) # 2D all combinations of positions + dice
            destinationsValid = np.logical_and(
                np.logical_or(np.logical_and(destinations > 0, destinations < 25), [[can_remove_pegs] * destinations.shape[1]] * destinations.shape[0]),
                np.logical_not(others_slots[np.clip(destinations,0,25)]) )  # which are valid moves
            if np.any(destinationsValid):
                    # choose random movement
                    valid_idx = destinationsValid.flatten().nonzero()[0]
                    choice = np.random.choice(valid_idx)
                    [diceIdx, slotIdx] = np.unravel_index(choice, destinations.shape)
                    moves.append([my_slots_idx[slotIdx], turn * dice[diceIdx]] )
                    # board update:
                    board, err = apply_move(board, turn, dice[[diceIdx]], [moves[-1]])
                    if err:
                        input('ilegal move,Enter to continue')

                    # % board(my_slots_idx(slotIdx)) = board(my_slots_idx(slotIdx)) - turn;
                    # % slotIdx = my_slots_idx(slotIdx) + turn * Dice(diceIdx);
                    # % if slotIdx > 1 & & slotIdx < 26
                    #     % board(slotIdx) = board(slotIdx) + turn;
                    # % end
                    dice = np.delete(dice, diceIdx)
            else: # no more valid moves
                for d in dice:
                    moves.append( [None, turn * d])
                dice = []
            my_slots = (board * turn) > 0
            my_slots_idx = my_slots.nonzero()[0]

        for d in dice:#if game has ended but some dice left
            moves.append([None, turn * d])
        return moves


class BestRandomNPlayer(BkgPlayer):
    """performs best of n randomly sampled moves of RandomPlayer"""
    def __init__(self, player_name, n=3):
        # super(RandomPlayer, self).__init__(player_name)
        self.name = player_name
        self.n = n
        self.PlayerType = 'randPlayer'+str(n)
        self.RandomPlayer = RandomPlayer(player_name)

    def offer_move(self, board, turn, dice):
        offer_moves = [self.RandomPlayer.offer_move(board, turn, dice) for _ in range(self.n)]
        # boards = [b for b,_ in [apply_move(board, turn, dice, om) for om in offer_moves]]
        # scores = [gs.total_position_score(b, turn) for b in boards]
        scores = [gs.total_position_score(b, turn) for b,_ in [apply_move(board, turn, dice, om) for om in offer_moves]]
        return offer_moves[np.argmax(scores)]