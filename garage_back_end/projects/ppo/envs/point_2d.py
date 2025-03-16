import torch
from enum import Enum
from typing import Union
from envs.env import Env
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from typing import List


class Point2D(Env):
    class ObsIndexes(Enum):
        X_POS = 0
        X_VEL = 1
        Y_POS = 2
        Y_VEL = 3
        X_FORCE = 4
        Y_FORCE = 6

    class StatesIndex(Enum):
        X_POS = 0
        X_VEL = 1
        Y_POS = 2
        Y_VEL = 3

    class ActionsIndex(Enum):
        X_FORCE = 0
        Y_FORCE = 1
        
    class Constraints:
        pass

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
        obs[self.ObsIndexes.X_FORCE.value] = input[self.ActionsIndex.X_FORCE]
        obs[self.ObsIndexes.Y_FORCE.value] = input[self.ActionsIndex.Y_FORCE]
        return obs

    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = torch.tensor(data=0, dtype=torch.float)
        return rew

    def plot_rollout(self, obs: torch.Tensor):
        fig, ax = plt.subplots(ncols=2, nrows=2)
        ax: List[List[Axes]]
        ax[0][0].plot(obs[:, self.ObsIndexes.CART_VEL.value], label="cart vel")
        ax[0][1].plot(obs[:, self.ObsIndexes.PEND_POS.value], label="pend pos")
        ax[1][0].plot(obs[:, self.ObsIndexes.PEND_VEL.value], label="pend vel")
        ax[1][1].plot(obs[:, self.ObsIndexes.PREV_ACT.value], label="prev act")
        ax[0][0].legend()
        ax[0][1].legend()
        ax[1][0].legend()
        ax[1][1].legend()
        plt.show()
