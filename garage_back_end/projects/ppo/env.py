import torch
from binder import Simulation
from enum import Enum
from typing import Union


class Env:
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
        def __init__(self, actions_dims, observations_dims, states_dims) -> None:
            self.actions_dims = actions_dims
            self.observations_dims = observations_dims
            self.states_dims = states_dims

    def __init__(self, actions_dim: int, observations_dim: int, step_dt: float) -> None:
        self.dimensions = Env.Dimensions(actions_dims=actions_dim, observations_dims=observations_dim, states_dims=4)#todo fix these
        self.step_dt = step_dt
        self.sim = Simulation()
        self.constraints = Env.Constraints()

    def set_state(self, cart_vel: float, pend_pos: float, pend_vel: float, cart_pos: Union[None, float] = None):
        self.sim.setCartVel(cart_vel)
        self.sim.setPendAng(pend_pos)
        self.sim.setPendVel(pend_vel)
        if cart_pos is not None:
            self.sim.setCartPos(cart_pos)

    def get_observations(self) -> torch.Tensor:
        obs = torch.zeros(size=(self.dimensions.observations_dims,))
        obs[Env.ObsIndexes.CART_VEL.value] = self.sim.getCartVel()
        obs[Env.ObsIndexes.PEND_POS.value] = self.sim.getPendAng()
        obs[Env.ObsIndexes.PEND_VEL.value] = self.sim.getPendVel()
        obs[Env.ObsIndexes.PREV_ACT.value] = self.sim.getInput()
        return obs
    
    def get_states(self) -> torch.Tensor:
        states = torch.zeros(size=(self.dimensions.states_dims,))
        states[Env.StatesIndex.CART_POS.value] = self.sim.getCartPos()
        states[Env.StatesIndex.CART_VEL.value] = self.sim.getCartVel()
        states[Env.StatesIndex.PEND_POS.value] = self.sim.getPendAng()
        states[Env.StatesIndex.PEND_VEL.value] = self.sim.getPendVel()
        return states
    
    def get_time(self) -> float:
        return self.sim.getTime()

    def apply_actions(self, actions: torch.Tensor) -> None:
        self.sim.applyInput(actions.item())
        return

    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = torch.tensor(data=0, dtype=torch.float)
        assert 0 <= observations[Env.ObsIndexes.PEND_POS.value] < 2 * torch.pi, f"Angle must be in [0, 2pi). Got {observations[Env.ObsIndexes.PEND_POS.value]}"
        if observations[Env.ObsIndexes.PEND_POS.value] <= torch.pi:
            rew += torch.exp(-((observations[Env.ObsIndexes.PEND_POS.value]) ** 2) / 1)
        else:
            rew += torch.exp(-((2 * torch.pi - observations[Env.ObsIndexes.PEND_POS.value]) ** 2) / 1)
        rew += 0.1*torch.exp(-((observations[Env.ObsIndexes.PREV_ACT.value]) ** 2) / 1)
        return rew

    def step(self, actions: torch.Tensor) -> torch.Tensor:
        self.apply_actions(actions=actions)
        self.sim.run(self.step_dt, False)
        return self.get_observations()
