import torch
import torch.nn as nn


class DQN(nn.Module):
    def __init__(self, state_dim, action_dim) -> None:
        super().__init__()


        self.suite = nn.Sequential(
            nn.AvgPool2d(4),
            nn.Flatten()
        )
        
        self.net = nn.Sequential(
            nn.Linear(state_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
        )
        
    def forward(self, offset, suite=None):
        # x = self.suite(suite)
        # x = torch.cat((x, offset), dim=1)
        return torch.tanh(self.net(offset))


class MADQN(nn.Module):
    def __init__(self, output_dim):
        super().__init__()

        self.conv = nn.Sequential(
            # input: 3 x 64 x 64
            nn.Conv2d(in_channels=3, out_channels=8, kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.BatchNorm2d(num_features=8),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            # 8 x 32 x 32
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.BatchNorm2d(num_features=16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            # 16 x 16 x 16
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.BatchNorm2d(num_features=32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            # 32 x 8 x 8
        )

        self.q = nn.Sequential(
            nn.Linear(32 * 8 * 8, output_dim),
            # nn.Softmax()
        )

    def forward(self, x):
        # print(x.shape)
        y = self.conv(x)
        y = y.view(x.size(0), -1)
        return self.q(y)


class Actor(nn.Module):
    def __init__(self, output_dim):
        super().__init__()

        self.conv = nn.Sequential(
            # input: 3 x 64 x 64
            nn.Conv2d(in_channels=3, out_channels=8, kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.BatchNorm2d(num_features=8),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            # 8 x 32 x 32
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.BatchNorm2d(num_features=16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            # 16 x 16 x 16
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.BatchNorm2d(num_features=32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            # 32 x 8 x 8
        )

        self.action_selector = nn.Linear(32 * 8 * 8, output_dim)

    def forward(self, x):
        # print(x.shape)
        y = self.conv(x)
        y = y.view(x.size(0), -1)
        return self.action_selector(y)


class Critic(nn.Module):
    def __init__(self, actor_num):
        super().__init__()
        self.conv = nn.Sequential(
            # input: 3 x 64 x 64
            nn.Conv2d(in_channels=3 * actor_num, out_channels=8, kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.BatchNorm2d(num_features=8),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            # 8 x 32 x 32
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.BatchNorm2d(num_features=16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            # 16 x 16 x 16
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.BatchNorm2d(num_features=32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            # 32 x 8 x 8
        )

        self.q = nn.Linear(32 * 8 * 8, 1)

    def forward(self, x):
        # print(x.shape)
        y = self.conv(x)
        y = y.view(x.size(0), -1)
        return self.q(y)