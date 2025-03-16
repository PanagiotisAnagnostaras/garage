from ppo import PPO
from envs.inverted_pendulum import InvertedPendulum
from envs.point_2d import Point2D

if __name__=="__main__":
    # env = InvertedPendulum()
    env = Point2D()
    ppo = PPO(env=env, steps_per_rollout=50, n_epochs_per_training_step=50, n_rollouts_per_training_step=200, lr_actor=5e-5, lr_critic=1e-3, epsilon=0.1)
    ppo.train(total_training_steps=1000)