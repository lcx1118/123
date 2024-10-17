import numpy as np


class ReplayBuffer:
    def __init__(self, state_dim, action_dim, max_len) -> None:
        self.states = np.zeros((max_len, 3, state_dim, state_dim))
        self.states_ = np.zeros((max_len, 3, state_dim, state_dim))
        self.actions = np.zeros((max_len, 1))
        self.rewards = np.zeros((max_len, 1))
        self.dones = np.zeros((max_len, 1))

        self.ptr = 0
        self.len = 0
        self.max_len = max_len

    def __len__(self):
        return self.len

    def store(self, state, action, reward, state_, done):
        self.states[self.ptr] = state
        self.actions[self.ptr] = action
        self.rewards[self.ptr] = reward
        self.states_[self.ptr] = state_
        self.dones[self.ptr] = done

        self.len = min(self.len + 1, self.max_len)
        self.ptr = (self.ptr + 1) % self.max_len

    def sample(self, batch_size):
        idx = np.random.choice(np.arange(0, self.len, 1), batch_size, replace=False)

        state = self.states[idx]
        state_ = self.states_[idx]
        action = self.actions[idx]
        reward = self.rewards[idx]
        done = self.dones[idx]

        return state, action, reward, state_, done
