import torch
from enum import Enum
from typing import Union
from envs.env import Env
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from typing import List


class InvertedPendulum(Env):
    class ObsIndexes(Enum):
        CART_VEL = 0
        PEND_POS = 1
        PEND_VEL = 2
        PREV_ACT = 3

    class StatesIndex(Enum):
        CART_POS = 0
        CART_VEL = 1
        PEND_POS = 2
        PEND_VEL = 3

    class Constraints:
        max_cart_vel = 0
        max_pend_vel = 0
        max_input = 50

    class Dimensions:
        actions_dims = 1
        observations_dims = 4
        states_dims = 4

    def __init__(self) -> None:
        super().__init__()
        self.sim.setSystemInvertedPendulum()

    def get_observations(self) -> torch.Tensor:
        obs = torch.zeros(size=(self.Dimensions.observations_dims,))
        state = self.get_state()
        input = self.get_input()
        obs[self.ObsIndexes.CART_VEL.value] = state[self.StatesIndex.CART_VEL]
        obs[self.ObsIndexes.PEND_POS.value] = state[self.StatesIndex.PEND_POS]
        obs[self.ObsIndexes.PEND_VEL.value] = state[self.StatesIndex.PEND_VEL]
        obs[self.ObsIndexes.PREV_ACT.value] = input[0]
        return obs

    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = torch.tensor(data=0, dtype=torch.float)
        assert 0 <= observations[self.ObsIndexes.PEND_POS.value] < 2 * torch.pi, f"Angle must be in [0, 2pi). Got {observations[self.ObsIndexes.PEND_POS.value]}"
        if observations[self.ObsIndexes.PEND_POS.value] <= torch.pi:
            rew += torch.exp(-((observations[self.ObsIndexes.PEND_POS.value]) ** 2) / 1)
        else:
            rew += torch.exp(-((2 * torch.pi - observations[self.ObsIndexes.PEND_POS.value]) ** 2) / 1)
        rew += 0.1 * torch.exp(-((observations[self.ObsIndexes.PREV_ACT.value]) ** 2) / 1)
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
