import torch
import numpy as np
from model.network import MADQN
from model.buffer_madqn import ReplayBuffer

class Agent:
    def __init__(
        self, 
        state_dim,
        action_dim,
        
        gamma,
        
        epsilon,
        epsilon_decay,
        epsilon_min,
        
        buffer_len,
        batch_size,
        
        update_iter
    ) -> None:
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        self.gamma = gamma
        self.eval_net = MADQN(output_dim=action_dim).to(self.device)
        self.target_net = MADQN(output_dim=action_dim).to(self.device)
        self.loss = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=0.01)
        
        self.buffer = ReplayBuffer(state_dim=state_dim, action_dim=action_dim, max_len=buffer_len)
        self.batch_size = batch_size
        
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        self.iter = 0
        self.update_iter = update_iter
    
    def select_action(self, state, is_test=False, decay=False):
        # state = (state - state.mean()) / (state.max() - state.min())
        if is_test or np.random.random() > self.epsilon:
            actions = self.eval_net(torch.FloatTensor(state).unsqueeze(0).to(self.device)).detach().cpu().numpy()
            action = actions.argmax()
        else:
            action = np.random.randint(0, self.action_dim)

        if not is_test and decay:
            self.epsilon = max(
                self.epsilon_min, (1 - self.epsilon_decay) * self.epsilon
            )
        
        return action
    
    def store_transition(self, state, action, reward, state_, done):
        self.buffer.store(state, action, reward, state_, done)
        
    def update_target(self):
        self.target_net.load_state_dict(self.eval_net.state_dict())
    
    def train(self):
        if len(self.buffer) < self.batch_size:
            return 0

        state, action, reward, state_, done = self.buffer.sample(self.batch_size)

        state = torch.FloatTensor(state).to(self.device)
        action = torch.LongTensor(action).to(self.device)
        reward = torch.FloatTensor(reward).to(self.device)
        state_ = torch.FloatTensor(state_).to(self.device)
        done = torch.FloatTensor(done).to(self.device)

        q_eval = self.eval_net(state)
        q_eval = torch.gather(q_eval, dim=1, index=action)
        q_next = self.target_net(state_).detach().max(1)[0].view(self.batch_size, 1)
        
        q_target = reward + (1 - done) * self.gamma * q_next
        
        td_error = self.loss(q_eval, q_target)
        
        self.optimizer.zero_grad()
        td_error.backward()
        self.optimizer.step()
        
        self.iter += 1
        if self.iter % self.update_iter:
            self.update_target()

        return td_error.item()

    def save_params(self, name, save_dir='./weights'):
        path = save_dir + '/' + name + '.pth'
        torch.save(self.eval_net.state_dict(), path)

    def load_params(self, name, load_dir='./weights'):
        path = load_dir + '/' + name + '.pth'
        self.eval_net.load_state_dict(torch.load(path))
        self.update_target()
