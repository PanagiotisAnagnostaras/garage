import torch
from binder import Simulation
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
        def __init__(self) -> None:
            self.actions_dims = 1
            self.observations_dims = 4
            self.states_dims = 4

    def __init__(self) -> None:
        self.dimensions = self.Dimensions()
        self.step_dt = 0.01
        self.sim = Simulation()
        self.constraints = self.Constraints()

    def set_state(self, cart_vel: float, pend_pos: float, pend_vel: float, cart_pos: Union[None, float] = None):
        self.sim.setCartVel(cart_vel)
        self.sim.setPendAng(pend_pos)
        self.sim.setPendVel(pend_vel)
        if cart_pos is not None:
            self.sim.setCartPos(cart_pos)

    def get_observations(self) -> torch.Tensor:
        obs = torch.zeros(size=(self.dimensions.observations_dims,))
        obs[self.ObsIndexes.CART_VEL.value] = self.sim.getCartVel()
        obs[self.ObsIndexes.PEND_POS.value] = self.sim.getPendAng()
        obs[self.ObsIndexes.PEND_VEL.value] = self.sim.getPendVel()
        obs[self.ObsIndexes.PREV_ACT.value] = self.sim.getInput()
        return obs
    
    def get_states(self) -> torch.Tensor:
        states = torch.zeros(size=(self.dimensions.states_dims,))
        states[self.StatesIndex.CART_POS.value] = self.sim.getCartPos()
        states[self.StatesIndex.CART_VEL.value] = self.sim.getCartVel()
        states[self.StatesIndex.PEND_POS.value] = self.sim.getPendAng()
        states[self.StatesIndex.PEND_VEL.value] = self.sim.getPendVel()
        return states
    
    def get_time(self) -> float:
        return self.sim.getTime()

    def apply_actions(self, actions: torch.Tensor) -> None:
        self.sim.applyInput(actions.item())
        return

    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = torch.tensor(data=0, dtype=torch.float)
        assert 0 <= observations[self.ObsIndexes.PEND_POS.value] < 2 * torch.pi, f"Angle must be in [0, 2pi). Got {observations[self.ObsIndexes.PEND_POS.value]}"
        if observations[self.ObsIndexes.PEND_POS.value] <= torch.pi:
            rew += torch.exp(-((observations[self.ObsIndexes.PEND_POS.value]) ** 2) / 1)
        else:
            rew += torch.exp(-((2 * torch.pi - observations[self.ObsIndexes.PEND_POS.value]) ** 2) / 1)
        rew += 0.1*torch.exp(-((observations[self.ObsIndexes.PREV_ACT.value]) ** 2) / 1)
        return rew

    def step(self, actions: torch.Tensor) -> torch.Tensor:
        self.apply_actions(actions=actions)
        self.sim.run(self.step_dt, False)
        return self.get_observations()

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

