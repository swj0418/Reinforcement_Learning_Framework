import numpy as np


class HystereticAgent:
    def __init__(self, environment, agent_id,
                 learning_rate=0.1, discount_factor=0.99, exploration_rate=0.01,
                 exploration_rate_decay=1,
                 increasing_learning_rate=0.1, decreasing_learning_rate=0.01):
        self.environment = environment
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_rate_decay = exploration_rate_decay
        self.agent_id = agent_id
        self.increasing_learning_rate = increasing_learning_rate
        self.decreasing_learning_rate = decreasing_learning_rate

        # Setup q_table
        self.num_of_action = self.environment.actions.n
        self.states_dim_x = self.environment.states.dim_x
        self.states_dim_y = self.environment.states.dim_y

        #self.q_table = np.zeros(shape=(self.states_dim_x * self.states_dim_y, self.num_of_action))

        # q_table is a dict of np arrays
        self.q_table = {}

        self.position_index = self.actual_to_index(self.environment.states.default_initial_position)

        self.rewards = []
        self.steps = 0
        self.total_rewards = 0
        self.done = False


    def step(self):
        if not self.done:
            # Determine action
            action = self.get_action()

            # Previous State capture (Previous q value, previous position)
            q_p = self.q_table[self.position_index][action]
            pos_p = self.position_index

            # Take action
            obs, reward, done, valid = self.environment.step(action=action, agent_id=self.agent_id)
            self.position_index = self.actual_to_index(obs[0])

            # Update Q-table
            bellman_value = reward + self.discount_factor * (np.max(self.q_table[self.position_index]) - q_p)

            if bellman_value >= 0:
                new_q = q_p + self.increasing_learning_rate * bellman_value
            else:
                new_q = q_p + self.decreasing_learning_rate * bellman_value

            self.q_table[pos_p][action] = new_q

            self.total_rewards += reward
            self.steps += 1

            self.rewards.append(self.total_rewards / self.steps)


    def q_learn(self, prev_observation, prev_action, current_observation, reward):

        if prev_observation not in self.q_table.keys():
            self.q_table[prev_observation] = np.array([0 for _ in range(self.num_of_action)], dtype=np.float64)

        if current_observation not in self.q_table.keys():
            self.q_table[current_observation] = np.array([0 for _ in range(self.num_of_action)], dtype=np.float64)

        q_p = self.q_table[prev_observation][prev_action]
        pos_p = prev_observation

        #print(prev_observation,current_observation,self.q_table[current_observation])

        # Update Q-table
        bellman_value = reward + self.discount_factor * (np.max(self.q_table[current_observation]) - q_p)

        if bellman_value >= 0:
            new_q = q_p + self.increasing_learning_rate * bellman_value
        else:
            new_q = q_p + self.decreasing_learning_rate * bellman_value

        self.q_table[prev_observation][prev_action] = new_q

        """
        if reward != 0:
            print(prev_observation, " ", prev_action, "   ", new_q, "   ", self.q_table[prev_observation])
        """

    def index_to_actual(self, index):
        x = index % self.states_dim_y
        y = index // self.states_dim_x

    def actual_to_index(self, actual):
        index = actual[0] * self.states_dim_x + actual[1]
        return index

    def get_action(self):
        if np.random.randint(0, 100) / 100 < self.exploration_rate:
            # Explore
            action = np.random.randint(0, self.num_of_action)
        else:
            action = np.argmax(self.q_table[self.position_index])

        return action

    def get_action_from_observation(self, observation):
        if observation not in self.q_table:
            self.q_table[observation] = np.array([0 for _ in range(self.num_of_action)], dtype=np.float64)
            return np.random.choice( range(self.num_of_action) )

        if np.random.randint(0, 100) / 100 < self.exploration_rate:
            # Explore
            action = np.random.randint(0, self.num_of_action)
        else:
            action = np.argmax(self.q_table[observation])
            # print("action: ", action, "  ", np.max(self.q_table[observation]))

        # Start to decay when an agent starts to learn?
        self.exploration_rate = self.exploration_rate * self.exploration_rate_decay

        return action


    def get_rewards(self):
        return self.rewards
