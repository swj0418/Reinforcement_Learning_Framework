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

class Penalty:
    def __init__(self):
        self.actions = Action()
        self.reward = {}

        # Sets up a reward function
        self.__generate_reward_function()

    def step(self, action):
        observation = None
        reward = None
        done = False
        val = None




        # Converts action index into a concrete action that is in an action space
        concrete_action = self.actions[action]

        return observation, reward, done, val

    def reset(self):
        return True

    def __generate_reward_function(self):
        """
        Reward function must have a randomness in it for 2, 2 position
        50% of 0 and 50% of 14 (Paritially Stochastic Games)
        :return:
        """
        self.reward = np.array([[11, -30, 0],
                                [-30, 14, 6],
                                [0,   0,  5]])

