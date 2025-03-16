import torch
from abc import ABC, abstractmethod
from binder import SimulationFacade


class Env(ABC):
    class Dimensions:
        actions_dims = None
        observations_dims = None
        states_dims = None
        
    def __init__(self) -> None:
        self.sim = SimulationFacade()
        self.step_dt = 0.1

    def set_state(self, state: torch.Tensor) -> None:
        state_list = state.tolist()
        self.sim.setState(state_list)

    def get_state(self) -> torch.Tensor:
        return torch.tensor(data=self.sim.getState())

    def get_actions(self) -> torch.Tensor:
        return torch.tensor(data=self.sim.getInput())

    def get_time(self) -> float:
        return self.sim.getTime()

    def apply_actions(self, actions: torch.Tensor) -> None:
        self.sim.setInput(actions.tolist())

    def step(self, actions: torch.Tensor) -> torch.Tensor:
        self.apply_actions(actions=actions)
        self.sim.simulate(False, self.step_dt)
        return self.get_observations()

    @abstractmethod
    def get_observations(self) -> torch.Tensor:
        pass

    @abstractmethod
    def get_reward(self) -> torch.Tensor:
        pass
    
    @abstractmethod
    def plot_rollout(self) -> torch.Tensor:
        pass
    
    @abstractmethod
    def get_action_constraints(self) -> torch.Tensor:
        pass
    
    @abstractmethod
    def get_state_constraints(self) -> torch.Tensor:
        pass
