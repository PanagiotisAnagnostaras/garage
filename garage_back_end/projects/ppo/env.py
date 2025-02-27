import torch
from dimensions import Dimensions
from binder import Simulation
from enum import Enum

class Indexes(Enum):
    CART_VEL = 0
    PEND_POS = 1
    PEND_VEL = 2

class Constraints:
    max_cart_vel = 10
    max_pend_vel = 10
    max_input = 100
    
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
        obs = torch.zeros(size=(self.dimensions.observations_dims,))
        obs[Indexes.CART_VEL.value] = self.sim.getCartVel()
        obs[Indexes.PEND_POS.value] = self.sim.getPendAng() % (2*torch.pi)
        obs[Indexes.PEND_VEL.value] = self.sim.getPendVel()
        return obs
    
    def apply_actions(self, actions: torch.Tensor) -> None:
        action_normalized = self.constraints.max_input* 1/(1+torch.exp(-actions)) - self.constraints.max_input/2
        self.sim.applyInput(action_normalized.item())
        return
    
    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = torch.tensor(data=0, dtype=torch.float)
        rew += torch.exp(-(observations[Indexes.PEND_POS.value])**2/1)
        return rew
    
    def step(self, actions: torch.Tensor) -> torch.Tensor:
        self.apply_actions(actions=actions)
        self.sim.run(self.step_dt, False)
        return self.get_observations()