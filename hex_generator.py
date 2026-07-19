import random


class HexMazeGenerator:
    """Generate a perfect pointy-top hexagonal maze using DFS backtracking."""

    DIRECTIONS = (
        ("top_left", (-1, 0), "bottom_right"),
        ("top_right", (-1, 1), "bottom_left"),
        ("right", (0, 1), "left"),
        ("bottom_right", (1, 0), "top_left"),
        ("bottom_left", (1, -1), "top_right"),
        ("left", (0, -1), "right"),
    )

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = {
            (row, col): {
                "top_left": True,
                "top_right": True,
                "right": True,
                "bottom_right": True,
                "bottom_left": True,
                "left": True,
                "visited": False,
            }
            for row in range(rows)
            for col in range(cols)
        }

    def _neighbors(self, row, col):
        neighbors = []
        for wall, (dr, dc), opposite_wall in self.DIRECTIONS:
            other = (row + dr, col + dc)
            if other in self.cells:
                neighbors.append((other, wall, opposite_wall))
        return neighbors

    def _dfs(self, cell):
        self.cells[cell]["visited"] = True
        row, col = cell
        neighbors = self._neighbors(row, col)
        random.shuffle(neighbors)

        for other, wall, opposite_wall in neighbors:
            if not self.cells[other]["visited"]:
                self.cells[cell][wall] = False
                self.cells[other][opposite_wall] = False
                self._dfs(other)

    def generate(self):
        self._dfs((0, 0))
        for cell in self.cells.values():
            cell.pop("visited")
        return self.cells
