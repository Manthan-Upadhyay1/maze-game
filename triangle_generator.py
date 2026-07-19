import random


class TriangleMazeGenerator:
    """
    Generates a perfect maze on a triangular-cell grid using
    Recursive Backtracking, mirroring MazeGenerator's approach
    but on triangle topology instead of a square grid.

    The overall shape is one big triangle made of `size` rows of small
    triangles. Row r (0 = top apex) contains (2r + 1) triangles,
    indexed by k = 0 .. 2r:

        k even  -> triangle points UP    (base at bottom)
        k odd   -> triangle points DOWN  (base at top)

    Each cell has 3 possible walls instead of 4:
        "left"  : shared with (row, k - 1)
        "right" : shared with (row, k + 1)
        "vert"  : shared with the row below (if pointing up)
                  or the row above (if pointing down)
    """

    def __init__(self, size):

        self.size = size

        self.cells = {}

        for r in range(size):
            for k in range(2 * r + 1):
                self.cells[(r, k)] = {
                    "left": True,
                    "right": True,
                    "vert": True,
                    "visited": False
                }

    # ------------------------------------------------

    def _neighbors(self, r, k):
        """Return [(neighbor_cell, my_wall, their_wall), ...]."""

        nbrs = []

        if k - 1 >= 0:
            nbrs.append(((r, k - 1), "left", "right"))

        if k + 1 <= 2 * r:
            nbrs.append(((r, k + 1), "right", "left"))

        if k % 2 == 0:
            if (r + 1, k + 1) in self.cells:
                nbrs.append(((r + 1, k + 1), "vert", "vert"))
        else:
            if (r - 1, k - 1) in self.cells:
                nbrs.append(((r - 1, k - 1), "vert", "vert"))

        return nbrs

    # ------------------------------------------------

    def generate(self):

        self._dfs((0, 0))

        for cell in self.cells.values():
            cell.pop("visited")

        return self.cells

    # ------------------------------------------------

    def _dfs(self, cell):

        r, k = cell
        self.cells[cell]["visited"] = True

        nbrs = self._neighbors(r, k)
        random.shuffle(nbrs)

        for other, me_wall, other_wall in nbrs:

            if not self.cells[other]["visited"]:

                self.cells[cell][me_wall] = False
                self.cells[other][other_wall] = False

                self._dfs(other)
