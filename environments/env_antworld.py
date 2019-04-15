import os
import sys

import numpy as np

class Action:
    def __init__(self):
        # a and b ==> 0 and 1
        self.n = 5

        # Action VALUES // NORTH, EAST, SOUTH, WEST
        self.values = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]

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
    def __init__(self, dim_x=20, dim_y=20, agents_n=2):
        self.n = dim_x * dim_y
        self.agents_n = agents_n
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.default_initial_position = (10, 10)

class Ant:
    def __init__(self,my_id):
        self.position = (10,10)
        self.id = my_id
        self.carrying = False

class Pheromone:
    def __init__(self,position):
        self.position = position
        self.age = 0

class Antworld:
    def __init__(self,dim_x=20, dim_y=20, agents_n=2):
        self.actions = Action()
        self.states = States(dim_x=dim_x, dim_y=dim_y, agents_n=agents_n)
        self.observation = Observation()
        self.reward = {}
        self.max_pheromone_age = 300

        self.ants = [Ant(x) for x in agents_n]
        self.pheromones = []

        self.home_position = (10,10)
        self.food_position = (15,15)
        #right now agents are tuples: x, y, id, carrying

        # Sets up a reward function
        self.__generate_reward_function()

    def display(self):
        worldDisplay = [['.' for _ in self.dim_x] for _ in self.dim_y]
        worldDisplay[self.home_position] = 'H'
        worldDisplay[self.food_position] = 'F'

        for a in self.ants:
            if a[0] >= 0 and a[0] < self.dim_x and a[1] >= 0 and a[1] < self.dim_y:
                worldDisplay[a[0],a[1]] = 'a'
        for a in self.pheromones:
            if a[0] >= 0 and a[0] < self.dim_x and a[1] >= 0 and a[1] < self.dim_y:
                worldDisplay[a[0],a[1]] = 'p'

        out = ''
        for y in range(dim_y):
            for x in range(dim_x):
                out += str(worldDisplay[x,y])
            out += '\n'
        print(out)

    def step(self, actions, agent_ids):
        observation = None
        reward = None
        done = False
        valid = None

        rewards = [0 for _ in agent_ids]
        joint_reward = 0

        # pheromone timetables

        for pheromone in self.pheromones:
            pheromone.age += 1
            if pheromone.age > self.max_pheromone_age:
                self.pheromones.remove(pheromone)

        # move agents and get rewards

        for num in agent_ids:
            action = actions(num)
            agent = ants(num)
            agent.position += self.actions.values[action]
            if action == 4:
                self.pheromones += [Pheromone(agent.position)]
            if agent.carrying and agent.position == self.home_position:
                agent.carrying = False
                joint_reward += 1
                rewards[num] += 1 #give the bringer the best reward
            else if agent.position = self.food_position:
                agent.carrying = True

        for reward in rewards:
            reward += joint_reward #is this by reference?


        # generate observations

        observations = []
        observation = ''

        world = [['.' for _ in self.dim_x] for _ in self.dim_y]
        world[self.home_position] = 'H'
        world[self.food_position] = 'F'

        for a in self.ants:
            if a[0] >= 0 and a[0] < self.dim_x and a[1] >= 0 and a[1] < self.dim_y:
                world[a[0],a[1]] = 'a'
        for a in self.pheromones:
            if a[0] >= 0 and a[0] < self.dim_x and a[1] >= 0 and a[1] < self.dim_y:
                world[a[0],a[1]] = 'p'


        for ant in self.ants:
            for y in [ant.position-1:ant.position+2]:
                if y < 0 or y >= self.dim_y:
                    observation += 'EEE'
                for x in [ant.position-1:ant.position+2]:
                    if x < 0 or x >= self.dim_x:
                        observation += 'E'
                    else:
                        observation += world[x,y]
        observations += [observation,]


        return observations, rewards, done, valid

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

