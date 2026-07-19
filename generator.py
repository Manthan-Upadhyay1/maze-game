import random


class MazeGenerator:
    """
    Generates a perfect square maze using
    Recursive Backtracking.
    """

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        # Every cell initially has
        # Top, Right, Bottom, Left walls

        self.maze = [
            [
                {
                    "top": True,
                    "right": True,
                    "bottom": True,
                    "left": True,
                    "visited": False
                }

                for _ in range(cols)

            ]

            for _ in range(rows)
        ]

    # ------------------------------------------------

    def generate(self):

        self._dfs(0, 0)

        # Remove visited flag before returning

        for r in range(self.rows):
            for c in range(self.cols):
                self.maze[r][c].pop("visited")

        return self.maze

    # ------------------------------------------------

    def _dfs(self, row, col):

        self.maze[row][col]["visited"] = True

        directions = [
            (-1, 0),   # Top
            (1, 0),    # Bottom
            (0, -1),   # Left
            (0, 1)     # Right
        ]

        random.shuffle(directions)

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if (
                0 <= nr < self.rows
                and
                0 <= nc < self.cols
                and
                not self.maze[nr][nc]["visited"]
            ):

                # Remove wall

                if dr == -1:
                    self.maze[row][col]["top"] = False
                    self.maze[nr][nc]["bottom"] = False

                elif dr == 1:
                    self.maze[row][col]["bottom"] = False
                    self.maze[nr][nc]["top"] = False

                elif dc == -1:
                    self.maze[row][col]["left"] = False
                    self.maze[nr][nc]["right"] = False

                elif dc == 1:
                    self.maze[row][col]["right"] = False
                    self.maze[nr][nc]["left"] = False

                self._dfs(nr, nc)