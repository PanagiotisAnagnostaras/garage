import torch
from abc import ABC, abstractmethod

class Env(ABC):
    
    class Constraints:
        pass
        
    class Dimensions:
        actions_dims = None
        observations_dims = None
        states_dims = None
            
    @abstractmethod
    def __init__(self) -> None:
        self.dimensions = Env.Dimensions()
        self.constraints = Env.Constraints()

    @abstractmethod
    def set_state(self) -> None:
        pass
    
    @abstractmethod
    def get_observations(self) -> torch.Tensor:
        pass
    
    @abstractmethod
    def get_states(self) -> torch.Tensor:
        pass
    
    @abstractmethod
    def get_time(self) -> float:
        pass

    @abstractmethod
    def apply_actions(self, actions: torch.Tensor) -> None:
        pass

    @abstractmethod
    def get_reward(self) -> torch.Tensor:
        pass

    @abstractmethod
    def step(self) -> torch.Tensor:
        pass
