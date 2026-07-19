from heapq import heappush, heappop

from maze_utils import get_neighbors as _get_neighbors, start_goal, heuristic as _heuristic


class AStar:

    def __init__(self, maze):

        self.maze = maze
        self.start, self.goal = start_goal(maze)

    # -------------------------------------------------

    def heuristic(self, node):
        # Manhattan-style distance (exact on the square grid)
        return _heuristic(node, self.goal)

    # -------------------------------------------------

    def get_neighbors(self, row, col):
        return _get_neighbors(self.maze, row, col)

    # -------------------------------------------------

    def solve(self):

        start = self.start
        goal = self.goal

        frontier = []

        # (f = g+h, g, node)
        heappush(frontier, (self.heuristic(start), 0, start))

        parent = {}

        g_cost = {start: 0}

        explored = []

        while frontier:

            f, cost, current = heappop(frontier)

            if current in explored:
                continue

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

                new_cost = cost + 1

                if neighbor not in g_cost or new_cost < g_cost[neighbor]:

                    g_cost[neighbor] = new_cost

                    priority = new_cost + self.heuristic(neighbor)

                    heappush(
                        frontier,
                        (priority, new_cost, neighbor)
                    )

                    parent[neighbor] = current

        return [], explored