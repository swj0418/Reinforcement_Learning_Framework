import numpy as np

class Agent:
    def __init__(self):
        self.q_table = np.zeros(shape=(3, ))
        self.rewards = []
        self.averaged_rewards = []
        self.total_rewards = 0

        self.action_cursor = 1

class HystereticAgentMatrix:
    def __init__(self, environment, increasing_learning_rate=0.9, decreasing_learning_rate=0.1,
                 discount_factor=0.9, exploration_rate=0.01):
        self.environment = environment
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.increasing_learning_rate = increasing_learning_rate
        self.decreasing_learning_rate = decreasing_learning_rate

        # Setup q_table
        self.num_of_action = self.environment.actions.n
        self.states_dim_x = self.environment.states.dim_x
        self.states_dim_y = self.environment.states.dim_y

        # Agents
        self.num_of_agents = 2
        self.agents = []
        for i in range(self.num_of_agents):
            self.agents.append(Agent())
        self.steps = 1

    def step(self):
        actions = []
        for agent in self.agents:
            # Determine Actions
            action = self.get_action(agent)
            actions.append(action)

        # Take action and update
        for agent in self.agents:
            # Previous State capture (Previous q value, previous position)
            q_p = agent.q_table[agent.action_cursor]
            # Take action
            obs, reward, done, valid = self.environment.step(action=actions, agent_id=0)

            # Update Q-table
            bellman_value = reward + self.discount_factor * (np.max(agent.q_table[agent.action_cursor]) - q_p)

            if bellman_value >= 0:
                new_q = q_p + self.increasing_learning_rate * bellman_value
            else:
                new_q = q_p + self.decreasing_learning_rate * bellman_value

            agent.q_table[agent.action_cursor] = new_q
            # self.exploration_rate = self.exploration_rate / self.steps

            agent.total_rewards += reward
            agent.rewards.append(reward)

            if self.steps > 1:
                agent.averaged_rewards.append(agent.total_rewards / (self.steps + 5))

        self.steps += 1



    def get_action(self, agent):
        if np.random.randint(0, 100) / 100 < self.exploration_rate:
            # Explore
            action = np.random.randint(0, self.num_of_action)
        else:
            action = np.argmax(agent.q_table)

        agent.action_cursor = action

        return action

    def get_averaged_rewards(self, agent_id=0):
        return self.agents[agent_id].averaged_rewards, self.agents[agent_id + 1].averaged_rewards

    def get_rewards(self):
        return self.agents[0].rewards, self.agents[1].rewards
