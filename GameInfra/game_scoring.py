import numpy as np


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

def position_sum(board, turn):
    """ sum of player's positions """
    board = np.array(board)
    if turn > 0:
        positive = board > 0
        player_sum = (positive * board * np.arange(26)).sum()
    else:
        negative = board < 0
        player_sum = (negative * board * np.arange(25, -1, -1)).sum()
    return player_sum


def full_house(board, turn):
    """how many of opponent's last quarter is occupied"""
    board = np.array(board)
    if turn > 0:
        full_h = (board[1:7] < -1).sum() / 6
    else:
        full_h = (board[19:25] > 1).sum()/6
    return full_h


def risk_expect(board, turn):
    """risk: loss expectation
    current implementation is a first order risk : only first move
    and doesn't remove blocked paths from the loss"""
    board = np.array(board)
    positive_positions = (board > 0).nonzero()
    negative_positions = (board < 0).nonzero()

    if turn > 0:
        # positive risk
        positive_vulnerbl = board == 1
        positive_vulnerbl[0] = False
        positive_vulnerbl = positive_vulnerbl.nonzero()
        all_threat_combinations = np.meshgrid(positive_vulnerbl, negative_positions)
        all_threat_combinations = np.array([all_threat_combinations[0].ravel(), all_threat_combinations[1].ravel()])
        threat_combis = all_threat_combinations[:, all_threat_combinations[0] < all_threat_combinations[1]]
        valid_steps = threat_combis[1] - threat_combis[0]
        threat_probabilities = prob_all[valid_steps]  # initial probabilities, without considering blockages
        risk = (threat_probabilities * (threat_combis[0, :])).sum()
        num_vulnerable = len(positive_vulnerbl)
    else:
        # negative risk:
        negative_vulnerbl = board == -1
        negative_vulnerbl[-1] = False
        negative_vulnerbl = negative_vulnerbl.nonzero()
        all_threat_combinations = np.meshgrid(negative_vulnerbl, positive_positions)
        all_threat_combinations = np.array([all_threat_combinations[0].ravel(), all_threat_combinations[1].ravel()])
        threat_combis = all_threat_combinations[:, all_threat_combinations[0] > all_threat_combinations[1]]
        valid_steps = threat_combis[0] - threat_combis[1]
        threat_probabilities = prob_all[valid_steps]  # initial probabilities, without considering blockages
        risk = (threat_probabilities * (25 - threat_combis[0, :])).sum()
        num_vulnerable = len(negative_vulnerbl)
    return risk, num_vulnerable


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
        raise NotImplementedError


def total_position_score(board, turn):
    risk, n_threat = risk_expect(board, turn)
    total = position_sum(board, turn) - risk - n_threat * full_house(board, turn)
    return total





