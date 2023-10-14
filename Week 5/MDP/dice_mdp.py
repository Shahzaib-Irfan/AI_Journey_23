import math
import sys
import random


class DICEMDP:
    """
    This class is a blueprint and intuition for the Markov's Decision Problem.
    In future, we'll using this class to solve complex probelms. In this file we 
    are making a console game which includes dice. On dice roll, if it is not
    1 or 2, the player gets reward and the game continues else player gets 
    reward and game stops. If player chose to quit he/she will get 10 points as 
    reward and game stops
    """
    total_reward = 0

    def __init__(self, total_reward):
        self.total_reward = total_reward

    def Start(self):
        return 0

    def isGoal(self, s):
        """
        This function is checking if either the goal state has reached.
        If yes then returns true otherwise false

        args:
        s: state (current state)
        """
        return 'end' == s or 'quit' == s

    def states(self):
        return ['in', 'end']

    def actions(self, s):
        """
        This function allows user to make choice and reward will be on stake.

        args:
        s: state (current state)
        """
        print('Option an option: ')
        print('1. Stay')
        print('2. Quit')

        opt = input()
        return 'quit' if opt == 'quit' else 'stay'

    def reward(self, s, a, s_prime):
        """
        This function is calculating the reward of player's choice.

        args:
        s: state (current state)
        a: action (choice of player)
        s_prime: next state (result of player's choice)
        """
        if s == 'in' and a == 'stay' and (s_prime == 'in'):
            return 4
        elif s == 'in' and a == 'quit':
            return 10

        return 4

    def transition_prob(self, s, a, s_prime):
        """
        This function is calculating the probability of moving
        to next state through player's choice.


        args:
        s: state (current state)
        a: action (choice of player)
        s_prime: next state (result of player's choice)
        """
        if s == 'in' and a == 'stay' and s_prime == 'in':
            return 2/3
        elif s == 'in' and a == 'stay' and s_prime == 'end':
            return 1/3
        elif s == 'in' and a == 'quit' and s_prime == 'quit':
            return 1

    def transition(self, s, a):
        """
        This function is actually diciding the next move
        from player's choice.


        args:
        s: state (current state)
        a: action (choice of player)
        """
        if a == 'stay':
            num = random.randint(1, 6)
            return 'end' if num == 1 or num == 2 else 'in'
        return 'quit' if a == 'quit' else ''


def implement_game():
    a = DICEMDP(0)
    while True:
        action = a.actions('in')

        transition = a.transition('in', action)
        print("Transition: ", transition)

        print("Transition Probability: ",
              a.transition_prob('in', action, transition))

        a.total_reward += a.reward('in', action, transition)

        print("Total Reward: ", a.total_reward)
        if a.isGoal(transition):
            break


def policy_evaluation(mdp, echelon=0.2):
    prev = 0
    current = 0
    maximum = -1

    def implement_game(a, act):
        nonlocal prev, current, maximum
        while True:
            action = a.actions(act)

            transition = a.transition('in', action)
            print("Transition: ", transition)

            transition_prob = a.transition_prob('in', action, transition)

            print("Transition Probability: ", transition_prob)

            a.total_reward += a.reward('in', action, transition)
            print("Previous: ", prev)
            current += transition_prob * \
                (a.reward('in', action, transition) + prev)
            maximum = max(maximum, current - prev)
            prev = current
            print("Total Reward: ", a.total_reward)
            print("Maximum: ", maximum)
            print("Current: ", current)
            if a.isGoal(transition):
                return maximum

    dict = {}
    for a in mdp.states():
        dict[a] = 0
    for i in range(2):
        for a, n in dict.items():
            dict[a] = implement_game(mdp, a)
        if maximum <= echelon:
            print("dict: ", dict.items())
            print("Maximum: ", maximum)
            break


a = DICEMDP(0)
policy_evaluation(a)
# implement_game()
