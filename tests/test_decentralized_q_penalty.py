'''
testing decentralized_q learning on the climbing game.
'''

from matplotlib import pyplot as plt
import numpy as np

from environments.env_penalty import Penalty
from learning_algorithms.decentralized_q_matrix import DecentralizedAgentMatrix

episodes = 1000
epochs = 1000
exp_rate = 0.01
exp_rate_decay = 0.999

def run_episode(agent):
    for i in range(epochs):
        agent.step()

    reward_1, reward_2 = agent.get_rewards()
    reward_1 = np.asarray(reward_1)
    reward_2 = np.asarray(reward_2)

    avgrewards_1, avgrewards_2 = agent.get_averaged_rewards()
    avgrewards_1 = np.asarray(avgrewards_1)
    avgrewards_2 = np.asarray(avgrewards_2)

    return (avgrewards_1 + avgrewards_2) / 2


if __name__ == "__main__":
    env = Penalty()
    agent = DecentralizedAgentMatrix(environment=env, exploration_rate=exp_rate)

    overall = np.zeros(shape=(epochs, ))
    for episode in range(episodes):
        r = run_episode(agent)

        overall = np.add(overall, r)

        print("Episode ", episode)
        agent.reset_reward()

    plt.plot(overall / episodes)
    plt.xlabel("Epochs")
    plt.ylabel("Averaged Rewards (Averaged over all episodes)")
    plt.show()
