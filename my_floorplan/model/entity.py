import numpy as np
import matplotlib.pyplot as plt


class Entity:
    def __init__(self, mask: np.array, entity_type, core=None, color=None, door=None):
        self.mask = mask.copy()

        if entity_type == 'core':
            dy, dx = np.where(mask == -1)
            self.entry = [[y, x] for y, x in zip(dy, dx)]

            # position of the first door in the mask
            self.door = np.array(self.entry[0])

        else:
            dy, dx = np.where(mask == -1)
            self.entry = [dy[0], dx[0]]
            self.door = [dy[0], dx[0]]

        self.core = core

        # position of the first door in the environment
        self.x = 0
        self.y = 0

        # color
        if color is not None:
            self.color = color
        else:
            color = 0

    def update(self, x, y, mask_=None):
        """

        :param mask_: new mask of entity
        :param x: new x coordinate of door
        :param y: new y coordinate of door
        :return:
        """
        if mask_ is not None:
            self.mask = mask_.copy()
        self.x = x
        self.y = y

    def step(self, shape: int, m=None, d=None):
        """
        take a step and get the new mask
        :param shape:
        :return:
        """
        if m is None:
            mask = self.mask.copy()
            door = self.door.copy()
        else:
            mask = m.copy()
            door = d.copy()

        mask[door[0], door[1]] = 2.

        options = [
            [0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [1, 1], [0, 2], [1, 2]
        ]
        angle, axis = options[shape]
        mask = self.flip(self.rotate(mask, angle), axis)
        # mask = self.rotate(self.flip(mask, axis), angle)

        # get new door position
        dy, dx = np.where(mask == 2.)
        self.door = np.array([dy[0], dx[0]])
        self.mask = np.where(mask == 2., -1., mask)

        # door = np.array([dy[0], dx[0]])
        # mask = np.where(mask == 2., -1., mask)
        #
        # return mask, door

    def rotate(self, m, angle):
        """
        rotate entity
        :param m:
        :param angle:
        :return:
        """
        mask = m.copy()
        if angle == 1:    # clockwise 90 degree
            mask = mask[::-1].T
        elif angle == 2:    # clockwise 180 degree
            temp = mask.reshape(1, int(mask.size))
            mask = temp[0][::-1].reshape(mask.shape)
        elif angle == 3:    # clockwise 270 degree
            mask = mask.T[::-1]
        else:
            pass
        return mask

    def flip(self, m, axis):
        """
        flip entity either horizontally or vertically
        will result in different mask and door position
        :param m:
        :param axis:
        :return:
        """
        mask = m.copy()

        if axis == 1:       # horizontal flip
            mask = self.rotate(m, 2)[::-1]
        elif axis == 2:     # vertical flip
            mask = mask[::-1]
        else:
            pass

        return mask
