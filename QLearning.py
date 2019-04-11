import numpy as np


class QLearning:
    epsilon = 0.1

    def __init__(self, state_dim, action_space=None, state_space=None):
        """
        A state space that is 2-dimensional
        A state space that is 1-dimensional
        Has to be treated differently. For generic input, determination has to be done at some point.
        Passing on dimension of the state space as a parameter can solve this problem
        :param action_space:
        :param state_space:
        :param state_dim: tuple. (1, n) indicates 1-dimension, (n, n) indicates 2.
        """

        if state_dim[0] == 1:
            # 1 Dimension
            self.action_space, self.state_space = self.create_1d_state_action_space(state_dim[1])

        elif state_dim[0] != 1:
            # 2 Dimension
            self.action_space, self.state_space = self.create_2d_state_action_space(state_dim[0], state_dim[1])

        elif action_space is not None and state_space is not None:
            self.action_space = action_space
            self.state_space = state_space

        self.x_dim_size = state_dim[1]
        self.y_dim_size = state_dim[0]
        self.num_of_actions = len(self.action_space)
        self.num_of_states = len(self.state_space)

        self.q_table = np.zeros(shape=(self.num_of_states, self.num_of_actions))

        self.current_pos = (0, 0) # Current position should be determined

    def run_step(self, epsilon, observation=None, rewards=None):
        # Maximum Q value or new random action found. Take that action
        new_action = self.take_action(epsilon)

        # Calculate Bellmen


        # Update Q-Table

    def take_action(self, epsilon):
        new_action = None
        if self.determine_exploration(epsilon):
            # Explore
            while True:
                action_idx = np.random.randint(0, self.num_of_actions)
                if self.action_out_of_bound(self.action_space[action_idx], self.current_pos):
                    continue
                else:
                    # Legitimate Action
                    new_action = self.action_space[action_idx]
                    break

        else:
            # Exploit
            # Choose action based on Q-table
            # See all action space
            new_action = None
            max_q_index = 0
            max_q_value = 0  # Initial Q value
            counter = 0
            for Q in self.q_table[self.convert_pos_to_q_idx(self.current_pos)]:
                for possible_action in self.action_space:
                    # Check bound condition
                    if self.action_out_of_bound(possible_action, self.current_pos) is False:
                        if Q >= max_q_value:
                            max_q_value = Q
                            max_q_index = counter
                            new_action = possible_action

                    counter += 1

        return new_action


    def determine_exploration(self, epsilon):
        random = np.random.randint(0, 100) / 100
        if random > epsilon:
            return False
        else:
            return True

    def convert_pos_to_q_idx(self, pos):
        index = pos[0] * self.y_dim_size + pos[1]
        return index

    def action_out_of_bound(self, action, current_pos):
        """
        Bound function is a function of a dimension of a state space and a new action to be taken
        :param action: Tuple
        :return:
        """
        if current_pos[0] + action[0] >= 0 and current_pos[1] + action[1] >= 0 and current_pos[0] + action[0] < self.x_dim_size and current_pos[1] + action[1] < self.y_dim_size:
            # print("OUTOFBOUND", current_pos, action)
            return False
        else:
            return True

    def create_1d_state_action_space(self, x_dim):
        """
        A state space for 1-dimensional domain and 1-dimensional domain can be constructed in a singular fashion,
        but an action space has to be constrained for each of the space.

        For example, in a 2-dimensional state space, if we restrict a movement of an agent by 1 adjacent unit per
        iteration, action space

        :return: State Space and Action Space, also a movement restriction rule function.
        """

        state_space = np.zeros(shape=(1, x_dim))
        action_space = [(-1, 0), (0, 0), (1, 0)]

        return action_space, state_space

    def create_2d_state_action_space(self, x_dim, y_dim):
        state_space = np.zeros(shape=(y_dim, x_dim))
        action_space = [(0, -1), (1, 0), (0, 1), (-1, 0)] # Clockwise starting from North

        return action_space, state_space


if __name__ ==  "__main__":
    qlearning = QLearning((5, 5))
    for i in range(100):
        qlearning.run_step(0.1)
