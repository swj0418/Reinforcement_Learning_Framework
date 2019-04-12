import os
import sys
import numpy as np

from env_interface import ReinforcementLearningEnvironment


class Action:
    def __init__(self):
        # a and b ==> 0 and 1
        self.n = 4

        # Action VALUES // NORTH, EAST, SOUTH, WEST
        self.values = [(0, -1), (1, 0), (0, 1), (-1, 0)]

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
    def __init__(self, dim_x=3, dim_y=3):
        self.n = dim_x * dim_y
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.world = np.zeros(shape=(dim_y, dim_x))

    def check_world(self):
        """
        Checks if there are any other agents in a tile
        :return:
        """


class Climbing(ReinforcementLearningEnvironment):
    def __init__(self):
        ReinforcementLearningEnvironment.__init__(self)
        self.actions = Action()
        self.states = States(dim_x=3, dim_y=3)
        self.observation = Observation()

        self.reward = {}

        # Sets up a reward function
        self.__generate_reward_function()

    def step(self, action):
        """
        Take an action given by the policy and give evaluative feedback.

        If an action is not a valid action, i.e., out of bound, step function will directly return False for val.

        :param action: An index of an action space.
        :return:
                observation:
                reward:
                done:
                val: checking whether an action proposed by an agent is a valid action or not.
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
        self.reward = np.array([[]])
