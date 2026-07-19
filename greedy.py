from heapq import heappush, heappop

from maze_utils import get_neighbors as _get_neighbors, start_goal, heuristic as _heuristic


class Greedy:

    def __init__(self, maze):

        self.maze = maze
        self.start, self.goal = start_goal(maze)

    # -------------------------------------------------

    def heuristic(self, node):
        return _heuristic(node, self.goal)

    # -------------------------------------------------

    def get_neighbors(self, row, col):
        return _get_neighbors(self.maze, row, col)

    # -------------------------------------------------

    def solve(self):

        start = self.start
        goal = self.goal

        frontier = []
        heappush(frontier, (self.heuristic(start), start))

        parent = {}
        visited = {start}

        explored = []

        while frontier:

            _, current = heappop(frontier)

            explored.append(current)

            if current == goal:

                path = []

                while current != start:
                    path.append(current)
                    current = parent[current]

                path.append(start)
                path.reverse()

                return path, explored

            row, col = current

            for neighbor in self.get_neighbors(row, col):

                if neighbor not in visited:

                    visited.add(neighbor)
                    parent[neighbor] = current

                    heappush(
                        frontier,
                        (self.heuristic(neighbor), neighbor)
                    )

        return [], explored