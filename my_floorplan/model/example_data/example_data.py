import numpy as np
import matplotlib.pyplot as plt


def get_suite_data():
    m = list()

    mask = np.zeros((16, 16))
    mask[4:11, 2:11] = 1.
    mask[5:10, 11] = -2.
    mask[9, 1] = -1.
    plt.imshow(mask)
    plt.show()

    # 除了 16 x 16 的mask，还会用到后面这个12维向量来确定户型的朝向
    m.append(['suite_65B', mask.copy(), [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]])

    mask = np.zeros((16, 16))
    mask[2:13, 4:11] = 1.
    mask[13, 5:10] = -2.
    mask[7:9, 11] = -2.
    mask[3:5, 11] = -2.
    mask[1, 5] = -1.
    plt.imshow(mask)
    plt.show()
    m.append(['suite_80A', mask.copy(), [0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0]])

    mask = np.zeros((16, 16))
    mask[4:12, 3:14] = 1.
    mask[3, 7:13] = -2.
    mask[12, 7:10] = -2.
    mask[12, 11:13] = -2.
    mask[5, 2] = -1.
    plt.imshow(mask)
    plt.show()
    m.append(['suite_80B', mask.copy(), [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1]])

    return m


def get_core_data():

    c = list()
    mask = np.ones((7, 7))
    mask[-1, :] = 0.
    mask[-1, 3] = -1.
    plt.imshow(mask)
    plt.show()
    c.append(['core_1', mask.copy()])

    mask = np.ones((6, 7))
    mask[-1, :] = 0.
    mask[-1, 4] = -1.
    plt.imshow(mask)
    plt.show()
    c.append(['core_2', mask.copy()])

    return c

if __name__ == '__main__':
    get_suite_data()
