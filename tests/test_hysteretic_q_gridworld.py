'''
testing hysteretic_q learning on the climbing game.
'''

from matplotlib import pyplot as plt

from environments.env_gridworld import GridWorld
from learning_algorithms.hysteretic_q import HystereticAgent


if __name__ == "__main__":
    env = GridWorld()
    agent_1 = HystereticAgent(environment=env, agent_id=0)
    agent_2 = HystereticAgent(environment=env, agent_id=1)

    for i in range(500):
        agent_1.step()
        agent_2.step()

    rewards_1 = agent_1.get_rewards()
    rewards_2 = agent_2.get_rewards()

    plt.plot(rewards_1)
    # plt.plot(rewards_2)
    plt.show()
