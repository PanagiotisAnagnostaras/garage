from envs.env import Env
from envs.inverted_pendulum import AnimationInvertedPendulum
from envs.point_2d import AnimationPoint2D

if __name__ == "__main__":
    actor_model_path = "/garage_back_end/projects/ppo/saved_models/2025_03_04_22_24_saved_actor_step_134_total_steps_1000_w_input_rew.pth"
    anim = AnimationInvertedPendulum(actor_model_path=actor_model_path)
    initial_state = [0.5, 0.0, 0.5, 0.0]
    steps = 10000
    anim.animate(steps=steps, x0=initial_state)
