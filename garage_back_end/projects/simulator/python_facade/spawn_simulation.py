from binder import SimulationFacade
from matplotlib import pyplot as plt
from matplotlib import patches
from typing import List
import matplotlib.animation as animation
import numpy
import matplotlib
import sys

class SimulationPy:
    def __init__(self) -> None:
        self._sim = SimulationFacade()
        self._sim.setSystemInvertedPendulum()
        self.time_data = []
        self.cart_pos_data = []
        self.cart_vel_data = []
        self.pend_ang_data = []
        self.pend_vel_data = []
        self.input_data = []
        self.time = 0
        self.plot_period_s = 0.1

    def run(self, steps: int):
        self._sim.setState([0.0, 0.0, 1.0, 0.0])
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
            print(f"before")
            self._sim.simulate(True, self.plot_period_s)
            print(f"after")
            self.time += self._sim.getTime()
            state = self._sim.getState()
            cart_pos: float = state[0]
            cart_vel: float = state[1]
            pend_ang: float = state[2]
            pend_vel: float = state[3]
            input_signal: float = self._sim.getInput()[0]
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

def run_simulation(steps: int):
    sim_py = SimulationPy()
    sim_py.run(steps)
    
if __name__ == "__main__":
    matplotlib.use('TkAgg')
    run_simulation(10000)
