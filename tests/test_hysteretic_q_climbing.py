'''
testing hysteretic_q learning on the climbing game.
'''
from matplotlib import pyplot as plt
import numpy as np

from environments.env_climbling import Climbing
from learning_algorithms.hysteretic_q_matrix import HystereticAgentMatrix


def moving_average(a, n=20) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def main():
    env = Climbing()
    learning = HystereticAgentMatrix(environment=env)

    for i in range(1000):
        learning.step()

    reward_1, reward_2 = learning.get_rewards()
    reward_1 = np.asarray(reward_1)
    reward_2 = np.asarray(reward_2)

    avgrewards_1, avgrewards_2 = learning.get_averaged_rewards()
    avgrewards_1 = np.asarray(avgrewards_1)
    avgrewards_2 = np.asarray(avgrewards_2)

    reward_1_moving_average = moving_average(reward_1)

    plt.plot(avgrewards_1)
    plt.title('Climbing game, average reward')
    plt.ylabel('average_reward')
    plt.xlabel('episode')
    plt.show()


if __name__ == "__main__":
    main()
