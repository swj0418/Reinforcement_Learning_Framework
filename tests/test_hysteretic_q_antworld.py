'''
testing hysteretic_q learning on the climbing game.
'''

from matplotlib import pyplot as plt

from environments.env_antworld import Antworld

from learning_algorithms.hysteretic_q import HystereticAgent



if __name__ == '__main__':
    env = Antworld()
    epochs = 1000
    simulations = 1
    epoch_length = 1000
    num_agents = 3
    rewards_1 = []

    for simulation in range(simulations):

        env = Antworld(agents_n=num_agents)
        agents = [HystereticAgent(env,this_id) for this_id in range(num_agents)]

        # get initial observations/rewards
        observations, rewards, _, _ = env.step([],[x for x in range(num_agents)])
        #print(observations)

        for epoch in range(epochs):
            env.reset()

            sum_rewards = 0
            for time in range(epoch_length):
                actions = []
                for agent_num in range(num_agents):
                    actions += [agents[agent_num].get_action_from_observation(observations[agent_num]),]

                prev_observations = observations
                observations, rewards, _, _, = env.step(actions,[x for x in range(num_agents)])
                
                sum_rewards += sum(rewards)
                for agent_num in range(num_agents):
                    agents[agent_num].q_learn(prev_observations[agent_num],actions[agent_num],observations[agent_num],rewards[agent_num])


            env.display()
            print(sum_rewards)
            rewards_1 += [sum_rewards,]
                

    plt.plot(rewards_1)
    plt.show()