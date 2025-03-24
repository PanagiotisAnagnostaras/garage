import torch
from enum import Enum
from typing import Union
from envs.env import Env
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from typing import List
from matplotlib import patches
import matplotlib.animation as animation
import numpy
import sys
import matplotlib
from networks import Actor

# todo:
# - wrap circle to [0,2pi]

class InvertedPendulum(Env):
    class ObsIndexes(Enum):
        CART_VEL = 0
        PEND_POS = 1
        PEND_VEL = 2
        PREV_ACT = 3

    class StatesIndex(Enum):
        CART_POS = 0
        CART_VEL = 1
        PEND_POS = 2
        PEND_VEL = 3

    class Dimensions:
        actions_dims = 1
        observations_dims = 4
        states_dims = 4

    def __init__(self) -> None:
        super().__init__()
        self.sim.setSystemInvertedPendulum()

    def get_observations(self) -> torch.Tensor:
        obs = torch.zeros(size=(self.Dimensions.observations_dims,))
        state = self.get_state()
        actions = self.get_actions()
        obs[self.ObsIndexes.CART_VEL.value] = state[self.StatesIndex.CART_VEL.value]
        obs[self.ObsIndexes.PEND_POS.value] = state[self.StatesIndex.PEND_POS.value]
        obs[self.ObsIndexes.PEND_VEL.value] = state[self.StatesIndex.PEND_VEL.value]
        obs[self.ObsIndexes.PREV_ACT.value] = actions[0]
        return obs

    def get_reward(self, observations: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        rew = torch.tensor(data=0, dtype=torch.float)
        assert 0 <= observations[self.ObsIndexes.PEND_POS.value] < 2 * torch.pi, f"Angle must be in [0, 2pi). Got {observations[self.ObsIndexes.PEND_POS.value]}"
        if observations[self.ObsIndexes.PEND_POS.value] <= torch.pi:
            rew += torch.exp(-((observations[self.ObsIndexes.PEND_POS.value]) ** 2) / 1)
        else:
            rew += torch.exp(-((2 * torch.pi - observations[self.ObsIndexes.PEND_POS.value]) ** 2) / 1)
        rew += 0.1 * torch.exp(-((observations[self.ObsIndexes.PREV_ACT.value]) ** 2) / 1)
        return rew

    def plot_rollout(self, obs: torch.Tensor):
        fig, ax = plt.subplots(ncols=2, nrows=2)
        ax: List[List[Axes]]
        ax[0][0].plot(obs[:, self.ObsIndexes.CART_VEL.value], label="cart vel")
        ax[0][1].plot(obs[:, self.ObsIndexes.PEND_POS.value], label="pend pos")
        ax[1][0].plot(obs[:, self.ObsIndexes.PEND_VEL.value], label="pend vel")
        ax[1][1].plot(obs[:, self.ObsIndexes.PREV_ACT.value], label="prev act")
        ax[0][0].legend()
        ax[0][1].legend()
        ax[1][0].legend()
        ax[1][1].legend()
        plt.show()

    def get_action_constraints(self) -> torch.Tensor:
        max_applied_input = [100]
        return torch.tensor(data=max_applied_input)
    
    def get_state_constraints(self) -> torch.Tensor:
        max_cart_pos = 1
        max_cart_vel = 0
        max_pend_pos = 1
        max_pend_vel = 0
        constraints = [max_cart_pos, max_cart_vel, max_pend_pos, max_pend_vel]
        return torch.tensor(data=constraints)
    
class AnimationInvertedPendulum(InvertedPendulum):
    def __init__(self, actor_model_path) -> None:
        super().__init__()
        matplotlib.use('TkAgg')
        self.time_data = []
        self.cart_pos_data = []
        self.cart_vel_data = []
        self.pend_ang_data = []
        self.pend_vel_data = []
        self.input_data = []
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

        ax_cart_pos = ax[0][0]
        ax_cart_vel = ax[1][0]
        ax_pend_ang = ax[0][1]
        ax_pend_vel = ax[1][1]
        ax_input = ax[0][2]
        ax_animation = ax[1][2]

        (line_cart_pos,) = ax_cart_pos.plot([], [], label="Cart Position")
        (line_cart_vel,) = ax_cart_vel.plot([], [], label="Cart Velocity")
        (line_pend_ang,) = ax_pend_ang.plot([], [], label="Pendulum Angle")
        (line_pend_vel,) = ax_pend_vel.plot([], [], label="Pendulum Velocity")
        (line_input,) = ax_input.plot([], [], label="Input Signal")
        (line_animation,) = ax_animation.plot([], [], label="Animation")

        ax_cart_pos.set_title("Cart Position")
        ax_cart_pos.set_xlabel("Time (s)")
        ax_cart_pos.set_ylabel("Cart Position (m)")

        ax_cart_vel.set_title("Cart Velocity")
        ax_cart_vel.set_xlabel("Time (s)")
        ax_cart_vel.set_ylabel("Cart Velocity (m/s)")

        ax_pend_ang.set_title("Pendulum Angle")
        ax_pend_ang.set_xlabel("Time (s)")
        ax_pend_ang.set_ylabel("Pendulum Angle (rad)")

        ax_pend_vel.set_title("Pendulum Velocity")
        ax_pend_vel.set_xlabel("Time (s)")
        ax_pend_vel.set_ylabel("Pendulum Velocity (rad/s)")

        ax_input.set_title("Input Signal vs Time")
        ax_input.set_xlabel("Time (s)")
        ax_input.set_ylabel("Input Signal")

        ax_animation.set_title("Animation")
        ax_animation.set_xlabel("x")
        ax_animation.set_ylabel("y")

        cart = patches.Rectangle((0, 0), 0.2, 0.1, linewidth=2, edgecolor="r", facecolor="none")
        pendulum = patches.FancyArrow(0, 0, 0.0, 1.0, head_width=0.0,head_length=0.0, linewidth=2, edgecolor="g")

        ax_animation.add_patch(cart)
        ax_animation.add_patch(pendulum)

        def init():
            line_cart_pos.set_data([], [])
            line_cart_vel.set_data([], [])
            line_pend_ang.set_data([], [])
            line_pend_vel.set_data([], [])
            line_input.set_data([], [])
            ax_cart_pos.set_xlim(0, 10)
            ax_cart_vel.set_xlim(0, 10)
            ax_pend_ang.set_xlim(0, 10)
            ax_pend_vel.set_xlim(0, 10)
            ax_animation.set_xlim(-2, 2)
            ax_input.set_xlim(0, 10)
            ax_cart_pos.set_ylim(-5, 10)
            ax_cart_vel.set_ylim(-5, 10)
            ax_pend_ang.set_ylim(-5, 10)
            ax_pend_vel.set_ylim(-5, 10)
            ax_input.set_ylim(-5, 10)
            ax_animation.set_ylim(-2, 2)
            return line_cart_pos, line_cart_vel, line_pend_ang, line_pend_vel, line_input, line_animation

        def update(frame):
            self.mdp_step()
            actions = self.get_actions()
            self.time += self.get_time()
            state = self.get_state()
            cart_pos: float = state[self.StatesIndex.CART_POS]
            cart_vel: float = state[self.StatesIndex.CART_VEL]
            pend_ang: float = state[self.StatesIndex.PEND_POS]
            pend_vel: float = state[self.StatesIndex.PEND_VEL]
            input_signal: float = actions[0]
            print(f"self.time = {self.time} cart_pos = {cart_pos} cart_vel = {cart_vel} pend_ang = {pend_ang} pend_vel = {pend_vel} input_signal = {input_signal}")

            self.time_data.append(self.time)
            self.cart_pos_data.append(cart_pos)
            self.cart_vel_data.append(cart_vel)
            self.pend_ang_data.append(pend_ang)
            self.pend_vel_data.append(pend_vel)
            self.input_data.append(input_signal)

            line_cart_pos.set_data(self.time_data, self.cart_pos_data)
            line_cart_vel.set_data(self.time_data, self.cart_vel_data)
            line_pend_ang.set_data(self.time_data, self.pend_ang_data)
            line_pend_vel.set_data(self.time_data, self.pend_vel_data)
            line_input.set_data(self.time_data, self.input_data)

            cart.set_xy((cart_pos-0.1, -0.1))
            pendulum.set_data(x=cart_pos, y=0, dx=numpy.sin(pend_ang), dy=numpy.cos(pend_ang))
            nonlocal remaining_steps
            remaining_steps -= 1
            print(f"Remaining steps = {remaining_steps}/{steps}")
            if remaining_steps ==0:
                sys.exit()
            return line_cart_pos, line_cart_vel, line_pend_ang, line_pend_vel, line_input, line_animation

        ani = animation.FuncAnimation(fig, update, frames=1, init_func=init, blit=False, interval=1)
        # Adjust layout
        plt.tight_layout()
        plt.show()
        
    def _mdp_step(self):
        s = self.get_observations()
        a = self.actor(s) * self.get_action_constraints() # todo fix this
        s = self.step(a)