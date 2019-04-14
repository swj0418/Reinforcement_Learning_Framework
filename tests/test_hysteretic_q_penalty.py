'''
testing hysteretic_q learning on the climbing game.
'''

from matplotlib import pyplot as plt

from environments.env_penalty import Penalty
from learning_algorithms.hysteretic_q_matrix import HystereticAgentMatrix


if __name__ == "__main__":
    env = Penalty()
    agent_1 = HystereticAgentMatrix(environment=env, agent_id=0)
    agent_2 = HystereticAgentMatrix(environment=env, agent_id=1)

    for i in range(500):
        agent_1.step()
        agent_2.step()

    rewards_1 = agent_1.get_rewards()
    rewards_2 = agent_2.get_rewards()

    plt.plot(rewards_1)
    # plt.plot(rewards_2)
    plt.show()
