import random
from model.example_data import get_suite_data
import numpy as np
import matplotlib.pyplot as plt
import math
from copy import deepcopy
import random

# 不区分前端、边端？

def permute(nums):
    if len(nums) == 1:
        return [nums]
    output = []
    for i in range(len(nums)):
        rest_nums = nums[:i] + nums[i+1:]
        for p in permute(rest_nums):
            output.append([nums[i]] + p)
    return output


def circular_shift(content, n):
    n = len(content) - n % len(content)
    shifted = content[n:] + content[:n]
    return shifted


class GA:
    def __init__(
            self,
            pop_size,
            generation_num,
            suites,
            crossover_rate,
            mutation_rate,
            traffic_core_type,
            cats
    ):
        self.pop_size = pop_size
        self.suite_num = len(suites)

        self.seqs = permute([i for i in range(len(suites))])
        self.seq_size = int(np.ceil(np.sqrt(len(self.seqs))))
        self.trans_size = 3
        self.trans_options = [
            [0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [1, 1], [0, 2], [1, 2]
        ]

        self.suites = deepcopy(suites)

        self.dna_size = self.seq_size + self.trans_size * self.suite_num

        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        self.generation_num = generation_num

        self.traffic_core_type = traffic_core_type

        self.cats = deepcopy(cats)

    def _decode_DNA(self, dna: np.array):
        suites = list()
        seq = dna[:self.seq_size]
        seq_idx = min(len(self.seqs) - 1, int('0b' + ''.join([str(p) for p in seq]), 2))
        seq = self.seqs[seq_idx]
        trans_id = list()
        cats = list()
        for i in range(self.suite_num):
            trans = dna[self.seq_size + i * self.trans_size:
                        self.seq_size + (i + 1) * self.trans_size]
            trans_idx = int('0b' + ''.join([str(p) for p in trans]), 2)
            trans_id.append(trans_idx)
            cats.append(self.cats[seq[i]])
            rotate, flip = self.trans_options[trans_idx]
            suite = self.suites[seq[i]]
            door = circular_shift(suite[:4], rotate)
            balcony = circular_shift(suite[4:8], rotate)
            window = circular_shift(suite[8:12], rotate)
            if flip == 2:
                door[1], door[3] = door[3], door[1]
                balcony[1], balcony[3] = balcony[3], balcony[1]
                window[1], window[3] = window[3], window[1]
            elif flip == 1:
                door[0], door[2] = door[2], door[0]
                balcony[0], balcony[2] = balcony[2], balcony[0]
                window[0], window[2] = window[2], window[0]

            suites.append(door + balcony + window + suite[12:])

        seq_trans = [(seq[i], trans_id[i]) for i in range(len(seq))]
        seq_trans.extend([(seq[-1-i], (trans_id[i] + 4) % len(self.trans_options)) for i in range(len(seq))])
        cat_trans = [(cats[i], trans_id[i]) for i in range(len(cats))]
        cat_trans.extend([(cats[-1-i], (trans_id[i] + 4) % len(self.trans_options)) for i in range(len(cats))])

        return suites, seq_trans, cat_trans

    def compute_fitness(self, pop):
        """
        计算适应度
        """
        fitness = list()

        for dna in pop:
            f = 0
            seq = dna[:self.seq_size]
            seq_idx = min(len(self.seqs) - 1, int('0b' + ''.join([str(p) for p in seq]), 2))
            seq = self.seqs[seq_idx]
            suites, _, cats = self._decode_DNA(dna)
            acc = True

            for i in range(len(suites)):
                suite = suites[i]
                door, balcony, window = suite[:4], suite[4:8], suite[8:12]
                if (i == 0 and (door[2] or door[3] or window[0])) or \
                        (i == len(suites) - 1 and (door[0] or door[3] or window[2])) or \
                        (i == 1 and (door[1] or door[2] or window[0] or window[3])) or \
                        (i == len(suites) - 2 and (door[1] or door[0] or window[2] or window[3])) or \
                        (i == 2 and (door[1] or window[0] or window[2] or window[3])):
                    acc = False
                    f -= 10000
                    break
            if acc:
                # 对称性
                cat = cats[:self.suite_num]
                for i in range(len(cat) // 2):
                    if cat[i][0] == cat[len(cat)-1-i][0] and cat[i][1] == (cat[len(cat)-1-i][1] + 4) % len(self.trans_options):
                        f += 100
                # cao'i
                for i in range(len(suites)):
                    suite0 = suites[i]
                    if suite0[5] == 1:
                        f += 500
                    elif suite0[7] == 1:
                        f -= 0
                    else:
                        f += 400
            fitness.append(f)

        return np.array(fitness)

    def select(self, pop: np.array, fitness: np.array):
        """
        种群选择
        """
        # 根据适应度降序排序
        idx = np.argsort(fitness)[::-1]
        new_pop = pop[idx]
        new_pop[100:] = self.crossover_and_mutate(new_pop[100:])
        if len(pop) < self.pop_size:
            new_pop_ = np.zeros((self.pop_size, self.dna_size), dtype=int)
            new_pop_[:len(pop)] = new_pop
            new_pop_[len(pop):] = np.random.randint(0, 2, size=(self.pop_size - len(pop), self.dna_size))
            new_pop = new_pop_
        random.shuffle(new_pop)

        return new_pop

    def crossover_and_mutate(self, pop):
        """
        交叉
        """
        pop_ = list()
        for father in pop:
            child = father
            if np.random.rand() < self.crossover_rate:
                mother = pop[np.random.randint(len(pop))]
                cross_point = np.random.randint(low=0, high=self.dna_size)
                child[cross_point:] &= mother[cross_point:]
            self._mutate(child)
            pop_.append(child)
        return np.array(pop_)

    def _mutate(self, child):
        """
        变异
        """
        if np.random.rand() < self.mutation_rate:
            mutate_point = np.random.randint(low=0, high=self.dna_size)
            child[mutate_point] ^= 1

    def run(self):
        # init
        pop = np.random.randint(0, 2, size=(self.pop_size, self.dna_size))
        for g in range(self.generation_num):
            pop = np.unique(pop, axis=0)
            fitness = self.compute_fitness(pop)
            # print('generation {}, max fitness: {} of DNA {}'.format(g, max(fitness), pop[fitness.argmax()]))
            pop = self.select(pop, fitness)

        pop = np.unique(pop, axis=0)
        fitness = self.compute_fitness(pop)
        seq_visited = []
        best_seqs = []
        best_cats = []
        for i in range(len(pop)):

            if fitness[i] == max(fitness):
                _, seq_trans, cat_trans = self._decode_DNA(pop[i])
                if cat_trans[:self.suite_num] not in best_cats or cat_trans[self.suite_num:] not in best_cats:
                    # if cat_trans not in best_cats:
                    best_cats.append(cat_trans[:self.suite_num])
                    best_cats.append(cat_trans[self.suite_num:])
                    best_seqs.append(seq_trans[:self.suite_num])

        return best_seqs[np.random.randint(0, len(best_seqs))]

if __name__ == '__main__':
    suite_65B, suite_80A, suite_80B = get_suite_data()
    # door balcony window
    suites = [
        suite_65B[-1], suite_65B[-1], suite_65B[-1], suite_80B[-1], suite_80B[-1],
    ]


    ga = GA(
        pop_size=5000,
        generation_num=500,
        suites=suites,
        crossover_rate=0.5,
        mutation_rate=0.5,
        traffic_core_type=0,
        cats=[0, 0, 0, 1, 1],
    )

    ga.run()
