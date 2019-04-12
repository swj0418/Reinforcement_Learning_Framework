import os
import sys

import numpy as np


class Learner:
    """
    Learner class.
    It is responsible for keeping information about value function
    Implementing Q learning for testing.

    Q-learning requires a reward feedback

    Learner is responsible for keeping its Q-table

    Q-table's row corresponds to a size of states.
    Q-table's column corresponds to a size of actions.

    """
    def __init__(self, num_of_actions, num_of_states):
        """
        Initializes Q table and other values for updating a table.
        :param num_of_actions:
        :param num_of_states:
        """
        self.num_of_states = num_of_states
        self.num_of_actions = num_of_actions
        self.q_table = np.zeros(shape=(num_of_states, num_of_actions))

    def get_action(self):
        """
        Function returns an action that will be chosen by a given algorithm.
        TODO: Create abstraction for future plug-n-play algorithms.
        :return: action
        """




    def reset(self):
        """
        Resets a Q table
        :return: boolean:
        """

        self.q_table = np.zeros(shape=(self.num_of_states, self.num_of_actions))

