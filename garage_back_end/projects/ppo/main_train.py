from ppo import PPO
from envs.inverted_pendulum import InvertedPendulum
from envs.point_2d import Point2D

if __name__=="__main__":
    # env = InvertedPendulum()
    env = Point2D()
    ppo = PPO(env=env, steps_per_trajectory=50, n_epochs_per_training_step=1, n_trajectories_per_training_step=500, lr_actor=1e-4, lr_critic=0.5e-3, epsilon=0.04, prefix_saved_model="point_2d", std=0.01)
    ppo.train(total_training_steps=1000)