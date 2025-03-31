from ppo import PPO
from envs.inverted_pendulum import InvertedPendulum
from envs.point_2d import Point2D

if __name__=="__main__":
    # env = InvertedPendulum()
    env = Point2D()
    ppo = PPO(env=env, steps_per_trajectory=10, n_epochs_per_training_step=3, n_trajectories_per_training_step=100, lr_actor=1e-4, lr_critic=0.5e-3, epsilon=0.1, prefix_saved_model="point_2d", std=0.1)
    ppo.train(total_training_steps=1000)