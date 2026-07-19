from collections import deque

from maze_utils import get_neighbors as _get_neighbors, start_goal


class BFS:
    """
    Breadth First Search Solver

    Returns:
    - shortest path from start to goal
    - explored nodes
    """

    def __init__(self, maze):

        self.maze = maze

        self.start, self.goal = start_goal(maze)

    # --------------------------------------------------
    # Get Valid Neighbours
    # --------------------------------------------------

    def get_neighbors(self, row, col):
        return _get_neighbors(self.maze, row, col)

    # --------------------------------------------------
    # Solve Maze
    # --------------------------------------------------

    def solve(self):

        queue = deque()

        queue.append(self.start)

        visited = set()
        visited.add(self.start)

        parent = {}

        explored = []

        while queue:

            current = queue.popleft()

            explored.append(current)

            if current == self.goal:
                break

            row, col = current

            for neighbor in self.get_neighbors(row, col):

                if neighbor not in visited:

                    visited.add(neighbor)

                    parent[neighbor] = current

                    queue.append(neighbor)

        # ----------------------------------------------
        # Reconstruct Path
        # ----------------------------------------------

        path = []

        if self.goal in parent or self.goal == self.start:

            current = self.goal

            while current != self.start:

                path.append(current)

                current = parent[current]

            path.append(self.start)

            path.reverse()

        return path, explored