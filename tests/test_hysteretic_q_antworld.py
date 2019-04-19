'''
testing hysteretic_q learning on the climbing game.
'''

from matplotlib import pyplot as plt

from environments.env_antworld import Antworld

from learning_algorithms.hysteretic_q import HystereticAgent

if __name__ == '__main__':
    env = None
    epochs = 1000
    simulations = 1
    epoch_length = 10000
    num_agents = 2
    rewards_1 = []
    individual_run_rewards = []
    averaged_rewards = []

    for simulation in range(simulations):
        food_position = (7, 8)
        env = Antworld(dim_x=10, dim_y=10, agents_n=num_agents, food=food_position)
        agents = [HystereticAgent(env, this_id, exploration_rate=0.01, exploration_rate_decay=0.999999) for this_id in range(num_agents)]

        # get initial observations/rewards
        observations, rewards, _, _ = env.step([],[x for x in range(num_agents)])
        total_sum_rewards = 0
        for epoch in range(epochs):
            env.reset(food=food_position)

            sum_rewards = 0
            for time in range(epoch_length):
                actions = []
                for agent_num in range(num_agents):
                    actions += [agents[agent_num].get_action_from_observation(observations[agent_num])]

                prev_observations = observations
                observations, rewards, _, _, = env.step(actions,[x for x in range(num_agents)])

                if epoch > epochs - 2:
                    env.display()

                sum_rewards += sum(rewards)
                for agent_num in range(num_agents):
                    agents[agent_num].q_learn(prev_observations[agent_num],
                                              actions[agent_num],
                                              observations[agent_num],
                                              rewards[agent_num])


            print("Epoch: ", epoch, "   Accumulative Rewards: ", sum_rewards, " Averaged Rewards: ", sum_rewards / epoch_length,
                  "     ", (total_sum_rewards / epoch_length) / (epoch + 1), " Exploration Rate: ", agents[0].exploration_rate)
            # print(len(agents[0].q_table.keys()))
            # print(agents[0].exploration_rate)

            rewards_1 += [sum_rewards,]
            total_sum_rewards += sum_rewards
            individual_run_rewards.append(sum_rewards / epoch_length)
            averaged_rewards.append((total_sum_rewards / epoch_length) / (epoch + 1))

    plt.plot(averaged_rewards)
    plt.show()
