import os
import sys
from enum import Enum
import numpy as np

from environments.env_interface import ReinforcementLearningEnvironment
from environments.env_climbling import Climbing


class Environments(Enum):
    climbing = 'climbing'
    boutilier = 'boutilier'
    gridworld = 'gridworld'
    penalty = 'penalty'
    antworld = 'antworld'

class HystereticAgent:
    def __init__(self, environment, learning_rate=0.1, discount_factor=0.9):
        self.environment = environment
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        # Setup q_table
        self.num_of_action = self.environment.actions.n
        self.states_dim_x = self.environment.states.dim_x
        self.states_dim_y = self.environment.states.dim_y

        self.q_table = np.zeros(shape=(self.states_dim_x * self.states_dim_y, self.num_of_action))

        #
        self.agents = []

    def run(self):
        observation, reward, done, val = self.environment.step(action=1)

        while not done:
            # Determine action

            obs, reward, done, val = self.environment.step(action=2)
            print(reward)







if __name__ == "__main__":
    env = Climbing()
    agent_1 = HystereticAgent(environment=env)
    agent_1.run()
