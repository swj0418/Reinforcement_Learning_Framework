'''
testing hysteretic_q learning on the penalty game.
'''

from matplotlib import pyplot as plt
import numpy as np

from environments.env_penalty import Penalty
from learning_algorithms.hysteretic_q_matrix import HystereticAgentMatrix


if __name__ == "__main__":
    env = Penalty()
    learning = HystereticAgentMatrix(environment=env)

    for i in range(10000):
        learning.step()

    reward_1, reward_2 = learning.get_rewards()

    """
    plt.plot(reward_1)
    plt.show()
    """
    rewards_1, rewards_2 = learning.get_averaged_rewards()
    rewards_1 = np.asarray(rewards_1)
    rewards_2 = np.asarray(rewards_2)

    plt.plot(rewards_1)
    plt.show()
