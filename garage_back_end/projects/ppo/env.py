import torch
from dimensions import Dimensions
from binder import Simulation


class Env:
    
    def __init__(self, actions_dim: int, observations_dim: int, step_dt: float) -> None:
        self.dimensions = Dimensions(actions_dims=actions_dim, observations_dims=observations_dim)
        self.step_dt = step_dt
        self.sim = Simulation()
    
    def get_observations(self) -> torch.Tensor:
        obs = []
        obs.append(self.sim.getCartPos())
        obs.append(self.sim.getCartVel())
        obs.append(self.sim.getPendAng())
        obs.append(self.sim.getPendVel())
        return torch.tensor(obs)
    
    def apply_actions(self, actions: torch.Tensor) -> None:
        self.sim.applyInput(0.0) # to fix this
        return
    
    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = 0
        rew += - torch.log(torch.abs(observations[2])+1) # theta -> 0
        rew += - torch.log(torch.abs(observations[3])+1) # omega -> 0
        return torch.tensor(rew)
    
    def step(self, actions: torch.Tensor) -> torch.Tensor:
        self.apply_actions(actions=actions)
        self.sim.run(self.step_dt, False)
        return self.get_observations()