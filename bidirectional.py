from collections import deque

from maze_utils import get_neighbors as _get_neighbors, start_goal


class BidirectionalSearch:

    def __init__(self, maze):

        self.maze = maze
        self.start, self.goal = start_goal(maze)

    # -------------------------------------------------

    def get_neighbors(self, row, col):
        return _get_neighbors(self.maze, row, col)

    # -------------------------------------------------

    def build_path(self, meet, parent_start, parent_goal):

        path1 = []

        node = meet

        while node is not None:
            path1.append(node)
            node = parent_start[node]

        path1.reverse()

        path2 = []

        node = parent_goal[meet]

        while node is not None:
            path2.append(node)
            node = parent_goal[node]

        return path1 + path2

    # -------------------------------------------------

    def solve(self):

        start = self.start
        goal = self.goal

        if start == goal:
            return [start], [start]

        queue_start = deque([start])
        queue_goal = deque([goal])

        visited_start = {start}
        visited_goal = {goal}

        parent_start = {start: None}
        parent_goal = {goal: None}

        explored = []

        while queue_start and queue_goal:

            # -----------------------------
            # Expand from Start
            # -----------------------------

            current = queue_start.popleft()
            explored.append(current)

            for neighbor in self.get_neighbors(*current):

                if neighbor not in visited_start:

                    visited_start.add(neighbor)
                    parent_start[neighbor] = current
                    queue_start.append(neighbor)

                    if neighbor in visited_goal:

                        path = self.build_path(
                            neighbor,
                            parent_start,
                            parent_goal
                        )

                        return path, explored

            # -----------------------------
            # Expand from Goal
            # -----------------------------

            current = queue_goal.popleft()
            explored.append(current)

            for neighbor in self.get_neighbors(*current):

                if neighbor not in visited_goal:

                    visited_goal.add(neighbor)
                    parent_goal[neighbor] = current
                    queue_goal.append(neighbor)

                    if neighbor in visited_start:

                        path = self.build_path(
                            neighbor,
                            parent_start,
                            parent_goal
                        )

                        return path, explored

        return [], explored