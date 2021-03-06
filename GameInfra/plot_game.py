import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
matplotlib.get_backend()
import numpy as np
from apply_move import apply_move


dx = 36
dy = 38
midP = 250
peice_size = 200
img_board = mpimg.imread('GB-5-2.jpg')

F = plt.figure()
ax1 = plt.subplot2grid((3,5), (0,0), colspan=4, rowspan=3)
bkgrnd_plot = ax1.imshow(img_board)

ax_die1 = plt.subplot2grid((3, 5), (0, 4))
ax_die1.axis('off')
ax_die2 = plt.subplot2grid((3, 5), (1, 4))
ax_die2.axis('off')
ax_turn = plt.subplot2grid((3, 5), (2, 4))
ax_turn.axis('off')
ax_turn.text(-0.02, -0.027, 'Turn')


def sct_clr(ax):
    for ob in ax.get_children():
        if isinstance(ob, matplotlib.collections.PathCollection):
            ob.remove()


def dice_init():
    dice_img = mpimg.imread('Cubes.jpg')
    sz = dice_img.shape
    dd = np.ceil(sz[:2]/np.array([3,6]) * 1.04).astype(int)
    dice_imgs = []
    r = 0  # 0
    for i in range(6):
        dice_imgs.append(dice_img[10+r*dd[0]:(r+1)*dd[0]-70, 10+i*dd[1]:(i+1)*dd[1]-70, :])
        # plt.imshow(dice_imgs[i])
    return dice_imgs


dice_imgs = dice_init()


def ij_to_xy_pos(i, j):
    """ converts i,j(absolute value) to x,y coordinates in game image"""
    if 0 < i < 13:
        x_pos = dx * (i) + 8
        if i >= 7:
            x_pos = x_pos + 14
        y_pos = 5 + dx + dy * (j)
    elif 25 > i >= 13:
        x_pos = 23 + dx * (25 - i)
        if i >= 19:
            x_pos = x_pos - 14
        y_pos = 13 * dx - dy * j - 7
    elif i == 0:
        x_pos = midP
        y_pos = midP + (j + 1) * dy
    elif i == 25:
        x_pos = midP
        y_pos = midP - (j + 1) * dy
    else:
        print('what? ', i, j)
    return x_pos, y_pos


def plot_game(board=[0,], plt_block=0.08):

    # ax1.clear()  # clear prev plots
    sct_clr(ax1)

    x = list()
    y = list()
    c = list()
    # dx = 36
    # dy = 38
    # peice_size = 200
    for i in range(26):
        if board[i]:
            for j in range(abs(board[i])):
                x_pos, y_pos = ij_to_xy_pos(i, j)
                x.append(x_pos)
                y.append(y_pos)
                c.append(1 if board[i] >= 1 else 0)  #[1, 1, 1] * 255 *
    sctplot = ax1.scatter(x, y, peice_size, c, vmin=0)
    ax1.axis('off')
    plt.show(block=plt_block >= 10)
    if 0 < plt_block < 10:
        plt.pause(plt_block)


class AnimationStep:
    def __init__(self):
        self.animat_plot = []

    def __call__(self, x_pos, y_pos, sign):
        if type(self.animat_plot) is not list and self.animat_plot.axes is not None:
            self.animat_plot.remove()
        self.animat_plot = ax1.scatter(x_pos, y_pos, peice_size, (1 if sign == 1 else 0), vmin=0)
        ax1.axis('off')
        plt.show(block=False)
        plt.pause(0.000005)
        # animat_plot.remove()


animation_step = AnimationStep()


def animation_steps(x_pos_0, y_pos_0, x_pos_1, y_pos_1, sign, n_steps=5):
    for i in range(1, n_steps + 1):
        x_pos = x_pos_0 + i * (x_pos_1 - x_pos_0) / (n_steps )
        y_pos = y_pos_0 + i * (y_pos_1 - y_pos_0) / (n_steps )
        animation_step(x_pos, y_pos, sign)


def animate_move(board, moves):
    board = board.copy()

    for mov in moves:
        if mov[0] is not None:
            board_animat = board.copy()
            sign = int(board[mov[0]] / abs(board[mov[0]]))
            board_animat[mov[0]] -= sign  # remove the piece
            plot_game(board_animat, plt_block=0)
            x_pos_0, y_pos_0 = ij_to_xy_pos(mov[0], abs(board[mov[0]]))
            if mov[0] not in [0, 25]:
                if 0 < mov[0] + mov[1] < 25:  # don't animate taking out pegs
                    for i in range(sign, mov[1] + sign, sign):
                        j = abs(board_animat[mov[0]+i])
                        x_pos_1, y_pos_1 = ij_to_xy_pos(mov[0]+i, j)
                        animation_steps(x_pos_0, y_pos_0, x_pos_1, y_pos_1, sign, n_steps=2)
                        x_pos_0, y_pos_0 = x_pos_1, y_pos_1

            else:  # animate prison escapes differently:
                x_pos_0, y_pos_0 = ij_to_xy_pos(mov[0], abs(board[mov[0]]))
                x_pos_1, y_pos_1 = ij_to_xy_pos(mov[0] + mov[1], abs(board[mov[0] + mov[1]]))
                animation_steps(x_pos_0, y_pos_0, x_pos_1, y_pos_1, sign, n_steps=5)

            board, illegal_move = apply_move(board, sign, [abs(mov[1])], [mov])
            # plot_game(board)


def plot_dice(dice):
    for im in ax_die1.images:
        im.remove()
    ax_die1.imshow(dice_imgs[dice[0] - 1])
    for im in ax_die2.images:
        im.remove()
    ax_die2.imshow(dice_imgs[dice[1] - 1])
    plt.show(block=False)


def show_whos_turn(sign):
    sct_clr(ax_turn)
    ax_turn.scatter(0, 0, 400, (1 if sign == 1 else 0), vmin=0)

    plt.show(block=False)


def dice_image():
    pass


def counts_histogram(rounds_log, game_log, name1=None, name2=None):
    plt.figure()
    plt.suptitle('Turn count histograms')
    plt.subplot(3, 1, 1)
    plt.hist(rounds_log, range(30, 150, 2))

    plt.subplot(3, 1, 2).set_title(name1)
    p1_turns = rounds_log[game_log > 0]
    plt.hist(p1_turns, range(38, 142, 2))
    print(f'player1 {name1} wins turn count Mean:{p1_turns.mean()} Median:{np.median(p1_turns)}')

    plt.subplot(3, 1, 3).set_title(name2)
    p2_turns = rounds_log[game_log < 1]
    plt.hist(p2_turns, range(38, 142, 2))
    print(f'player2 {name2} wins turn count Mean:{p2_turns.mean()} Median:{np.median(p2_turns)}')

    plt.show()


    ''' from PIL import Image
    image = Image.open('GB-5-2.jpg')
    image.show()
    input("Press Enter to continue...")  # wait for enter'''



    '''plt.figure()
    
    plt.imshow()
    plt.show()  # display it'''


#plot_game()