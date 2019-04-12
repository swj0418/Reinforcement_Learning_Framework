import os
import sys
import numpy as np

from env_interface import ReinforcementLearningEnvironment


class Action:
    def __init__(self):
        self.n = 2 # a and b ==> 0 and 1

    def sample(self):
        s = np.random.randint(0, 1)
        return s


class Observation:
    def __init__(self):
        pass


class Boutilier(ReinforcementLearningEnvironment):
    def __init__(self):
        ReinforcementLearningEnvironment.__init__(self)
        self.action = Action()

        self.reward = {}
        self.k = -100

        # Sets up a reward function
        self.__generate_reward_function()

    def step(self, action):
        """
        Take an action given by the policy and give evaluative feedback.

        :param action: An index of an action space.
        :return:
                observation:
                reward:
                done:
                val:
        """
        observation = None
        reward = None
        done = False
        val = None

        # Converts action index into a concrete action that is in an action space
        concrete_action = self.actions[action]

        # Bound check for grid world



        pass

    def reset(self):

        return True

    def is_out_of_bound(self, concrete_action):
        pass

    def __generate_reward_function(self):
        self.reward[1] = 0 # S1
        self.reward[2] = 0
        self.reward[3] = 0
        self.reward[4] = 11
        self.reward[5] = self.k
        self.reward[6] = 7
