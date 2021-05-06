import matplotlib.pyplot as plt
from BkgPlayer import BkgPlayer
import numpy as np


def xy2moves(coords, turn, dice):
    d = []
    place = []
    for c in coords:
        if c[0] > 0.75 and c[1] > 0.4:  # dice area
            if c[1] > 0.62:  # dice separation
                d.append(dice[0])
            else:
                d.append(dice[-1])
        elif 0.16 < c[0] < 0.7 and 0.15 < c[1] < 0.85:  # board area
            if abs(c[0]-0.43) < 0.05 and abs(c[1]-0.5) < 0.15:  # middle (prison) area
                i = 0 if turn==1 else 25  # prison index depends on player
            else:
                i = np.round((c[0]-0.15)*22.6415)  # 12/(0.7-0.17)=22.6415
                if i > 12:
                    i = 12
                elif i < 1:
                    i = 1
                if c[1] < 0.5:  # bottom half of board
                    i = 25 - i
            place.append(int(i))
        else:  # out of bord, i.e. can't do noffin
            place.append(None)
        # print(c)
    if len(place) == len(d) == len(dice):
        moves = [[place[i], d[i]*turn] for i in list(range(len(place)))]
    else:
        return []
    return moves

class MUIPlayer(BkgPlayer):
    """class for human-MouseUI backgammon player"""
    axMUI = []  # will hold axes for mouse UI

    def __init__(self, player_name=''):
        if player_name == '':
            player_name = input("Enter Player Name:")
        self.name = player_name
        self .instructions_presented = False

    def offer_move(self, board, turn, dice):
        if not self.instructions_presented:
            print('Use mouse to select Dice and locations, right click to cancel last selection, middle button to finish')
            self.instructions_presented = True
        print(self.name, ', make your move.')
        if not len(self.axMUI):
            F = plt.gcf
            self.axMUI.append(plt.axes([0, 0, 1, 1], facecolor='none'))
            self.axMUI[0].axis('off')
        plt.sca(self.axMUI[0])
        coordinates = plt.ginput(2 * len(dice), timeout=0)
        moves = xy2moves(coordinates, turn, dice)

        return moves

