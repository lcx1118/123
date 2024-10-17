from model.envrionment import Environment
from model.entity import Entity
from model.agent_dqn import Agent

import numpy as np
import matplotlib.pyplot as plt
from typing import List
from copy import deepcopy
from model.example_data import get_core_data, get_suite_data
from model.utils import plot_suite_seq
from model.init_orientation import GA


def get_aggregation(suites, core, objective=0):
    SUITE_COLORS = [5, 11, 6, 9]
    CORE = Entity(core[1], 'core')
    SUITES = list()
    cats = [0, 0, 1, 1]
    ga = GA(pop_size=10000,
            generation_num=100,
            suites=[suites[i][-1] for i in cats],
            crossover_rate=0.5,
            mutation_rate=0.5,
            traffic_core_type=0,
            cats=cats)
    idx_trans = ga.run()

    for idx, trans in idx_trans:
        s = Entity(suites[cats[idx]][1], 'suite', color=SUITE_COLORS[cats[idx]])
        s.step(trans)
        SUITES.append(deepcopy(s))
    ENV_X = 64
    ENV_Y = 64
    COR_LEN_MAX = [10]
    env = Environment(
        env_x=ENV_X,
        env_y=ENV_Y,
        core=CORE,
        suites=SUITES,
        corridor_len_max=COR_LEN_MAX,
    )

    agent = Agent(
        state_dim=64,
        action_dim=5,
        gamma=0.7,
        epsilon=0.9,
        epsilon_decay=0.0005,
        epsilon_min=0.01,
        buffer_len=1000,
        batch_size=64,
        update_iter=10,
    )

    best_pos = list()
    best = 0

    MAX_STEP = 50
    MAX_EPISODE = 100

    for episode in range(MAX_EPISODE):
        env.reset()
        losses = 0
        returns = 0
        adjs = [False for _ in range(len(SUITES))]
        for step in range(MAX_STEP):
            for i in range(len(SUITES)):
                state = env.observe(i)
                action = agent.select_action(state, decay=i == len(SUITES)-1)
                reward, state_, adj, valid_action = env.step(action, i)
                adjs[i] = adj

                if all(adjs):
                    r, sf, cr, nl = env.eval()
                    if r >= best:
                        best = r
                        best_pos = deepcopy(env.pos)
                    reward += r
                returns += reward

                agent.store_transition(state, action, reward, state_, False)
            loss = agent.train()
            losses += loss
        # print('[train] episode: {}, epsilon: {}, returns: {}, losses: {}'.format(episode, agent.epsilon, returns / len(SUITES), losses))

    filename = env.plot(best_pos)
    return filename

    # res = dict()
    # for i in range(len(SUITES)):
    #     res[str(i)] = {'suite_id': suites[cats[i]][0], 'pos': best_pos[i], 'trans': idx_trans[i][1]}
    #
    # return res

def main1(image_names):
    suites = get_suite_data(image_names)
    core = get_core_data(image_names)[0]
    timestamp = get_aggregation(suites, core)
    # print(suites)
    # print(core)
    # print(get_aggregation(suites, core))
    return timestamp