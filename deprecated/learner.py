import os
import sys
import numpy as np


class Learner:
    def __init__(self, obs_high, obs_low, num_of_actions):
        """
        Given information from the environment
        """

        self.num_of_actions = num_of_actions

        self.determine_states(obs_high, obs_low)

    def determine_states(self, obs_high, obs_low, discrete_cut=10):
        """

        :param obs_high: Highest value of an observation
        :param obs_low: Lowest value of an observation
        :param discrete_cut: An extent to which states will be discretized. A value for creating a bucket
        :return:
                state_category: Number of a category of a state
                state: Discretized map of a state. A bucket
        """
        diff = obs_high - obs_low
        state_category = len(obs_high)

        state = []

        for s in diff: # For all state categories
            individual_bucket = []
            for i in range(0, discrete_cut):
                individual_bucket.append(0)

        return state_category


    def get_action(self, observation):


        return 1

    def update(self, observation, reward):
        """
        Updating Value function based on an observation and a reward from taking the last action.
        :param observation:
        :param reward:
        :return:
        """
        pass
