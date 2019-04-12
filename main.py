import os
import sys
import gym
from gym import spaces

from learner import Learner

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

    learner = Learner(env.observation_space.high, env.observation_space.low, env.action_space.n)

    # Initial step / Random action
    sample = env.action_space.sample()
    observation, reward, done, val = env.step(action=sample)

    for epoch in range(100):
        action = learner.get_action(observation)
        observation, reward, done, val = env.step(action=action)

        learner.update(observation, reward)

        if done:
            break
