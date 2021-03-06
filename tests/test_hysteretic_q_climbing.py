'''
testing hysteretic_q learning on the climbing game.
'''
from matplotlib import pyplot as plt
import numpy as np

from environments.env_climbling import Climbing
from learning_algorithms.hysteretic_q_matrix import HystereticAgentMatrix

episodes = 5000
epochs = 300
exp_rate = 0.5
exp_rate_decay = 0.999

def moving_average(a, n=20) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def run_episode(agent):
    for i in range(epochs):
        agent.step()

    reward_1, reward_2 = agent.get_rewards()
    reward_1 = np.asarray(reward_1)
    reward_2 = np.asarray(reward_2)

    avgrewards_1, avgrewards_2 = agent.get_averaged_rewards()
    avgrewards_1 = np.asarray(avgrewards_1)
    avgrewards_2 = np.asarray(avgrewards_2)

    reward_1_moving_average = moving_average(reward_1)
    """
    plt.plot(avgrewards_1)
    plt.title('Climbing game, average reward')
    plt.ylabel('average_reward')
    plt.xlabel('episode')
    plt.show()
    """
    return reward_1


if __name__ == "__main__":
    env = Climbing()
    agent = HystereticAgentMatrix(environment=env, exploration_rate=exp_rate)

    overall = np.zeros(shape=(epochs, ))
    for episode in range(episodes):
        overall += run_episode(agent)
        print("Episode ", episode)
        exp_rate = exp_rate * exp_rate_decay
        agent.set_exploration_rate(exp_rate)
        agent.reset_reward()
        print(exp_rate)

    plt.plot(overall / episodes)
    plt.xlabel("Epochs")
    plt.ylabel("Averaged Rewards (Averaged over all episodes)")
    plt.show()
