import os
import sys
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

from environments.env_interface import ReinforcementLearningEnvironment
from environments.env_climbling import Climbing


class Environments(Enum):
    climbing = 'climbing'
    boutilier = 'boutilier'
    gridworld = 'gridworld'
    penalty = 'penalty'
    antworld = 'antworld'


class HystereticAgent:
    def __init__(self, environment, agent_id, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.environment = environment
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.agent_id = agent_id
        self.alpha = 0.3
        self.beta = 0.7

        # Setup q_table
        self.num_of_action = self.environment.actions.n
        self.states_dim_x = self.environment.states.dim_x
        self.states_dim_y = self.environment.states.dim_y

        self.q_table = np.zeros(shape=(self.states_dim_x * self.states_dim_y, self.num_of_action))
        self.position_index = self.actual_to_index(self.environment.states.default_initial_position)

        self.rewards = []

    def run(self):
        done = False

        steps = 0
        total_rewards = 0
        while not done:

            # Determine action
            action = self.get_action()

            # Previous State capture (Previous q value, previous position)
            q_p = self.q_table[self.position_index][action]
            pos_p = self.position_index

            # Take action
            obs, reward, done, val = self.environment.step(action=action, agent_id=self.agent_id)
            self.position_index = self.actual_to_index(obs[self.agent_id])

            # Update Q-table
            delta = reward + self.discount_factor* (np.max(self.q_table[self.position_index]) - q_p)

            if delta >= 0:
                new_q = q_p + self.alpha * delta
            else:
                new_q = q_p + self.alpha * delta

            self.q_table[pos_p][action] = new_q

            total_rewards += reward
            steps += 1

            self.rewards.append(total_rewards / steps)

            if steps == 500:
                break


    def index_to_actual(self, index):
        x = index % self.states_dim_y
        y = index // self.states_dim_x

    def actual_to_index(self, actual):
        index = actual[0] * self.states_dim_x + actual[1]
        return index

    def get_action(self):
        if np.random.randint(0, 100) / 100 < self.exploration_rate:
            # Explore
            action = np.random.randint(0, self.num_of_action)

        else:
            action = np.argmax(self.q_table[self.position_index])

        return action

    def get_rewards(self):
        return self.rewards


if __name__ == "__main__":
    env = Climbing()
    agent_1 = HystereticAgent(environment=env, agent_id=0)
    agent_1.run()

    rewards = agent_1.get_rewards()

    plt.plot(rewards)
    plt.show()
