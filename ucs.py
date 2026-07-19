import heapq

from maze_utils import get_neighbors as _get_neighbors, start_goal


class UCS:
    """
    Uniform Cost Search Maze Solver
    """

    def __init__(self, maze):

        self.maze = maze

        self.start, self.goal = start_goal(maze)

    # --------------------------------------------------

    def get_neighbors(self, row, col):
        return _get_neighbors(self.maze, row, col)

    # --------------------------------------------------

    def solve(self):

        priority_queue = []

        heapq.heappush(priority_queue, (0, self.start))

        cost = {
            self.start: 0
        }

        parent = {}

        explored = []

        visited = set()

        while priority_queue:

            current_cost, current = heapq.heappop(priority_queue)

            if current in visited:
                continue

            visited.add(current)

            explored.append(current)

            if current == self.goal:
                break

            for neighbor in self.get_neighbors(*current):

                new_cost = current_cost + 1

                if (
                    neighbor not in cost
                    or
                    new_cost < cost[neighbor]
                ):

                    cost[neighbor] = new_cost

                    parent[neighbor] = current

                    heapq.heappush(
                        priority_queue,
                        (new_cost, neighbor)
                    )

        # -------------------------
        # Reconstruct Path
        # -------------------------

        path = []

        node = self.goal

        while node != self.start:

            path.append(node)

            node = parent[node]

        path.append(self.start)

        path.reverse()

        return path, explored