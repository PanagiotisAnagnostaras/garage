import torch
from enum import Enum
from typing import Union
from envs.env import Env
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from typing import List
import math

class Point2D(Env):
    class ObsIndexes(Enum):
        X_POS = 0
        X_VEL = 1
        Y_POS = 2
        Y_VEL = 3
        X_FORCE = 4
        Y_FORCE = 5

    class StatesIndex(Enum):
        X_POS = 0
        X_VEL = 1
        Y_POS = 2
        Y_VEL = 3

    class ActionsIndex(Enum):
        X_FORCE = 0
        Y_FORCE = 1
        
    class Dimensions:
        actions_dims = 2
        observations_dims = 6
        states_dims = 4

    def __init__(self) -> None:
        super().__init__()
        self.sim.setSystemPoint2D()

    def get_observations(self) -> torch.Tensor:
        obs = torch.zeros(size=(self.Dimensions.observations_dims,))
        state = self.get_state()
        input = self.get_actions()
        obs[self.ObsIndexes.X_POS.value] = state[self.StatesIndex.X_POS.value]
        obs[self.ObsIndexes.X_VEL.value] = state[self.StatesIndex.X_VEL.value]
        obs[self.ObsIndexes.Y_POS.value] = state[self.StatesIndex.Y_POS.value]
        obs[self.ObsIndexes.Y_VEL.value] = state[self.StatesIndex.Y_VEL.value]
        obs[self.ObsIndexes.X_FORCE.value] = input[self.ActionsIndex.X_FORCE.value]
        obs[self.ObsIndexes.Y_FORCE.value] = input[self.ActionsIndex.Y_FORCE.value]
        return obs

    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = torch.tensor(data=0, dtype=torch.float)
        distance = math.hypot(observations[self.ObsIndexes.X_POS.value], observations[self.ObsIndexes.Y_POS.value])
        velocity = math.hypot(observations[self.ObsIndexes.X_VEL.value], observations[self.ObsIndexes.Y_VEL.value])
        rew += 10*torch.exp(-(torch.tensor(data=distance) ** 2) / 1)
        rew += torch.exp(-(torch.tensor(data=velocity) ** 2) / 1)
        return rew

    def plot_rollout(self, obs: torch.Tensor):
        fig, ax = plt.subplots(ncols=3, nrows=2)
        ax: List[List[Axes]]
        ax[0][0].plot(obs[:, self.ObsIndexes.X_POS.value], label="x pos")
        ax[0][1].plot(obs[:, self.ObsIndexes.Y_POS.value], label="y pos")
        ax[1][0].plot(obs[:, self.ObsIndexes.X_VEL.value], label="x vel")
        ax[1][1].plot(obs[:, self.ObsIndexes.Y_VEL.value], label="y vel")
        ax[0][2].plot(obs[:, self.ObsIndexes.X_POS.value], obs[:, self.ObsIndexes.Y_POS.value], label="x-y")
        ax[0][0].legend()
        ax[0][1].legend()
        ax[1][0].legend()
        ax[1][1].legend()
        plt.show()

    def get_action_constraints(self) -> torch.Tensor:
        max_applied_input = [10, 10]
        return torch.tensor(data=max_applied_input)
    
    def get_state_constraints(self) -> torch.Tensor:
        max_x_pos = 1
        max_x_vel = 10
        max_y_pos = 1
        max_y_vel = 10
        constraints = [max_x_pos, max_x_vel, max_y_pos, max_y_vel]
        return torch.tensor(data=constraints)

class AnimationPoint2D(Point2D):
    pass