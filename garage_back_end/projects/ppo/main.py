from ppo import PPO
from env import Env

if __name__=="__main__":
    env = Env(actions_dim=1, observations_dim=4, step_dt=0.1)
    ppo = PPO(env=env, steps_per_rollout=100, n_epochs=30, lr=1e-12)
    ppo.train(total_training_steps=10_000_000)
    ppo.save()
    