import matplotlib.pyplot as plt
import matplotlib.image as mpimg

dx = 36
dy = 38
midP = 250
peice_size = 200

F = plt.figure()


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

     return x_pos, y_pos


def plot_game(board=[0,], plt_block=False):

    F.clear()  # clear prev plots
    img = mpimg.imread('GB-5-2.jpg')
    imgplot = plt.imshow(img)

    x = list()
    y = list()
    c = list()
    # dx = 36
    # dy = 38
    # peice_size = 200
    for i in range(1, 25):
        if board[i]:
            for j in range(abs(board[i])):
                if i < 13:
                    x_pos = dx * (i) + 8
                    if i >= 7:
                        x_pos = x_pos + 14
                    y_pos = 5 + dx + dy * (j)
                else:
                    x_pos = 23 + dx * (25 - i)
                    if i >= 19:
                        x_pos = x_pos - 14
                    y_pos = 13 * dx - dy * j - 7
                x.append(x_pos)
                y.append(y_pos)
                c.append(1 if board[i] >= 1 else 0)  #[1, 1, 1] * 255 *
    # midP = 250
    if board[0]:
        for i in range(board[0]):
            x.append(midP)
            y.append(midP + (i+1)*dy)
            c.append(1)
    if board[25]:
        for i in range(-board[25]):
            x.append(midP)
            y.append(midP - (i+1)*dy)
            c.append(0)
    sctplot = plt.scatter(x, y, peice_size, c)
    plt.show(block=plt_block)
    plt.pause(0.1)



    ''' from PIL import Image
    image = Image.open('GB-5-2.jpg')
    image.show()
    input("Press Enter to continue...")  # wait for enter'''



    '''plt.figure()
    
    plt.imshow()
    plt.show()  # display it'''


#plot_game()