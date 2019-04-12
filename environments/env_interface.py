import os
import sys

class ReinforcementLearningEnvironment:
    def __init__(self):
        pass

    def step(self, action, agent_id):
        """
                Take an action given by the policy and give evaluative feedback.

                agent_id is a requirement for multi-agent system.

                If an action is not a valid action, i.e., out of bound,
                step function will directly return False for val.

                :param action: An index of an action space.
                :return:
                        observation:
                        reward:
                        done:
                        val: checking whether an action proposed by an agent is a valid action or not.
        """
        pass

    def reset(self):
        pass
