'''
testing hysteretic_q learning on the boutilier
'''

from matplotlib import pyplot as plt
import numpy as np

from environments.env_boutilier import Boutilier
from learning_algorithms.hysteretic_q_boutilier import HystereticAgentBoutilier

episodes = 1000
epochs = 300
exp_rate = 0.01
exp_rate_decay = 0.999

def run_episode():
    env = Boutilier()
    learning = HystereticAgentBoutilier(environment=env, exploration_rate=exp_rate)

    for i in range(epochs):
        learning.step()

    reward_1, reward_2 = learning.get_rewards()

    rewards_1, rewards_2 = learning.get_averaged_rewards()
    rewards_1 = np.asarray(rewards_1)
    rewards_2 = np.asarray(rewards_2)

    return rewards_2 + rewards_1

if __name__ == "__main__":
    overall = np.zeros(shape=(epochs - 1,))

    for episode in range(episodes):
        overall += run_episode()
        print("Episode ", episode)

    plt.plot(overall / episodes)
    plt.xlabel("Epochs")
    plt.ylabel("Averaged Rewards (Averaged over all episodes)")
    plt.show()