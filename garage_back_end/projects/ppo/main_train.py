from ppo import PPO
from env import Env

if __name__=="__main__":
    env = Env(actions_dim=1, observations_dim=4, step_dt=0.1)
    ppo = PPO(env=env, steps_per_rollout=100, n_epochs_per_training_step=50, n_rollouts_per_training_step=200, lr_actor=5e-3, lr_critic=1e-3, epsilon=0.1)
    ppo.train(total_training_steps=1000)