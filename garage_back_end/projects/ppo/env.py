import torch
from dimensions import Dimensions
from binder import Simulation
from enum import Enum

class Indexes(Enum):
    CART_VEL = 0
    PEND_POS = 1
    PEND_VEL = 2

class Constraints:
    max_cart_vel = 100
    max_pend_vel = 100
    
class Env:
    def __init__(self, actions_dim: int, observations_dim: int, step_dt: float) -> None:
        self.dimensions = Dimensions(actions_dims=actions_dim, observations_dims=observations_dim)
        self.step_dt = step_dt
        self.sim = Simulation()
        self.constraints = Constraints()

    def set_state(self, cart_vel: float, pend_pos: float, pend_vel: float):
        self.sim.setCartVel(cart_vel)
        self.sim.setPendAng(pend_pos)
        self.sim.setPendVel(pend_vel)
    
    def get_observations(self) -> torch.Tensor:
        obs = []
        # obs.append(self.sim.getCartPos())
        obs.append(self.sim.getCartVel())
        obs.append(self.sim.getPendAng())
        obs.append(self.sim.getPendVel())
        return torch.tensor(obs)
    
    def apply_actions(self, actions: torch.Tensor) -> None:
        self.sim.applyInput(actions.item())
        return
    
    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = 0
        rew += torch.exp(-(observations[Indexes.PEND_POS.value])**2/0.1)
        return torch.tensor(rew)
    
    def step(self, actions: torch.Tensor) -> torch.Tensor:
        self.apply_actions(actions=actions)
        self.sim.run(self.step_dt, False)
        return self.get_observations()