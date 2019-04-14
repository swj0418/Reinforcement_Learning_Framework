import numpy as np


class HystereticAgentMatrix:
    def __init__(self, environment, agent_id,
                 learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1,
                 increasing_learning_rate=0.1, decreasing_learning_rate=0.01):
        self.environment = environment
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.agent_id = agent_id
        self.increasing_learning_rate = increasing_learning_rate
        self.decreasing_learning_rate = decreasing_learning_rate

        # Setup q_table
        self.num_of_action = self.environment.actions.n
        self.states_dim_x = self.environment.states.dim_x
        self.states_dim_y = self.environment.states.dim_y

        self.q_table = np.zeros(shape=(self.states_dim_x * self.states_dim_y, self.num_of_action))

        self.rewards = []
        self.steps = 0
        self.total_rewards = 0
        self.done = False

    def step(self):
        if not self.done:
            # Determine action
            action = self.get_action()

            # Previous State capture (Previous q value, previous position)
            q_p = self.q_table[action][0]

            action = [0, 1]

            # Take action
            obs, reward, done, valid = self.environment.step(action=action, agent_id=self.agent_id)

            # Update Q-table
            bellman_value = reward + self.discount_factor * (np.max(self.q_table[action]) - q_p)

            if bellman_value >= 0:
                new_q = q_p + self.increasing_learning_rate * bellman_value
            else:
                new_q = q_p + self.decreasing_learning_rate * bellman_value

            self.q_table[action][0] = new_q

            self.total_rewards += reward
            self.steps += 1

            self.rewards.append(self.total_rewards / self.steps)

    def get_action(self):
        if np.random.randint(0, 100) / 100 < self.exploration_rate:
            # Explore
            action = np.random.randint(0, self.num_of_action)
        else:
            action = np.argmax(self.q_table)

        return action

    def get_rewards(self):
        return self.rewards
