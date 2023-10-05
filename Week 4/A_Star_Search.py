class Node:
    """
    Represents a node in the puzzle.

    Attributes:
        state: The current state of the puzzle.
        parent: The parent node from which this node was generated.
        g: The cost of reaching this node from the initial state.
        h: The heuristic cost estimate from this node to the goal state.
        f: The total cost of the node (f = g + h).
    """

    def __init__(self, state, parent=None):
        """Initialize a new node."""
        self.state = state
        self.parent = parent
        self.g = 0 if parent is None else parent.g + 1
        self.h = 0
        self.f = 0

    def move(self, dx, dy):
        """
        Move the empty tile in the puzzle by dx and dy.

        Args:
            dx: The change in the x-coordinate.
            dy: The change in the y-coordinate.

        Returns:
            A new Node representing the puzzle state after the move, or None if the move is invalid.
        """
        empty_index = self.state.index(0)
        x, y = empty_index % 3, empty_index // 3
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = self.state[:]
            new_state[y * 3 + x], new_state[ny * 3 +
                                            nx] = new_state[ny * 3 + nx], new_state[y * 3 + x]
            return Node(new_state, self)
        return None

    def get_children(self):
        """Generate child nodes by moving the empty tile in all possible directions."""
        return filter(None, [self.move(0, -1), self.move(0, 1), self.move(-1, 0), self.move(1, 0)])


class Puzzle:
    """
    Represents a sliding puzzle and provides methods to solve it.

    Attributes:
        initial_state: The initial state of the puzzle as a Node.
        goal_state: The goal state of the puzzle.

    Methods:
        h(node): Calculate the heuristic cost from a given node to the goal state.
        solve(): Solve the puzzle using the A* search algorithm.
        print_state(state): Print the current state of the puzzle.
    """

    def __init__(self, initial_state, goal_state):
        """Initialize a new puzzle with an initial state and a goal state."""
        self.initial_state = Node(initial_state)
        self.goal_state = goal_state

    def h(self, node):
        """
        Calculate the heuristic cost from a given node to the goal state.

        Args:
            node: The node for which to calculate the heuristic cost.

        Returns:
            The heuristic cost estimate.
        """
        return sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
                   for b, g in ((node.state.index(i), self.goal_state.index(i)) for i in range(1, 9)))

    def solve(self):
        """Solve the puzzle using the A* search algorithm."""
        open_list = [self.initial_state]
        closed_set = set()
        i = 0
        while open_list:
            print("Iteration: ", i)
            node = min(open_list, key=lambda node: node.f)
            if node.state == self.goal_state:
                path = []
                while node:
                    path.append(node.state)
                    node = node.parent
                path.reverse()
                for state in path:
                    self.print_state(state)
                break
            open_list.remove(node)
            closed_set.add(node)
            for child in node.get_children():
                if child in closed_set:
                    continue
                child.h = self.h(child)
                child.f = child.g + child.h
                if not any(child.state == n.state and child.g >= n.g for n in open_list):
                    open_list.append(child)
            i += 1

    def print_state(self, state):
        """Print the current state of the puzzle."""
        for i in range(3):
            for j in range(3):
                print(state[i * 3 + j], end=' ')
            print()
        print()


initial_state = [1, 2, 3,
                 4, 0, 6,
                 5, 8, 7]
goal_state = [1, 2, 3,
              4, 5, 6,
              7, 8, 0]

puzzle = Puzzle(initial_state, goal_state)
puzzle.solve()
