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
    positive_vulnerbl = board == 1
    negative_vulnerbl = board == -1
    positive_vulnerbl[0] = False
    negative_vulnerbl[-1] = False
    positive_vulnerbl = positive_vulnerbl.nonzero()
    negative_vulnerbl = negative_vulnerbl.nonzero()
    positive_positions = (board > 0).nonzero()
    negative_positions = (board < 0).nonzero()
    all_threat_combinations = np.meshgrid(negative_vulnerbl, positive_positions)
    all_threat_combinations = np.array([all_threat_combinations[0].ravel(), all_threat_combinations[1].ravel()])
    threat_combis = all_threat_combinations[:, all_threat_combinations[0] > all_threat_combinations[1]]
    valid_steps = threat_combis[0] - threat_combis[1]
    threat_probabilities = prob_all[valid_steps]  # initial probabilities, without considering blockages

    idx = threat_probabilities > 0
    threat_combis = threat_combis[:, idx]
    valid_steps = valid_steps[idx]
    threat_probabilities = threat_probabilities[idx]

def max_loss_dice_mov(board, dice, negative_vulnerbl, positive_positions, threat_combis, valid_steps):
    board = np.array(board)
    dice_sum = np.cumsum(dice)
    dice_and_sums = np.append(dice, dice_sum)
    viable_threats_idx = np.in1d(valid_steps, dice_and_sums)
    threat_combis = threat_combis.copy()[:, viable_threats_idx]
    valid_steps = valid_steps.copy()[viable_threats_idx]
    if len(valid_steps) == 0:
        return 0  # no loss
    elif len(valid_steps) == 1:
        #! need 2 make sure this is a valid move
        return threat_combis[0, 0]  # only 1 option
    else:  # figure out max loss






d = np.arange(1, 7)
all_dice_combinations = np.array(np.meshgrid(d, d)).T.reshape(-1, 2)
all_dice_combinations = [np.tile(xi, (1, 2)).flatten() if xi[0]==xi[1] else xi for xi in all_dice_combinations]  # double the doubles
all_dice_sums = [np.cumsum(x)[1:] for x in all_dice_combinations]
all_dice_sums_conctnt = np.concatenate(all_dice_sums)

prob_sum = np.histogram(all_dice_sums_conctnt, np.array(range(25)))
# prob_sum = dict(zip(prob_sum[1][0:-1], prob_sum[0]/36))  # probability dictionary for sums of dice
prob_sum = np.append(prob_sum[0], 0)/36
prob_single_die = np.array(([0] + [11] * 6 + [0] * 18)) / 36
prob_all = prob_sum + prob_single_die


