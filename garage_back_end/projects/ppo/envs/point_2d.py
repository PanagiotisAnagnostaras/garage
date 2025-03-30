import sys
import numpy as np
import torch
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.axes import Axes
from typing import List, Union
from enum import Enum
from envs.env import Env
from networks import Actor
import math

class Point2D(Env):
    class ObsIndexes(Enum):
        X_POS = 0
        X_VEL = 1
        Y_POS = 2
        Y_VEL = 3
        X_FORCE = 4
        Y_FORCE = 5

    class StatesIndex(Enum):
        X_POS = 0
        X_VEL = 1
        Y_POS = 2
        Y_VEL = 3

    class ActionsIndex(Enum):
        X_FORCE = 0
        Y_FORCE = 1

    class Dimensions:
        actions_dims = 2
        observations_dims = 6
        states_dims = 4

    def __init__(self) -> None:
        super().__init__()
        self.sim.setSystemPoint2D()

    def get_observations(self) -> torch.Tensor:
        obs = torch.zeros(size=(self.Dimensions.observations_dims,))
        state = self.get_state()
        input = self.get_actions()
        obs[self.ObsIndexes.X_POS.value] = state[self.StatesIndex.X_POS.value]
        obs[self.ObsIndexes.X_VEL.value] = state[self.StatesIndex.X_VEL.value]
        obs[self.ObsIndexes.Y_POS.value] = state[self.StatesIndex.Y_POS.value]
        obs[self.ObsIndexes.Y_VEL.value] = state[self.StatesIndex.Y_VEL.value]
        obs[self.ObsIndexes.X_FORCE.value] = input[self.ActionsIndex.X_FORCE.value]
        obs[self.ObsIndexes.Y_FORCE.value] = input[self.ActionsIndex.Y_FORCE.value]
        return obs

    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = torch.tensor(data=0, dtype=torch.float)
        distance = math.hypot(observations[self.ObsIndexes.X_POS.value], observations[self.ObsIndexes.Y_POS.value])
        velocity = math.hypot(observations[self.ObsIndexes.X_VEL.value], observations[self.ObsIndexes.Y_VEL.value])
        rew += 10 * torch.exp(-(torch.tensor(data=distance) ** 2) / 1)
        rew += torch.exp(-(torch.tensor(data=velocity) ** 2) / 1)
        return rew

    def plot_rollout(self, obs: torch.Tensor):
        fig, ax = plt.subplots(ncols=4, nrows=2)
        ax: List[List[Axes]]
        # x - t
        ax[0][0].plot(obs[:, self.ObsIndexes.X_POS.value], label="x pos")
        ax[0][0].set_ylabel(self.ObsIndexes.X_POS.name)
        ax[0][0].legend()
        # y - t
        ax[0][1].plot(obs[:, self.ObsIndexes.Y_POS.value], label="y pos")
        ax[0][1].set_ylabel(self.ObsIndexes.Y_POS.name)
        ax[0][1].legend()
        # dot x - t
        ax[1][0].plot(obs[:, self.ObsIndexes.X_VEL.value], label="x vel")
        ax[1][0].set_ylabel(self.ObsIndexes.X_VEL.name)
        ax[1][0].legend()
        # dot y - t
        ax[1][1].plot(obs[:, self.ObsIndexes.Y_VEL.value], label="y vel")
        ax[1][1].set_ylabel(self.ObsIndexes.Y_VEL.name)
        ax[1][1].legend()
        # F_x - t
        ax[0][2].plot(obs[:, self.ObsIndexes.X_FORCE.value], label="Fx")
        ax[0][2].set_ylabel(self.ObsIndexes.X_FORCE.name)
        ax[0][2].legend()
        # F_y - t
        ax[1][2].plot(obs[:, self.ObsIndexes.Y_FORCE.value], label="Fy")
        ax[1][2].set_ylabel(self.ObsIndexes.Y_FORCE.name)
        ax[1][2].legend()
        # x - y 
        ax[0][3].plot(obs[:, self.ObsIndexes.X_POS.value], obs[:, self.ObsIndexes.Y_POS.value], label="x-y")
        ax[0][3].set_xlabel(self.ObsIndexes.X_POS.value)
        ax[0][3].set_ylabel(self.ObsIndexes.Y_POS.value)
        ax[0][3].legend()
        fig.tight_layout()
        plt.show()

    def get_action_constraints(self) -> torch.Tensor:
        max_applied_input = [0.1, 0.1]
        return torch.tensor(data=max_applied_input)

    def get_state_constraints(self) -> torch.Tensor:
        max_x_pos = 1
        max_x_vel = 0
        max_y_pos = 1
        max_y_vel = 0
        constraints = [max_x_pos, max_x_vel, max_y_pos, max_y_vel]
        return torch.tensor(data=constraints)


class AnimationPoint2D(Point2D):
    def __init__(self, actor_model_path) -> None:
        super().__init__()
        matplotlib.use("TkAgg")
        self.time_data = []
        self.x_pos_data = []
        self.x_vel_data = []
        self.y_pos_data = []
        self.y_vel_data = []
        self.input_data_x = []
        self.input_data_y = []
        self.time = 0
        self.plot_period_s = 0.1
        actor = Actor(obs_dim=self.Dimensions.observations_dims, act_dim=self.Dimensions.actions_dims)
        actor = torch.load(actor_model_path, weights_only=False)
        self.actor = actor

    def animate(self, steps: int, x0: torch.tensor):
        self.set_state(x0)
        remaining_steps = steps
        fig, ax = plt.subplots(ncols=3, nrows=2)
        ax: List[List[plt.Axes]]
        fig: plt.Figure

        ax_x_pos = ax[0][0]
        ax_x_vel = ax[1][0]
        ax_y_pos = ax[0][1]
        ax_y_vel = ax[1][1]
        ax_animation = ax[1][2]

        (line_x_pos,) = ax_x_pos.plot([], [], label="x pos")
        (line_x_vel,) = ax_x_vel.plot([], [], label="x vel")
        (line_y_pos,) = ax_y_pos.plot([], [], label="y pos")
        (line_y_vel,) = ax_y_vel.plot([], [], label="y vel")
        (line_animation,) = ax_animation.plot([], [], label="Animation")

        ax_x_pos.set_title("X Pos - Time")
        ax_x_pos.set_xlabel("Time (s)")
        ax_x_pos.set_ylabel("X Pos (m)")

        ax_x_vel.set_title("X Vel - Time")
        ax_x_vel.set_xlabel("Time (s)")
        ax_x_vel.set_ylabel("X Vel (m/s)")

        ax_y_pos.set_title("Y Pos - Time")
        ax_y_pos.set_xlabel("Time (s)")
        ax_y_pos.set_ylabel("Y Pos (m)")

        ax_y_vel.set_title("Y Vel - Time")
        ax_y_vel.set_xlabel("Time (s)")
        ax_y_vel.set_ylabel("Y Vel (m/s)")


        ax_animation.set_title("Animation")
        ax_animation.set_xlabel("x")
        ax_animation.set_ylabel("y")

        target = patches.Circle((0, 0), 0.1, linewidth=2, edgecolor="r", facecolor="r")
        ball = patches.Circle((0, 0), 0.1, linewidth=2, edgecolor="b", facecolor="b")

        ax_animation.add_patch(target)
        ax_animation.add_patch(ball)

        def init():
            line_x_pos.set_data([], [])
            line_x_vel.set_data([], [])
            line_y_pos.set_data([], [])
            line_y_vel.set_data([], [])
            ax_x_pos.set_xlim(0, 10)
            ax_x_vel.set_xlim(0, 10)
            ax_y_pos.set_xlim(0, 10)
            ax_y_vel.set_xlim(0, 10)
            ax_x_pos.set_ylim(-5, 10)
            ax_x_vel.set_ylim(-5, 10)
            ax_y_pos.set_ylim(-5, 10)
            ax_y_vel.set_ylim(-5, 10)
            ax_animation.set_xlim(-2, 2)
            ax_animation.set_ylim(-2, 2)
            return line_x_pos, line_x_vel, line_y_pos, line_y_vel, line_animation

        def update(frame):
            self._mdp_step()
            actions = self.get_actions()
            self.time += self.get_time()
            state = self.get_state()
            x_pos: float = state[self.StatesIndex.X_POS.value]
            x_vel: float = state[self.StatesIndex.X_VEL.value]
            y_pos: float = state[self.StatesIndex.Y_POS.value]
            y_vel: float = state[self.StatesIndex.Y_VEL.value]
            input_signal_x: float = actions[0]
            input_signal_y: float = actions[1]
            print(f"self.time = {self.time} x_pos = {x_pos} x_vel = {x_vel} y_pos = {y_pos} y_vel = {y_vel} input_signal_x = {input_signal_x} input_signal_y = {input_signal_y}")

            self.time_data.append(self.time)
            self.x_pos_data.append(x_pos)
            self.x_vel_data.append(x_vel)
            self.y_pos_data.append(y_pos)
            self.y_vel_data.append(y_vel)
            self.input_data_x.append(input_signal_x)
            self.input_data_y.append(input_signal_y)

            line_x_pos.set_data(self.time_data, self.x_pos_data)
            line_x_vel.set_data(self.time_data, self.x_vel_data)
            line_y_pos.set_data(self.time_data, self.y_pos_data)
            line_y_vel.set_data(self.time_data, self.y_vel_data)


            target.set_center((0.0 , 0.0))
            ball.set_center((x_pos, y_pos))
            nonlocal remaining_steps
            remaining_steps -= 1
            print(f"Remaining steps = {remaining_steps}/{steps}")
            if remaining_steps == 0:
                sys.exit()
            return line_x_pos, line_x_vel, line_y_pos, line_y_vel, line_animation

        ani = animation.FuncAnimation(fig, update, frames=1, init_func=init, blit=False, interval=1)
        # Adjust layout
        plt.tight_layout()
        plt.show()

    def _mdp_step(self):
        s = self.get_observations()
        a = self.actor(s) * self.get_action_constraints()  # todo fix this
        s = self.step(a)
