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
    def __init__(self,my_id,position):
        self.position = position
        self.id = my_id
        self.carrying = False

class Pheromone:
    def __init__(self,position):
        self.position = position
        self.age = 0

class Antworld:
    def __init__(self,dim_x=10, dim_y=10, agents_n=2, food=(3,3), max_pheromone_age=30):
        self.actions = Action()
        self.states = States(dim_x=dim_x, dim_y=dim_y, agents_n=agents_n)
        self.agents_n = agents_n
        self.observation = Observation()
        self.reward = {}
        self.max_pheromone_age = max_pheromone_age

        self.dim_x = dim_x
        self.dim_y = dim_y

        self.home_position = (dim_x//2,dim_y//2)
        self.food_position = food
        self.ants = [Ant(x,self.home_position) for x in range(agents_n)]
        self.pheromones = []

        #right now agents are tuples: x, y, id, carrying

    def display(self):
        worldDisplay = [['.' for x in range(self.dim_x)] for y in range(self.dim_y)]
        worldDisplay = np.array(worldDisplay)

        for a in self.ants:
            if a.position[0] >= 0 and a.position[0] < self.dim_x and a.position[1] >= 0 and a.position[1] < self.dim_y:
                if a.carrying:
                    worldDisplay[a.position[0], a.position[1]] = 'c'
                else:
                    worldDisplay[a.position[0], a.position[1]] = 'a'

        for a in self.pheromones:
            if a.position[0] >= 0 and a.position[0] < self.dim_x and a.position[1] >= 0 and a.position[1] < self.dim_y:
                worldDisplay[a.position[0],a.position[1]] = 'p'

        worldDisplay[self.home_position] = 'H'
        worldDisplay[self.food_position] = 'F'
        out = ''
        for y in range(self.dim_y):
            for x in range(self.dim_x):
                out += str(worldDisplay[x,y])
            out += '\n'
        print(out)

    def pheromone_output(self):
        phero = np.zeros((self.dim_x,self.dim_y))
        anty = np.zeros((self.dim_x,self.dim_y))
        for a in self.pheromones:
            if a.position[0] >= 0 and a.position[0] < self.dim_x and a.position[1] >= 0 and a.position[1] < self.dim_y:
                phero[a.position[0], a.position[1]] = 1

        for a in self.ants:
            if a.position[0] >= 0 and a.position[0] < self.dim_x and a.position[1] >= 0 and a.position[1] < self.dim_y:
                anty[a.position[0], a.position[1]] = 1

        return phero, anty

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
        if len(actions) > 0:
            for num in agent_ids:
                action = actions[num]
                agent = self.ants[num]
                prevpos = agent.position
                agent.position = tuple(map(sum,zip(self.actions.values[action],agent.position)))
                if agent.position[0] < 0 or agent.position[0] >= self.dim_x:
                    agent.position = prevpos
                if agent.position[1] < 0 or agent.position[1] >= self.dim_y:
                    agent.position = prevpos
                if action == 4:
                    self.pheromones += [Pheromone(agent.position)]
                if agent.carrying and agent.position == self.home_position:
                    agent.carrying = False
                    joint_reward += 10
                    rewards[num] += 10 #give the bringer the best reward
                elif agent.position == self.food_position:
                    agent.carrying = True

                # Movement penalty
                rewards[num] -= 1

            rewards = np.array(rewards) + joint_reward



        # generate observations

        observations = []

        world = [['.' for _ in range(self.dim_x)] for _ in range(self.dim_y)]
        world = np.array(world)

        for a in self.ants:
            if a.position[0] >= 0 and a.position[0] < self.dim_x and a.position[1] >= 0 and a.position[1] < self.dim_y:
                world[a.position[0], a.position[1]] = 'a'
        for a in self.pheromones:
            if a.position[0] >= 0 and a.position[0] < self.dim_x and a.position[1] >= 0 and a.position[1] < self.dim_y:
                world[a.position[0], a.position[1]] = 'p'
            else:
                a.age = 301

        world[self.home_position] = 'H'
        world[self.food_position] = 'F'

        for ant in self.ants:
            observation = ''
            for y in range(ant.position[1] - 1, ant.position[1] + 2):
                if y < 0 or y >= self.dim_y:
                    observation += '...'
                else:
                    for x in range(ant.position[0]-1,ant.position[0]+2):
                        if x < 0 or x >= self.dim_x:
                            observation += '.'
                        else:
                            if world[x, y] != 'a':
                                observation += world[x, y]
                            elif (x, y) != ant.position:
                                observation += '.'
                            elif ant.carrying and (x, y) == ant.position:
                                observation += 'c'
                            
            observations += [observation, ]

        return observations, rewards, done, valid

    def reset(self, food=(3, 3)):
        self.ants = [Ant(x, self.home_position) for x in range(self.agents_n)]
        self.pheromones = []

        self.food_position = food

        return True
