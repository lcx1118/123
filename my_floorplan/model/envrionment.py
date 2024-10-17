import os

import numpy as np
from copy import deepcopy
from model.entity import Entity
from typing import List
from model.utils import calculate_distance, get_perimeter, is_reachable, fill_floor
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt
import datetime

class Environment:
    def __init__(
            self,
            env_x,
            env_y,
            core: Entity,
            suites: List[Entity],
            corridor_len_max: List[int],
    ):
        self.env_x = env_x
        self.env_y = env_y
        self.env = np.zeros((env_y, env_x))
        self.env_empty = np.zeros((env_y, env_x))
        self.env_clash = np.zeros((env_y, env_x))
        self.env_full = np.zeros((env_y, env_x))
        self.potential_mask = dict()

        self.window_masks = [np.zeros((env_y, env_x)) for _ in range(len(suites))]

        self.core = deepcopy(core)
        self.suites = deepcopy(suites)
        self.corridor_len_max = deepcopy(corridor_len_max)
        self.pos = None
        self._pos = None

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self.search_space_potential = dict()
        self._init_suite_pos = dict()
        self._get_search_region()

        # self.reward_entrance_potential = lambda p: 0.5 / (p - self.corridor_len_max - 1)
        self.reward_entrance_potential = lambda p: 0.5 * p
        self.reward_surface_potential = lambda p: 0.2 * p
        self.reward_corridor_ratio = lambda cr: 0.2 / cr
        self.reward_shape_factor = lambda sf: 0.3 / sf
        self.reward_natural_lighting = lambda er: er * 0.2

    # work with the GA
    def get_fitness_init(self, transformations, locations):
        suites = deepcopy(self.suites)
        env = self.env_empty.copy()
        fitness = 0
        for i, suite in enumerate(suites):
            trans = transformations[i]
            y, x = locations[i]
            y_mask = y - suite.door[0]
            x_mask = x - suite.door[1]
            suite.step(trans)
            env[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += suite.mask
            if np.count_nonzero(env > 1):
                fitness -= 10000
                break

    def get_init_pos(self):
        tmp_env = self.env.copy()
        for i, suite in enumerate(self.suites):
            for (y, x) in self._init_suite_pos[suite.core]:
                y_mask = y - suite.door[0]
                x_mask = x - suite.door[1]
                tmp_env[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += suite.mask

    def init_pos(self, pos):
        self.pos = deepcopy(pos)
        for i, suite in enumerate(self.suites):
            suite.y, suite.x = pos[i]
            y_mask = suite.y - suite.door[0]
            x_mask = suite.x - suite.door[1]
            self.env[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += suite.mask

        # self.plot()
        self._pos = deepcopy(pos)

    def init_pos_(self, boundary: List):
        # print(boundary)
        boundary.sort(key=lambda x: x[1])
        # print(boundary)
        idx = np.linspace(0, len(boundary) - 1, len(self.suites), dtype=int)
        # print(idx)
        is_compatible = False
        while not is_compatible:
            env = self.env_empty.copy()
            is_compatible = True
            for i, suite in enumerate(self.suites):
                # print(i, boundary[idx[i]])
                suite.y, suite.x = boundary[idx[i]]
                y_mask = suite.y - suite.door[0]
                x_mask = suite.x - suite.door[1]
                env[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += suite.mask
                if np.count_nonzero(env[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] > 1):
                    is_compatible = False
                    if i < len(self.suites) / 2:
                        idx[i] -= 1
                    else:
                        idx[i] += 1

        self.init_pos([boundary[idx[i]] for i in range(len(self.suites))])

    def _get_core_potential_field(self, max_dist=6):
        # 使用 distance_transform_edt 计算欧氏距离变换
        distance_field = distance_transform_edt(1 - self.env_empty)
        # 将大于最大距离的值截断为最大距离
        potential_field = np.minimum(distance_field, max_dist)
        potential_field = max_dist - potential_field


        return potential_field

    def _get_agent_potential_field(self, max_dist=6):
        fields = list()
        for suite in self.suites:
            empty = np.zeros((self.env_y, self.env_x))
            mask_y = suite.y - suite.door[0]
            mask_x = suite.x - suite.door[1]
            empty[mask_y:mask_y + suite.mask.shape[0], mask_x:mask_x + suite.mask.shape[1]] += suite.mask

            # 使用 distance_transform_edt 计算欧氏距离变换
            distance_field = distance_transform_edt(1 - empty)
            # 大于最大距离的值截断为最大距离
            potential_field = np.minimum(distance_field, max_dist)
            potential_field = max_dist - potential_field
            # potential_field = np.where(potential_field == max_dist, 0, potential_field)
            # plt.imshow(potential_field)
            # plt.colorbar()
            # plt.show()
            fields.append(potential_field)

        return fields

    def _get_search_region(self):
        """
        based on Manhattan distance
        """
        my, mx = self.core.mask.shape
        x = (self.env_x - mx) // 2
        y = (self.env_y - my) // 2
        self.core.x = x
        self.core.y = y
        for suite in self.suites:
            suite.core = (y + self.core.door[0], x + self.core.door[1])

        self.env[y:y + my, x:x + mx] += self.core.mask
        self.env_empty = self.env.copy()
        self.env_clash = self.env.copy()
        mask = np.zeros((self.env_y, self.env_x))
        mask = np.where(mask == 0, 100, 100)
        sx = list()
        sy = list()
        for i, entry in enumerate(self.core.entry):
            res = calculate_distance(self.env, y + entry[0], x + entry[1], self.corridor_len_max[i])
            boundary = list()
            self.potential_mask[(y + entry[0], x + entry[1])] = np.where(self.env_empty == 0, -1, -1)
            self._init_suite_pos[(y + entry[0], x + entry[1])] = list()
            # {(y, x): dist}
            for item in res:
                sy.append(item[0])
                sx.append(item[1])
                if res[item] == self.corridor_len_max[i]:
                    # print(item)
                    self._init_suite_pos[(y + entry[0], x + entry[1])].append(res[item])
                    if item[0] >= y + entry[0]:
                        boundary.append(item)
                self.potential_mask[(y + entry[0], x + entry[1])][item] = max(
                    self.potential_mask[(y + entry[0], x + entry[1])][item], res[item]) \
                    if self.potential_mask[(y + entry[0], x + entry[1])][item] != -1 \
                    else res[item]
                # print(item)
            # print((y + entry[0], x + entry[1]), 'entry')
            self.init_pos_(boundary)
            self.potential_mask[(y + entry[0], x + entry[1])] = self.corridor_len_max[i] - self.potential_mask[
                (y + entry[0], x + entry[1])]
            self.potential_mask[(y + entry[0], x + entry[1])] = np.where(
                self.potential_mask[(y + entry[0], x + entry[1])] == self.corridor_len_max[i] + 1, -1,
                self.potential_mask[(y + entry[0], x + entry[1])])

            if i == 0:
                mask = self.corridor_len_max[i] - self.potential_mask[(y + entry[0], x + entry[1])] + 1
            else:
                mask = np.where(mask == self.corridor_len_max[i - 1] + 2,
                                self.corridor_len_max[i] - self.potential_mask[(y + entry[0], x + entry[1])] + 1, mask)
                mask = np.where(mask < self.corridor_len_max[i] - self.potential_mask[(y + entry[0], x + entry[1])] + 1,
                                mask, self.corridor_len_max[i] - self.potential_mask[(y + entry[0], x + entry[1])] + 1)

            # mask = self.corridor_len_max[i] - mask + 1

        self.min_x = min(sx)
        self.min_y = min(sy)
        self.max_x = max(sx)
        self.max_y = max(sy)

    def reset(self):
        """
        reset
        """
        self.env = np.zeros((self.env_y, self.env_x))
        self.env_full = np.zeros((self.env_y, self.env_x))
        my, mx = self.core.mask.shape
        x = (self.env_x - mx) // 2
        y = (self.env_y - my) // 2
        self.core.update(x + self.core.door[1], y + self.core.door[0])
        self.env[y:y + my, x:x + mx] += self.core.mask
        self.env_full[y:y + my, x:x + mx] += self.core.mask
        self.env_clash = np.where(self.env == -1, 0, self.env)
        self.window_masks = [np.zeros((self.env_y, self.env_x)) for _ in range(len(self.suites))]

        peer_masks = list()
        # get initial state
        states = np.zeros((len(self.suites), 3, self.env_y, self.env_x))
        self.pos = deepcopy(self._pos)
        for i, (y, x) in enumerate(self.pos):
            self.suites[i].y, self.suites[i].x = y, x
            y_mask, x_mask = y - self.suites[i].door[0], x - self.suites[i].door[1]
            mask = np.where(self.suites[i].mask == -2, 0, self.suites[i].mask)
            clash_mask = np.where(self.suites[i].mask == -2, 1, self.suites[i].mask)
            clash_mask = np.where(clash_mask == -1, 1, clash_mask)
            self.env_full[y_mask:y_mask + self.suites[i].mask.shape[0], x_mask:x_mask + self.suites[i].mask.shape[1]] += \
                self.suites[i].mask
            self.env[y_mask:y_mask + self.suites[i].mask.shape[0], x_mask:x_mask + self.suites[i].mask.shape[1]] += mask
            self.env_clash[y_mask:y_mask + self.suites[i].mask.shape[0],
            x_mask:x_mask + self.suites[i].mask.shape[1]] += self.suites[i].mask

        for i, (y, x) in enumerate(self.pos):
            self.suites[i].y, self.suites[i].x = y, x
            y_mask, x_mask = y - self.suites[i].door[0], x - self.suites[i].door[1]
            clash_mask = np.where(self.suites[i].mask == -2, 1, self.suites[i].mask)
            clash_mask = np.where(clash_mask == -1, 1, clash_mask)

            self_mask = np.zeros((self.env_y, self.env_x))
            self_mask[y_mask:y_mask + self.suites[i].mask.shape[0], x_mask:x_mask + self.suites[i].mask.shape[1]] += \
                self.suites[i].mask
            # peer_mask = self.env_clash - self.env_empty - self_mask
            peer_mask = self.env_full.copy()
            peer_mask[y_mask:y_mask + self.suites[i].mask.shape[0], x_mask:x_mask + self.suites[i].mask.shape[1]] -= \
                self.suites[i].mask
            peer_mask[y:y + my, x:x + mx] -= self.core.mask
            states[i, 0, :, :] = np.where(self_mask < -1, -1, self_mask)
            states[i, 1, :, :] = self.env_empty
            states[i, 2, :, :] = np.where(peer_mask < -1, -1, peer_mask)

        self.env_clash = np.where(self.env_clash < 0, 1, self.env_clash)

        return states

    def observe(self, idx):
        state = np.zeros((3, self.env_y, self.env_x))
        suite = self.suites[idx]
        y_mask, x_mask = suite.y - suite.door[0], suite.x - suite.door[1]

        self_mask = np.zeros((self.env_y, self.env_x))
        self_mask[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += suite.mask
        # peer_mask = self.env_clash - self.env_empty - self_mask
        peer_mask = self.env_full.copy()
        peer_mask[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] -= suite.mask
        peer_mask[
        self.core.y - self.core.door[0]:self.core.y - self.core.door[0] + self.core.mask.shape[0],
        self.core.x - self.core.door[1]:self.core.x - self.core.door[1] + self.core.mask.shape[1]
        ] -= self.core.mask
        state[0, :, :] = np.where(self_mask < -1, -1, self_mask)
        state[1, :, :] = self.env_empty
        state[2, :, :] = np.where(peer_mask < -1, -1, peer_mask)

        return state

    def check_reachable(self, tmp_env, idx, y_, x_):
        reachable = True
        for i, suite in enumerate(self.suites):
            if i == idx:
                y = y_
                x = x_
            else:
                y = int(suite.y)
                x = int(suite.x)
            ey = int(suite.core[0])
            ex = int(suite.core[1])
            if y < ey:
                start_y = 0
                target_y = ey - y
            else:
                start_y = y - ey
                target_y = 0
            if x < ex:
                start_x = 0
                target_x = ex - x
            else:
                start_x = x - ex
                target_x = 0

            reachable = is_reachable(
                tmp_env[
                min(y, ey):max(y, ey) + 1,
                min(x, ex):max(x, ex) + 1
                ], start_y, start_x, target_y, target_x
            )
            if not reachable:
                break

        return reachable

    def step(self, action, idx, pos=None):
        """
        take the action, get the new state

        """
        if pos is None:
            pos_ = deepcopy(self.pos)
        else:
            pos_ = deepcopy(pos)

        reward = 0
        adj = False
        suite = self.suites[idx]
        potential_old = self.potential_mask[suite.core][suite.y, suite.x]

        y_mask, x_mask = suite.y - suite.door[0], suite.x - suite.door[1]
        mask = np.where(suite.mask == -2, 0, suite.mask)
        clash_mask = np.where(suite.mask == -2, 1, suite.mask)
        clash_mask_ = np.where(clash_mask == -1, 1, clash_mask)
        # clash_mask = np.where(clash_mask == -1, 1, clash_mask)

        self.env[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] -= mask
        self.env_clash = np.where(self.env < 0, 1, self.env)
        # self.env_clash[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] -= clash_mask_
        self.env_full[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] -= suite.mask

        tmp_env = self.env.copy()
        tmp_env_clash = self.env_clash.copy()
        tmp_env_full = self.env_full.copy()

        y_, x_ = suite.y, suite.x  # position of door in the env
        if action == 1:  # up
            y_ -= 1
        elif action == 2:  # down
            y_ += 1
        elif action == 3:  # left
            x_ -= 1
        elif action == 4:  # right
            x_ += 1
        else:
            pass
        y_mask, x_mask = y_ - suite.door[0], x_ - suite.door[1]

        tmp_env[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += mask
        tmp_env_clash[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += clash_mask
        tmp_env_full[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += suite.mask

        # check if action is valid
        valid_action = True
        # out of search space
        if self.potential_mask[suite.core][y_, x_] == -1:
            reward -= 1.
            valid_action = False
        # clash
        elif np.count_nonzero(tmp_env_clash > 1) > 0 or tmp_env_full[y_, x_] > -1 or (
                tmp_env[y_, x_] < 0 and tmp_env_full[y_, x_] < -2):
            reward -= 1.
            valid_action = False
            # done = True
        else:
            if not self.check_reachable(tmp_env, idx, y_, x_):
                reward -= 1.
                valid_action = False

        if valid_action:
            suite.y = y_
            suite.x = x_

        y_mask, x_mask = suite.y - suite.door[0], suite.x - suite.door[1]

        self.env[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += mask
        self.env_clash = np.where(self.env < 0, 1, self.env)
        self.env_full[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += suite.mask

        pos_[idx] = (suite.y, suite.x)

        tmp_window_mask = np.zeros((self.env_y, self.env_x))
        tmp_window_mask[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += suite.mask
        windows_y, windows_x = np.where(tmp_window_mask == -2)
        for window_y, window_x in zip(windows_y, windows_x):
            if tmp_window_mask[window_y + 1, window_x] == 0 and tmp_window_mask[window_y - 1, window_x] == 1:
                """
                inside
                ------
                outside
                """
                tmp_window_mask[window_y + 1:, window_x] = -2.
            elif tmp_window_mask[window_y + 1, window_x] == 1 and tmp_window_mask[window_y - 1, window_x] == 0:
                """
                outside
                ------
                inside
                """
                tmp_window_mask[:window_y, window_x] = -2.
            elif tmp_window_mask[window_y, window_x + 1] == 1 and tmp_window_mask[window_y, window_x - 1] == 0:
                """
                outside | inside
                """
                tmp_window_mask[window_y, :window_x] = -2.

            elif tmp_window_mask[window_y, window_x + 1] == 0 and tmp_window_mask[window_y, window_x - 1] == 1:
                """
                inside | outside
                """
                tmp_window_mask[window_y, window_x + 1:] = -2.

            else:
                pass
        tmp_window_mask[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] -= suite.mask
        self.window_masks[idx] = tmp_window_mask
        # plt.imshow(tmp_window_mask)
        # plt.show()

        if valid_action:
            potential_new = self.potential_mask[suite.core][suite.y, suite.x]
            # reward += (potential_new - potential_old)
            # reward += (potential_new / self.corridor_len_max)
            reward += self.reward_entrance_potential(potential_new - potential_old)
            # reward += self.reward_entrance_potential(potential_new)
            # calculate suite potential
            fields = self._get_agent_potential_field(max_dist=4)
            bounds = self._get_agent_potential_field(max_dist=1)
            attachment_field = self._get_core_potential_field(max_dist=4)
            attachment_check = self._get_core_potential_field(max_dist=1)
            for i in range(len(fields)):
                if idx != i:
                    attachment_field += fields[i]
                    attachment_check += bounds[i]
            boundary_mask = self._get_agent_potential_field(max_dist=2)[idx]
            # boundary_mask = np.where(boundary_mask == 2, 0, boundary_mask)
            # 本来用的这个，包括角点的外轮廓
            # boundary_mask = np.where(boundary_mask != 0)
            # 只是把所有边都包围起来，不包括角点
            boundary_mask = np.where(boundary_mask == 1)
            # surface_potential = np.sum(attachment_field[boundary_mask])
            # reward += (surface_potential / 100)
            # 更新 surface potential 为 表面场强的均值
            surface_potential = np.average(attachment_field[boundary_mask])
            reward += self.reward_surface_potential(surface_potential)
            if np.count_nonzero(attachment_check[boundary_mask] >= 1) > 0:
                # self.plot()
                adj = True

        # offset = [[pos_[idx][0] - suite.core[0], pos_[idx][1] - suite.core[1]]]
        # offset.extend([[pos_[idx][0] - p[0], pos_[idx][1] - p[1]] for p in pos_])
        # offset = np.array(offset)
        # offset = offset / max(self.corridor_len_max)
        state_ = np.zeros((3, self.env_y, self.env_x))
        self_mask = np.zeros((self.env_y, self.env_x))
        self_mask[y_mask:y_mask + self.suites[idx].mask.shape[0],
        x_mask:x_mask + self.suites[idx].mask.shape[1]] += suite.mask
        # peer_mask = self.env_clash - self.env_empty - self_mask
        peer_mask = self.env_full.copy()
        peer_mask[y_mask:y_mask + self.suites[idx].mask.shape[0],
        x_mask:x_mask + self.suites[idx].mask.shape[1]] -= suite.mask
        my, mx = self.core.mask.shape
        peer_mask[(self.env_y - my) // 2:(self.env_y - my) // 2 + my,
        (self.env_x - mx) // 2:(self.env_x - mx) // 2 + mx] -= self.core.mask

        state_[0, :, :] = np.where(self_mask < -1, -1, self_mask)
        state_[1, :, :] = self.env_empty
        state_[2, :, :] = np.where(peer_mask < -1, -1, peer_mask)

        self.pos = pos_

        return reward, state_, adj, valid_action

    def eval(self):
        # evaluate
        my, mx = self.core.mask.shape
        x = (self.env_x - mx) // 2
        y = (self.env_y - my) // 2
        eval_mask = self.env.copy()
        for i, suite in enumerate(self.suites):
            # for cy, cx in self.core.entry:
            eval_mask[
            min(suite.y, suite.core[0]):max(suite.y, suite.core[0]) + 1,
            min(suite.x, suite.core[1]):max(suite.x, suite.core[1]) + 1
            ] = 1

        # eval_mask = fill_floor(eval_mask)

        corridor_mask = eval_mask - self.env

        corridor_mask = np.where(corridor_mask > 1, 1, corridor_mask)
        corridor_area = np.count_nonzero(corridor_mask == 1)
        total_area = np.count_nonzero(self.env > 0)
        suite_area = total_area - np.count_nonzero(self.core.mask == 1)

        perimeter = get_perimeter(eval_mask)
        shape_factor = perimeter / (total_area + corridor_area)
        corridor_ratio = (corridor_area + np.count_nonzero(self.core.mask == 1)) / suite_area

        # natural lighting
        window_len = 0.
        window_len_ = 0.
        for i, suite in enumerate(self.suites):
            window_mask = np.where(self.window_masks[i] == -2, -10, self.window_masks[i]) + np.where(self.env < 0, 1,
                                                                                                     self.env)
            wy, wx = np.where(self.window_masks[i] == -2)
            wy_, wx_ = np.where(window_mask == -9)
            wy = set(wy.tolist())
            wx = set(wx.tolist())
            wy_ = set(wy_.tolist())
            wx_ = set(wx_.tolist())
            if len(wy) < len(wx):
                window_len += len(wy)
                window_len_ += (len(wy) - len(wy_))
            else:  # len(wy) >= len(wx):
                window_len += len(wx)
                window_len_ += (len(wx) - len(wx_))
            # print(window_len, window_len_)
            # plt.imshow(np.hstack((window_mask, self.window_masks[i])))
            # plt.show()
        if window_len == 0:
            natural_lighting = 0
        else:
            natural_lighting = window_len_ / window_len
            # natural_lighting = 0

        # print(shape_factor, corridor_ratio)
        # plt.imshow(eval_mask)
        # plt.show()
        # plt.imshow(corridor_mask)
        # plt.show()
        return self.reward_shape_factor(shape_factor) * 0. + \
               self.reward_corridor_ratio(corridor_ratio) * 1. + \
               self.reward_natural_lighting(natural_lighting), shape_factor, corridor_ratio, natural_lighting

    def plot(self, pos=None):
        if pos is None:
            pos = self.pos
        env_display = np.zeros((self.env_y, self.env_x))

        # add traffic core
        my, mx = self.core.mask.shape
        x = (self.env_x - mx) // 2
        y = (self.env_y - my) // 2
        env_display[y:y + my, x:x + mx] += self.core.mask
        env_display = np.where(env_display == 1, 4, env_display)

        # add suite one after another
        for i, suite in enumerate(self.suites):
            y_mask, x_mask = pos[i][0] - suite.door[0], pos[i][1] - suite.door[1]
            mask = np.where(suite.mask == -2, 0, suite.mask)
            env_display[y_mask:y_mask + suite.mask.shape[0], x_mask:x_mask + suite.mask.shape[1]] += mask
            env_display = np.where(env_display == 1, suite.color, env_display)

        env_display = np.where(env_display < 0, 3, env_display)
        env_display = np.where(env_display == 0., 8., env_display)
        env_display[0, 0] = 0
        env_display[0, 1] = 1
        env_display[0, 2] = 2
        env_display[0, 3] = 7
        env_display[0, 4] = 10
        plt.imshow(env_display, cmap='Set3')
        plt.axis('off')
        # plt.savefig("D:\\Users\\43171\\PycharmProjects\\my_floorplan\\media\\GeneratedImage\\output_image.png")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, "../media/GeneratedImage", f"output_image_{timestamp}.png")
        # filename = f"..//media/GeneratedImage/output_image_{timestamp}.png"
        plt.savefig(filename)
        plt.close()
        return timestamp