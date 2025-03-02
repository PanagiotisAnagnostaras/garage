from ppo import PPO
from env import Env
from utils import plot_rollout
from networks import Actor
import torch

class Deployment:
    def __init__(self, env: Env, actor_model_path: str) -> None:
        self.env = env
        self.actor = Actor(obs_dim=env.dimensions.observations_dims, act_dim=env.dimensions.actions_dims)
        self.actor=torch.load(actor_model_path, weights_only=False)
    
    def set_state(self, cart_pos: float, cart_vel: float, pend_pos: float, pend_vel: float):
        self.env.set_state(cart_vel=cart_vel, pend_vel=pend_vel, pend_pos=pend_pos, cart_pos=cart_pos)
    
    def run(self, steps: int):
        obs = []
        acts = []
        s = self.env.get_observations()
        obs.append(s)
        for step in range(steps):
            a = self.actor(s) * self.env.constraints.max_input
            s = self.env.step(a)
            # print(f"s = {s}")
            acts.append(a)
            obs.append(s)
        obs_t = torch.stack(obs)
        plot_rollout(obs_t)


if __name__=="__main__":
    actor_model_path = "/garage_back_end/projects/ppo/saved_models/2025_03_02_13_12_saved_actor_step_510_total_steps_1000.pth"
    env = Env(actions_dim=1, observations_dim=4, step_dt=0.1)    
    deployment = Deployment(env=env, actor_model_path=actor_model_path)
    deployment.set_state(cart_pos=0.0, cart_vel=0.0, pend_pos=0.5, pend_vel=0.0)
    deployment.run(steps=100)