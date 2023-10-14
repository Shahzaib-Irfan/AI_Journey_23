import numpy as np


class BridgeMDP:
    def __init__(self, nc, nr):
        self.nc = nc
        self.nr = nr

    def states(self):
        return np.arange(1, self.nc * self.nr + 1)

    def get_block_no(self, s):
        return (s - 1) // self.nc + 1, (s - 1) % self.nc + 1

    def get_state_no(self, x, y):
        return (x - 1)*self.nc + y

    def actions(self, s):
        action = []
        x, y = self.get_block_no(s)
        if y - 1 >= 1:
            action.append('Left')
        if y + 1 <= self.nc:
            action.append('Right')
        if x - 1 >= 1:
            action.append('Up')
        if x <= self.nr:
            action.append('Down')

        return action

    def FailureStates(self):
        return [3, 7]

    def SuccessState(self):
        return [4]

    def isGoal(self, s):
        if s in self.FailureStates():
            return True
        if s in self.SuccessState():
            return True
        return False

    def reward(self, state, action, new_state):
        if new_state in self.states():
            if new_state in self.FailureStates():
                return -50
            elif self.isGoal(new_state):
                return 20
            elif new_state == 9:
                return 2

        return 0

    def get_foul_states_neighbors(self):
        foul_states = self.FailureStates()

        neighbors = []
        for i in foul_states:
            x, y = self.get_block_no(i)
            # up
            if y - 1 > 0:
                if self.get_state_no(x, y-1) not in self.FailureStates() and self.get_state_no(x, y-1) not in self.SuccessState():
                    neighbors.append(self.get_state_no(x, y-1))
            # down
            if y <= self.nc-1:
                if self.get_state_no(x, y+1) not in self.FailureStates() and self.get_state_no(x, y+1) not in self.SuccessState():
                    neighbors.append(self.get_state_no(x, y+1))
            # left
            if x - 1 > 0:
                if self.get_state_no(x - 1, y) not in self.FailureStates() and self.get_state_no(x - 1, y) not in self.SuccessState():
                    neighbors.append(self.get_state_no(x-1, y))
            # right
            if x <= self.nr-1:
                if self.get_state_no(x + 1, y) not in self.FailureStates() and self.get_state_no(x + 1, y) not in self.SuccessState():
                    neighbors.append(self.get_state_no(x+1, y))

        return neighbors

    def transition_probability(self, s, a, new_state):
        x, y = self.get_block_no(s)

        if a == "Left":
            y -= 1
        elif a == "Right":
            y += 1
        elif a == "Up":
            x -= 1
        elif a == "Down":
            x += 1

        s_calc = self.get_state_no(x, y)

        if s_calc == new_state:
            return 0.6
        elif new_state in self.FailureStates():
            return 0.4
        else:
            return 0.0


def policy_evaluation(mdp, gamma=1, theta=0.2):
    dict_states = {}

    for state in mdp.states():
        dict_states[state] = 0

    for i in range(100):
        delta = 0

        for state in mdp.states():
            current = 0

            for action in mdp.actions(state):
                for s_prime in mdp.states():
                    transition_prob = mdp.transition_probability(
                        state, action, s_prime)
                    reward = mdp.reward(state, action, s_prime)
                    current += transition_prob * \
                        (reward + gamma * dict_states[s_prime])

            delta = max(delta, abs(current - dict_states[state]))
            dict_states[state] = current

        if delta < theta:
            break

    return dict_states


def value_iteration(mdp, gamma=1, theta=0.2):
    dict_states = {}

    for state in mdp.states():
        dict_states[state] = 0

    for i in range(100):
        delta = 0

        for state in mdp.states():
            if mdp.isGoal(state):
                dict_states[state] = 0
            else:
                max_value = float("-inf")

                for action in mdp.actions(state):
                    current = 0

                    for s_prime in mdp.states():
                        transition_prob = mdp.transition_probability(
                            state, action, s_prime)
                        reward = mdp.reward(state, action, s_prime)
                        current += transition_prob * \
                            (reward + gamma * dict_states[s_prime])

                    if current > max_value:
                        max_value = current

                delta = max(delta, abs(max_value - dict_states[state]))
                dict_states[state] = max_value

        if delta < theta:
            break

    return dict_states


def implement_game():
    a = BridgeMDP(4, 3)
    print(a.get_block_no(8))
    value_dict = policy_evaluation(a)
    print("Policy Evaluation Result:")
    for a, n in value_dict.items():
        print(f'Total Evaluation Policy for {a} state: {n}')


implement_game()
