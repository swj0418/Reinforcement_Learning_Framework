import os
import sys
import numpy as np

from env_interface import ReinforcementLearningEnvironment

class GridWorld(ReinforcementLearningEnvironment):
    def __init__(self):
        ReinforcementLearningEnvironment.__init__(self)
        self.reward = np.zeros(shape=(5, 5))
        self.position = (0, 0) # Initial (Starting) Position

        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # 0, 1, 2, 3 Index

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
        self.position = (0, 0)

        return True

    def is_out_of_bound(self, concrete_action):
        pass