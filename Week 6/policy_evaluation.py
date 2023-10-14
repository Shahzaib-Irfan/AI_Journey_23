# import math
# import sys
# import random


# class DICEMDP:
#     total_reward = 0

#     def __init__(self, total_reward):
#         self.total_reward = total_reward

#     def Start(self):
#         return 0

#     def isGoal(self, s):
#         return 'end' == s or 'quit' == s

#     def states(self):
#         return ['in', 'end']

#     def get_policy(self, s):
#         """
#         Define your policy here. You can use any logic you want to determine the action.
#         For example, you can use a random policy, a fixed policy, or implement a policy evaluation algorithm.
#         """
#         # Example: Random policy
#         if s == 'in':
#             return random.choice([0, 1])  # 0 for 'stay', 1 for 'quit'
#         return 1  # Always choose 'quit' when not in 'in' state

#     def reward(self, s, a, s_prime):
#         if s == 'in' and a == 0 and (s_prime == 'in'):
#             return 4
#         elif s == 'in' and a == 1:
#             return 10
#         return 4

#     def transition_prob(self, s, a, s_prime):
#         if s == 'in' and a == 0:
#             if s_prime == 'in':
#                 return 2/3
#             elif s_prime == 'end':
#                 return 1/3
#         elif s == 'in' and a == 1 and s_prime == 'quit':
#             return 1
#         # Return 0 for all other cases
#         return 0

#     def transition(self, s, a):
#         if a == 0:  # 0 represents 'stay'
#             num = random.randint(1, 6)
#             return 'end' if num == 1 or num == 2 else 'in'
#         return 'quit' if a == 1 else ''  # 1 represents 'quit'
import math
import sys
import random


class DICEMDP:
    total_reward = 0

    def __init__(self, total_reward):
        self.total_reward = total_reward

    def Start(self):
        return 0

    def isGoal(self, s):
        return 'end' == s or 'quit' == s

    def states(self):
        return ['in', 'end']

    def actions(self, s):
        return ['stay', 'quit']

    def reward(self, s, a, s_prime):
        if s == 'in' and a == 'stay' and (s_prime == 'in'):
            return 4
        elif s == 'in' and a == 'quit':
            return 10
        return 4

    def transition_prob(self, s, a, s_prime):
        if s == 'in':
            if a == 'stay':
                if s_prime == 'in':
                    return 2/3
                elif s_prime == 'end':
                    return 1/3
            elif a == 'quit' and s_prime == 'quit':
                return 1
        return 0

    def transition(self, s, a):
        if a == 'stay':
            num = random.randint(1, 6)
            return 'end' if num == 1 or num == 2 else 'in'
        return s


def policy_evaluation(mdp, gamma=1.0, theta=0.2):
    dict = {}
    for state in mdp.states():
        dict[state] = 0

    for i in range(100):
        delta = 0
        #action = 'stay'
        for state in mdp.states():
            current = 0
            for action in mdp.actions(state):
                for s_prime in mdp.states():
                    current += mdp.transition_prob(state, action, s_prime) * \
                        (mdp.reward(state, action, s_prime) + dict[s_prime])

                    delta = max(delta, abs(current - dict[s_prime]))

                    dict[state] = current
        if delta < theta:
            break

    return dict


def implement_game():
    a = DICEMDP(0)
    value_dict = policy_evaluation(a)
    print("Policy Evaluation Result:")
    for a, n in value_dict.items():
        print(f'Total Evaluation Policy for {a} state: {n}')


if __name__ == "__main__":
    implement_game()
