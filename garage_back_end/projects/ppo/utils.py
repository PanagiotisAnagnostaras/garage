from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from env import Env, ObsIndexes
from typing import List

def plot_rollout(obs):
    fig, ax = plt.subplots(ncols=2, nrows=2)
    ax: List[List[Axes]]
    ax[0][0].plot(obs[:, ObsIndexes.CART_VEL.value], label="cart vel")
    ax[0][1].plot(obs[:, ObsIndexes.PEND_POS.value], label="pend pos")
    ax[1][0].plot(obs[:, ObsIndexes.PEND_VEL.value], label="pend vel")
    ax[1][1].plot(obs[:, ObsIndexes.PREV_ACT.value], label="prev act")
    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()
    plt.show()
