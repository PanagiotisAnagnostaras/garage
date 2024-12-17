from binder import Simulation
import threading
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from typing import List
import matplotlib.animation as animation
import concurrent.futures

class SimulationPy:
    def __init__(self) -> None:
        self._sim = Simulation()
        self.time_data = []
        self.cart_pos_data = []
        self.cart_vel_data = []
        self.pend_ang_data = []
        self.pend_vel_data = []
        self.input_data = []
        self.time = 0
        self.plot_period_s = 0.1
           
    def plot(self):
        fig, ax = plt.subplots(ncols=3, nrows=2)
        ax: List[List[plt.Axes]]
        fig: Figure
        fig.delaxes(ax[1, 2])

        ax_cart_pos = ax[0][0]
        ax_cart_vel = ax[1][0]
        ax_pend_ang = ax[0][1]
        ax_pend_vel = ax[1][1]
        ax_input = ax[0][2]

        line_cart_pos, = ax_cart_pos.plot([], [], label="Cart Position")
        line_cart_vel, = ax_cart_vel.plot([], [], label="Cart Velocity")
        line_pend_ang, = ax_pend_ang.plot([], [], label="Pendulum Angle")
        line_pend_vel, = ax_pend_vel.plot([], [], label="Pendulum Velocity")
        line_input, = ax_input.plot([], [], label="Input Signal")

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
            ax_input.set_xlim(0, 10)
            ax_cart_pos.set_ylim(-5, 10)
            ax_cart_vel.set_ylim(-5, 10)
            ax_pend_ang.set_ylim(-5, 10)
            ax_pend_vel.set_ylim(-5, 10)
            ax_input.set_ylim(-5, 10)
            return line_cart_pos, line_cart_vel, line_pend_ang, line_pend_vel, line_input
        
        def update(frame):
            self._sim.run(self.plot_period_s)
            self.time += self._sim.getTime()
            cart_pos: float = self._sim.getCartPos()
            cart_vel: float = self._sim.getCartVel()
            pend_ang: float = self._sim.getPendAng()
            pend_vel: float = self._sim.getPendVel()
            input_signal: float = self._sim.getInput()
            print(f"Time: {self.time}, Cart Position: {cart_pos}, Cart Velocity: {cart_vel}, Pendulum Angle: {pend_ang}, Pendulum Velocity: {pend_vel}, Input Signal: {input_signal}")

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
            return line_cart_pos, line_cart_vel, line_pend_ang, line_pend_vel, line_input
        
        ani = animation.FuncAnimation(
            fig, update, frames=1, init_func=init, blit=True, interval=1
        )
        # Adjust layout
        plt.tight_layout()
        plt.show()
            
if __name__ == '__main__':
    sim_py = SimulationPy()
    sim_py.plot()
