import numpy as np
def throwDice():
    dice =  np.random.randint(1, 7, 2)
    if dice[0] == dice[1]:
        dice = dice.repeat(2)
    return dice
