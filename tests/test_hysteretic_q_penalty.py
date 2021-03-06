'''
testing hysteretic_q learning on the penalty game.
'''

from matplotlib import pyplot as plt
import numpy as np

from environments.env_penalty import Penalty
from learning_algorithms.hysteretic_q_matrix import HystereticAgentMatrix

episodes = 1
epochs = 300
exp_rate = 0.01
exp_rate_decay = 0.999

def run_episode():
    env = Penalty()
    learning = HystereticAgentMatrix(environment=env, exploration_rate=exp_rate)

    for i in range(epochs):
        learning.step()

    reward_1, reward_2 = learning.get_rewards()

    """
    plt.plot(reward_1)
    plt.show()
    """
    rewards_1, rewards_2 = learning.get_averaged_rewards()
    rewards_1 = np.asarray(rewards_1)
    rewards_2 = np.asarray(rewards_2)

    """
    plt.plot(rewards_1)
    plt.title("Penalty Game, K = -3")
    plt.xlabel("steps")
    plt.ylabel("average_reward")
    plt.show()
    """
    return rewards_1

if __name__ == "__main__":
    overall = np.zeros(shape=(epochs - 1,))
    for episode in range(episodes):
        overall += run_episode()
        print("Episode ", episode)
        #exp_rate = exp_rate * exp_rate_decay
        #print(exp_rate)

    plt.plot(overall / episodes)
    plt.xlabel("Epochs")
    plt.ylabel("Averaged Rewards (Averaged over all episodes)")
    plt.show()

