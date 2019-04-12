from env_climbling import *
from learner import *

if __name__ == '__main__':
    env = Climbing()

    learner = Learner(env.actions.n, env.states.n)

    for simulation in range(5):
        # Complete one simulation
        for i in range(10):
            env.step(action=1)
