import numpy as np

from environments.env_interface import ReinforcementLearningEnvironment


class Action:
    def __init__(self):
        self.n = 2 # a and b ==> 0 and 1

    def sample(self):
        s = np.random.randint(0, 1)
        return s


class Observation:
    def __init__(self):
        pass


class Boutilier():
    def __init__(self):
        self.action = Action()
        self.state = 0

        self.reward = {}
        self.k = -3

        # Sets up a reward function
        self.__generate_reward_function()

    def step(self, actions):
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

        if self.state == 0:
            if actions[0] == 0:
                self.state = 1
                reward = self.reward[self.state]
            else:
                self.state = 2
                reward = self.reward[self.state]
        elif self.state == 1:
            if actions[0] == actions[1]:
                self.state = 3
                reward = self.reward[self.state] # 11
                done = True
            else:
                self.state = 4
                reward = self.reward[self.state]
                done = True
        elif self.state == 2:
            self.state = 5
            reward = self.reward[self.state]
            done = True

        observation = self.state

        return observation, reward, done, val

    def reset(self):
        self.state = 0
        return True

    def is_out_of_bound(self, concrete_action):
        pass

    def __generate_reward_function(self):
        self.reward[0] = 0 # S1
        self.reward[1] = 0
        self.reward[2] = 0
        self.reward[3] = 11
        self.reward[4] = self.k
        self.reward[5] = 7
