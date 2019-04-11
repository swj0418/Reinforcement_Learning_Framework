import os
import sys
import gym
from gym import spaces

from QLearning import QLearning

if __name__ == '__main__':
    env = gym.make('CartPole-v1')
    obs = env.reset()

    num_of_actions = env.action_space.n
    num_of_states_1 = env.observation_space.shape[0]
    num_of_states_0 = 0
    try:
        num_of_states_0 = env.observation_space.shape[1]
    except:
        pass

    Q = QLearning(state_dim=(num_of_states_0, num_of_states_1))

    for epoch in range(100):
        action = Q.take_action(0.1)
        print(action)
        observation, reward, done, val = env.step(action=1)

        if done:
            break
