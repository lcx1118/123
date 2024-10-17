import numpy as np
import matplotlib.pyplot as plt


def get_suite_data(image_names):
    m = list()

    mask = np.zeros((16, 16))
    mask[4:11, 2:11] = 1.
    mask[5:10, 11] = -2.
    mask[9, 1] = -1.
    # plt.imshow(mask)
    # plt.show()
    c = image_names.count('65B')
    for i in range(c):
    # 除了 16 x 16 的mask，还会用到后面这个12维向量来确定户型的朝向
        m.append(['suite_65B', mask.copy(), [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]])

    mask = np.zeros((16, 16))
    mask[2:13, 4:11] = 1.
    mask[13, 5:10] = -2.
    mask[7:9, 11] = -2.
    mask[3:5, 11] = -2.
    mask[1, 5] = -1.
    # plt.imshow(mask)
    # plt.show()
    # if '80A' in image_names:
    c = image_names.count('80A')
    for i in range(c):
        m.append(['suite_80A', mask.copy(), [0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0]])

    mask = np.zeros((16, 16))
    mask[4:12, 3:14] = 1.
    mask[3, 7:13] = -2.
    mask[12, 7:10] = -2.
    mask[12, 11:13] = -2.
    mask[5, 2] = -1.
    # plt.imshow(mask)
    # plt.show()
    # if '80B' in image_names:
    c = image_names.count('80B')
    for i in range(c):
        m.append(['suite_80B', mask.copy(), [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1]])

    return m


def get_core_data(image_names):
    c = list()
    # if '65B_1' in image_names:
    co = image_names.count('65B_1')
    for i in range(co):
        mask = np.ones((7, 7))
        mask[-1, :] = 0.
        mask[-1, 3] = -1.
        plt.imshow(mask)
        plt.show()
        c.append(['core_1', mask.copy()])
    # if '80A_1' in image_names:
    co = image_names.count('80A_1')
    for i in range(co):
        mask = np.ones((6, 7))
        mask[-1, :] = 0.
        mask[-1, 4] = -1.
        plt.imshow(mask)
        plt.show()
        c.append(['core_2', mask.copy()])

    return c

if __name__ == '__main__':
    get_suite_data()
