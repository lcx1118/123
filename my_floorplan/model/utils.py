from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_fill_holes
from typing import List
from model.entity import Entity


def get_perimeter(matrix: np.array):
    """
    calculate the perimeter of matrix
    :param matrix:
    :return:
    """
    rows, cols = matrix.shape
    perimeter = 0
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                # 检查上方像素
                if i == 0 or matrix[i - 1][j] == 0:
                    perimeter += 1
                # 检查下方像素
                if i == rows - 1 or matrix[i + 1][j] == 0:
                    perimeter += 1
                # 检查左方像素
                if j == 0 or matrix[i][j - 1] == 0:
                    perimeter += 1
                # 检查右方像素
                if j == cols - 1 or matrix[i][j + 1] == 0:
                    perimeter += 1

    return perimeter


def is_valid(x, y, matrix):
    # 检查当前位置是否在矩阵范围内，并且不是障碍物
    if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y] != 1:
        return True
    return False


def calculate_distance(matrix, start_x, start_y, dist):
    distances = [[float('inf') for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    distances[start_x][start_y] = 0
    queue = deque([(start_x, start_y)])

    while queue:
        curr_x, curr_y = queue.popleft()

        # 检查上下左右四个方向
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]

        for i in range(4):
            new_x = curr_x + dx[i]
            new_y = curr_y + dy[i]

            if is_valid(new_x, new_y, matrix):
                # 更新距离
                if distances[new_x][new_y] > distances[curr_x][curr_y] + 1:
                    distances[new_x][new_y] = distances[curr_x][curr_y] + 1
                    queue.append((new_x, new_y))

    result = dict()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if distances[i][j] <= dist:
                result[(i, j)] = distances[i][j]

    return result


def is_pos_valid(x, y, matrix):
    # 检查当前位置是否在矩阵范围内，并且不是障碍物
    if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y] != 1:
        return True
    return False


def is_reachable(matrix, start_x, start_y, target_x, target_y):
    visited = np.zeros(matrix.shape, dtype=bool)
    visited[start_x][start_y] = True

    queue = deque([(start_x, start_y)])

    while queue:
        curr_x, curr_y = queue.popleft()

        # 检查上下左右四个方向
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]

        if curr_x == target_x and curr_y == target_y:
            return True

        for i in range(4):
            new_x = curr_x + dx[i]
            new_y = curr_y + dy[i]

            if is_pos_valid(new_x, new_y, matrix) and not visited[new_x][new_y]:
                visited[new_x][new_y] = True
                queue.append((new_x, new_y))

    return False


def fill_floor(input_matrix):
    # 创建结构元素用于填充操作
    struct_element = np.ones((3, 3), dtype=int)
    # 使用二维卷积进行膨胀操作（填充）
    output_matrix = binary_fill_holes(input_matrix)

    # 打印结果
    # print(output_matrix)
    return output_matrix


def plot_suite_seq(suites: List[Entity]):
    seq = np.zeros((16 * len(suites) + 1, 16))
    for i, suite in enumerate(suites):
        seq[i * 16: (i + 1) * 16, :] = np.where(suite.mask == 1, suite.color, suite.mask)

    seq = np.where(seq == -1, 3, seq)
    seq = np.where(seq == 0., 8., seq)
    seq = np.where(seq == -2, 0, seq)

    seq[-1, 0] = 0
    seq[-1, 1] = 1
    seq[-1, 2] = 2
    seq[-1, 3] = 7
    seq[-1, 4] = 10

    plt.imshow(seq, cmap='Set3')
    plt.axis('off')
    plt.show()


def plot_suite_seq_(suites: List[Entity]):
    seq = np.zeros((33, 32))
    for i, suite in enumerate(suites):
        if i == 0:
            seq[:16, :16] = np.where(suite.mask == 1, suite.color, suite.mask)
        elif i == 1:
            seq[16:32, :16] = np.where(suite.mask == 1, suite.color, suite.mask)
        elif i == 2:
            seq[16:32, 16:] = np.where(suite.mask == 1, suite.color, suite.mask)
        else:
            seq[:16, 16:] = np.where(suite.mask == 1, suite.color, suite.mask)

    seq = np.where(seq == -1, 3, seq)
    seq = np.where(seq == -2, 0, seq)
    seq = np.where(seq == 0., 8., seq)

    seq[32, 0] = 0
    seq[32, 1] = 1
    seq[32, 2] = 2
    seq[32, 3] = 7
    seq[32, 4] = 10

    plt.imshow(seq, cmap='Set3')
    plt.axis('off')
    plt.show()

