from ppo import PPO
from env import Env
from utils import plot_rollout
from networks import Actor
import torch

class Deployment:
    def __init__(self, env: Env, actor_model_path: str) -> None:
        self.env = env
        self.actor = Actor()
        self.actor.load_state_dict(torch.load(actor_model_path))
    
    def set_state(self, cart_pos: float, cart_vel: float, pend_pos: float, pend_vel: float):
        self.env.set_state(cart_vel=cart_vel, pend_vel=pend_vel, pend_pos=pend_pos, cart_pos=cart_pos)
    
    def run(self, steps: int):
        obs = []
        acts = []
        s = self.env.get_observations()
        obs.append(s)
        for step in range(steps):
            a = self.actor(obs) * self.env.constraints.max_input
            s = self.env.step(a)
            # print(f"s = {s}")
            acts.append(a)
            obs.append(s)
        plot_rollout(obs)


if __name__=="__main__":
    actor_model_path = "/garage_back_end/projects/ppo/saved_models/2025_03_02_12_48_saved_actor_step_41_total_steps_100.pth"
    env = Env(actions_dim=1, observations_dim=4, step_dt=0.1)
    ppo = PPO(env=env, steps_per_rollout=100, n_epochs_per_training_step=50, n_rollouts_per_training_step=200, lr_actor=5e-3, lr_critic=1e-3)
    
    deployment = Deployment(env=env, actor_model_path=actor_model_path)
    deployment.set_state(cart_pos=0.0, cart_vel=0.0, pend_pos=0.5, pend_vel=0.0)
    deployment.run(steps=100)