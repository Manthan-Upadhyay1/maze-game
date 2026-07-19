from collections import deque

from maze_utils import get_neighbors as _get_neighbors, start_goal


class DFS:
    """
    Depth First Search Maze Solver
    """

    def __init__(self, maze):

        self.maze = maze
        self.start, self.goal = start_goal(maze)

    # --------------------------------------------------

    def get_neighbors(self, row, col):
        return _get_neighbors(self.maze, row, col)

    # --------------------------------------------------

    def solve(self):

        stack = [self.start]

        visited = set()

        parent = {}

        explored = []

        while stack:

            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            explored.append(current)

            if current == self.goal:
                break

            for neighbor in reversed(self.get_neighbors(*current)):

                if neighbor not in visited:

                    stack.append(neighbor)

                    if neighbor not in parent:
                        parent[neighbor] = current

        path = []

        node = self.goal

        while node != self.start:

            path.append(node)

            node = parent[node]

        path.append(self.start)

        path.reverse()

        return path, explored