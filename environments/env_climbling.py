import os
import sys

import numpy as np

class Action:
    def __init__(self):
        # a and b ==> 0 and 1
        self.n = 3

        self.values = [0, 1, 2]

    def sample(self):
        s = np.random.randint(0, self.n)
        return s

    def __getitem__(self, key):
        return self.values[key]

class Observation:
    """
    Observation function gives a position of an agent
    """
    def __init__(self, initial_position=(0,0)):
        pass


class States:
    """
    Default size of a climbing game is 9 (3x3)
    States object also contains all other agents in the environment if there are.
    """
    def __init__(self, dim_x=3, dim_y=3, agents_n=2):
        self.n = dim_x * dim_y
        self.agents_n = agents_n
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.default_initial_position = (1, 1)

class Climbing:
    def __init__(self):
        self.actions = Action()
        self.states = States(dim_x=1, dim_y=1, agents_n=2)
        self.observation = Observation()
        self.reward = {}

        # Sets up a reward function
        self.__generate_reward_function()

    def step(self, action, agent_id=0):
        observation = None
        reward = None
        done = False
        val = None

        if np.random.randint(0, 100) < 50:
            reward = self.reward[action[0]][action[1]]
        else:
            if action[0] == 1 and action[1] == 1:
                reward = 14
            else:
                reward = self.reward[action[0]][action[1]]


        return observation, reward, done, val

    def reset(self):
        return True

    def __generate_reward_function(self):
        """
        Reward function must have a randomness in it for 2, 2 position
        50% of 0 and 50% of 14 (Paritially Stochastic Games)
        :return:
        """
        K = -3
        self.reward = np.array([[11, -30, 0],
                                [-30,  7, 6],
                                [0,    0, 5]])

