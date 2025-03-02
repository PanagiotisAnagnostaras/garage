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
        
    class Constraints:
        max_cart_vel = 0
        max_pend_vel = 0
        max_input = 20
        
    class Dimensions:
        def __init__(self, actions_dims, observations_dims) -> None:
            self.actions_dims = actions_dims
            self.observations_dims = observations_dims
    
    def __init__(self, actions_dim: int, observations_dim: int, step_dt: float) -> None:
        self.dimensions = Env.Dimensions(actions_dims=actions_dim, observations_dims=observations_dim)
        self.step_dt = step_dt
        self.sim = Simulation()
        self.constraints = Env.Constraints()

    def set_state(self, cart_vel: float, pend_pos: float, pend_vel: float, cart_pos=Union[None, float]):
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
    
    def apply_actions(self, actions: torch.Tensor) -> None:
        self.sim.applyInput(actions.item())
        return
    
    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = torch.tensor(data=0, dtype=torch.float)
        rew += torch.exp(-(observations[Env.ObsIndexes.PEND_POS.value])**2/1)
        return rew
    
    def step(self, actions: torch.Tensor) -> torch.Tensor:
        self.apply_actions(actions=actions)
        self.sim.run(self.step_dt, False)
        return self.get_observations()