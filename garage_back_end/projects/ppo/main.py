from ppo import PPO
from env import Env

if __name__=="__main__":
    env = Env(actions_dim=1, observations_dim=4, step_dt=0.1)
    ppo = PPO(env=env, steps_per_rollout=50, n_epochs_per_training_step=30, n_rollouts_per_training_step=400, lr_actor=5e-3, lr_critic=1e-3)
    ppo.train(total_training_steps=100)
    ppo.save()
    