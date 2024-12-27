from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
from typing import List
import numpy as np
import matplotlib.animation as animation

# Load data from CSV
df = pd.read_csv(
    filepath_or_buffer="/projects/simulator/src/inverted-pendulum/scripts/simulation.txt", sep=","
)
df = df[df["time"] != 0]

# Extract relevant data
time = df["time"]
cart_pos = df["cart pos"]
cart_vel = df["cart vel"]
pend_ang = df["pend ang"]
pend_vel = df["pend vel"]
input_signal = df["input"]


# Create the figure and axes
fig, ax = plt.subplots(ncols=3, nrows=2)
ax: List[List[plt.Axes]]
fig: Figure

# Hide the unused subplot (ax[1, 2])
fig.delaxes(ax[1, 2])

# Define the plot lines for animation
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

# Plot the initial data
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

# Initialize the plot
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

# Animation update function
def update(frame):
    df = pd.read_csv(
    filepath_or_buffer="/projects/simulator/src/inverted-pendulum/scripts/simulation.txt", sep=","
    )
    df = df[df["time"] != 0]

    # Extract relevant data
    time = df["time"]
    cart_pos = df["cart pos"]
    cart_vel = df["cart vel"]
    pend_ang = df["pend ang"]
    pend_vel = df["pend vel"]
    input_signal = df["input"]
    # Update the data for each plot
    line_cart_pos.set_data(time, cart_pos)
    line_cart_vel.set_data(time, cart_vel)
    line_pend_ang.set_data(time, pend_ang)
    line_pend_vel.set_data(time, pend_vel)
    line_input.set_data(time, input_signal)
    return line_cart_pos, line_cart_vel, line_pend_ang, line_pend_vel, line_input

# Create the animation
ani = animation.FuncAnimation(
    fig, update, frames=100, init_func=init, blit=True, interval=100
)
# Adjust layout
plt.tight_layout()
manager = plt.get_current_fig_manager()
manager.window.attributes('-fullscreen', True)
plt.show()