from torch import nn
import torch
from torch.distributions import MultivariateNormal

class Actor(nn.Module):
    def __init__(self, obs_dim: int, act_dim: int) -> None:
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(obs_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, act_dim)
        )
        
    
    def forward(self, x):
        return self.linear_relu_stack(x)

class Critic(nn.Module):
    def __init__(self, obs_dim: int) -> None:
        super().__init__()
        
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(obs_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    
    def forward(self, x):
        return self.linear_relu_stack(x)
