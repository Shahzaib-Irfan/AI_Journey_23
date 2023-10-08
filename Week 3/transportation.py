import math
import sys


class Transportation:
    N = 0

    def __init__(self, N):
        self.N = N

    def Start(self):
        return 1

    def isGoal(self, s):
        return self.N == s

    def actions(self, s):
        actions = []
        if s + 1 <= self.N:
            actions.append('walk')
        if s * 2 <= self.N:
            actions.append('tram')

        return actions

    def cost(self, a):
        if a == 'walk':
            return 1
        elif a == 'tram':
            return 2

        return 0

    def transition(self, s, a):
        if a == 'walk':
            return s + 1
        elif a == 'tram':
            return s * 2

        return s


def BackTrackingSearch(problem):

    history = []
    min_cost = float('inf')

    def recurse(state, cost, historyObject):
        nonlocal min_cost, history
        if problem.isGoal(state):
            if cost < min_cost:
                min_cost = cost
                history = historyObject
                return
        else:
            actions = problem.actions(state)
            for act in actions:
                new_state = problem.transition(state, act)
                new_cost = problem.cost(act)

                recurse(new_state, cost + new_cost,
                        historyObject + [(state, act, new_state)])

    recurse(problem.Start(), 0, [])
    return min_cost, history


def BackTrackingSearch_Dynamic(problem):

    history = []
    min_cost = float('inf')
    cache = [float('inf') for x in range(problem.N + 1)]

    def recurse(state, cost, historyObject):
        sys.setrecursionlimit(200000)
        nonlocal min_cost, history, cache

        if cache[state] < cost:
            return

        cache[state] = cost
        if problem.isGoal(state):
            if cost < min_cost:
                min_cost = cost
                history = historyObject
                return
        else:
            actions = problem.actions(state)
            for act in actions:
                new_state = problem.transition(state, act)
                new_cost = problem.cost(act)

                recurse(new_state, cost + new_cost,
                        historyObject + [(state, act, new_state)])

    recurse(problem.Start(), 0, [])
    return min_cost, history


def DFS_Recursive(problem):

    history = []
    min_cost = float('inf')
    isGoal_Reached = False

    def recurse(state, cost, historyObject):
        sys.setrecursionlimit(200000)
        nonlocal min_cost, history, isGoal_Reached
        if problem.isGoal(state):
            if cost < min_cost:
                min_cost = cost
                history = historyObject
                isGoal_Reached = True
                return
        else:
            if isGoal_Reached == False:
                actions = problem.actions(state)
                for act in actions:
                    new_state = problem.transition(state, act)
                    new_cost = problem.cost(act)

                    recurse(new_state, cost + new_cost,
                            historyObject + [(state, act, new_state)])

    recurse(problem.Start(), 0, [])
    return min_cost, history


def BFS(problem):
    frontier = []
    frontier.append((problem.Start(), 0, []))

    reached = set()

    while frontier:
        node = frontier.pop(0)
        state, cost, history = node

        if problem.isGoal(state):
            return cost, history

        if state not in reached:
            reached.add(state)

        for act in problem.actions(state):
            new_state = problem.transition(state, act)
            new_cost = cost + problem.cost(act)

            frontier.append((new_state, new_cost, history +
                            [(state, act, new_state)]))

    return 0, []


def iterative_deepning_search(problem):

    depth = 0

    while True:
        result, history = depth_limited_search(problem, depth)

        if result != 'cut-off':
            return result, history
        depth += 1


def depth_limited_search(problem, depth):
    frontier = []
    frontier.append((problem.Start(), 0, []))

    reached = set()

    result = ''
    while frontier:
        node = frontier.pop()
        state, cost, history = node

        if problem.isGoal(state):
            return (cost, history)

        if cost > depth:
            result = 'cut-off'

        if state not in reached:
            reached.add(state)

        for act in problem.actions(state):
            new_state = problem.transition(state, act)
            new_cost = cost + problem.cost(act)

            frontier.append((new_state, new_cost, history +
                            [(state, act, new_state)]))

    return result, []


if __name__ == '__main__':

    problem = Transportation(6)
    print(iterative_deepning_search(problem))
