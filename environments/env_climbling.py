import numpy as np

from environments.env_interface import ReinforcementLearningEnvironment


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
    def __init__(self, dim_x=3, dim_y=3, agents_n=2):
        self.n = dim_x * dim_y
        self.agents_n = agents_n
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.default_initial_position = (2, 0)
        self.current_position = {}

        # World Dict maintains collection of worlds with respect to individual agents
        self.world = {}

        for i in range(agents_n):
            world = np.zeros(shape=(dim_y, dim_x))
            world[2][0] = 1 # Agent being in a position denoted by 1

            # Initial Position
            # All agents can start from initial position, (2, 0)
            self.current_position[i] = self.default_initial_position

            self.world[i] = world


    def is_collision(self, action, agent_id):
        """
        Checks if there are any other agents in a tile.
        If more than two agents' world completely overlaps, it means that agents have collided. Return True
        else Return False.
        Also checks bound condition as well

        Given an action, try the action. If legitimate, change state.
        :return: collision
        """
        trial = self.world[agent_id]
        # Not a tuple
        position = np.argmax(trial)

        x = position % self.dim_y
        y = position // self.dim_x
        # Previous position
        position = (y, x)

        new_y = position[0] + action[0]
        new_x = position[1] + action[1]

        # Check bound
        if new_y < 0 or new_x < 0 \
                or new_y > self.dim_x - 1 or new_x > self.dim_y - 1:
            # print("OUTOFBOUND")
            self.current_position[agent_id] = (y, x)
            return True

        # Update trial. This move does not go out of bound.
        trial[y][x] = 0
        trial[new_y][new_x] = 1

        for key in self.world.keys():
            if key is not agent_id:
                if np.array_equal(trial, self.world[agent_id]):
                    return True

        # Remove last position
        self.world[agent_id][y][x] = 0
        # Update new postion
        self.world[agent_id][new_y][new_x] = 1
        self.current_position[agent_id] = (new_y, new_x)

        return False


class Climbing(ReinforcementLearningEnvironment):
    def __init__(self):
        ReinforcementLearningEnvironment.__init__(self)
        self.actions = Action()
        self.states = States(dim_x=3, dim_y=3, agents_n=2)
        self.observation = Observation()

        self.reward = {}

        # Sets up a reward function
        self.__generate_reward_function()

    def step(self, action, agent_id=0):
        """
        Take an action given by the policy and give evaluative feedback.

        agent_id is a requirement for multi-agent system.

        If an action is not a valid action, i.e., out of bound, step function will directly return False for val.

        :param action: An index of an action space.
        :param agent_id: Requirement for MAS. Default is zero in case of a single agent game.
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
        if self.is_legitimate_move(action=concrete_action, agent_id=agent_id):
            # Move
            agent_position = self.states.current_position[agent_id]
            observation = [agent_position] # Current Position

            reward = self.reward[agent_position[0]][agent_position[1]]
            reward = reward - 1

            val = True
        else:
            # Inform that the move hasn't been made
            agent_position = self.states.current_position[agent_id]
            observation = [agent_position]

            reward = -1

            val = False

        # Moving agent has already been done

        # Check if the game is complete
        # There is no completion

        return observation, reward, done, val


    def reset(self):

        return True

    def is_legitimate_move(self, action, agent_id):
        """
        Checks whether an action is out_of_bound.
                                    Collision.
        :param action:
        :return:
        """
        # Collision check returns true if it isn't a legitimate move or out of bound
        # Self updates a state function
        collision = self.states.is_collision(action, agent_id)

        return not collision


    def __generate_reward_function(self):
        """
        Reward function must have a randomness in it for 2, 2 position
        50% of 0 and 50% of 14 (Paritially Stochastic Games)
        :return:
        """
        self.reward = np.array([[11, -30, 0],
                                [-30, 14, 6],
                                [0,   0,  5]])
