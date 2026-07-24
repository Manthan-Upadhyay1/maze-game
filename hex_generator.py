# import random


# class HexMazeGenerator:
#     """Generate a perfect pointy-top hexagonal maze using DFS backtracking."""

#     DIRECTIONS = (
#         ("top_left", (-1, 0), "bottom_right"),
#         ("top_right", (-1, 1), "bottom_left"),
#         ("right", (0, 1), "left"),
#         ("bottom_right", (1, 0), "top_left"),
#         ("bottom_left", (1, -1), "top_right"),
#         ("left", (0, -1), "right"),
#     )

#     def __init__(self, rows, cols):
#         self.rows = rows
#         self.cols = cols
#         self.cells = {
#             (row, col): {
#                 "top_left": True,
#                 "top_right": True,
#                 "right": True,
#                 "bottom_right": True,
#                 "bottom_left": True,
#                 "left": True,
#                 "visited": False,
#             }
#             for row in range(rows)
#             for col in range(cols)
#         }

#     def _neighbors(self, row, col):
#         neighbors = []
#         for wall, (dr, dc), opposite_wall in self.DIRECTIONS:
#             other = (row + dr, col + dc)
#             if other in self.cells:
#                 neighbors.append((other, wall, opposite_wall))
#         return neighbors

#     def _dfs(self, cell):
#         self.cells[cell]["visited"] = True
#         row, col = cell
#         neighbors = self._neighbors(row, col)
#         random.shuffle(neighbors)

#         for other, wall, opposite_wall in neighbors:
#             if not self.cells[other]["visited"]:
#                 self.cells[cell][wall] = False
#                 self.cells[other][opposite_wall] = False
#                 self._dfs(other)

#     def generate(self):
#         self._dfs((0, 0))
#         for cell in self.cells.values():
#             cell.pop("visited")
#         return self.cells



# import random


# class HexBoundaryMazeGenerator:
#     """
#     Generate a perfect maze using rectangular cells arranged
#     inside an overall hexagonal shape.

#     Internal passages:
#         UP / DOWN / LEFT / RIGHT

#     Overall maze:
#         Hexagonal
#     """

#     DIRECTIONS = (
#         ("top", (-1, 0), "bottom"),
#         ("right", (0, 1), "left"),
#         ("bottom", (1, 0), "top"),
#         ("left", (0, -1), "right"),
#     )

#     def __init__(self, rows=21, cols=25):
#         # Odd dimensions produce a more symmetrical hexagon
#         if rows % 2 == 0:
#             rows += 1

#         if cols % 2 == 0:
#             cols += 1

#         self.rows = rows
#         self.cols = cols

#         self.cells = {}

#         # Create only cells that belong inside the hexagon
#         for row in range(rows):
#             for col in range(cols):

#                 if self._inside_hexagon(row, col):
#                     self.cells[(row, col)] = {
#                         "top": True,
#                         "right": True,
#                         "bottom": True,
#                         "left": True,
#                         "visited": False,
#                     }

#     def _inside_hexagon(self, row, col):
#         """
#         Determine whether a rectangular grid cell belongs
#         inside the overall hexagonal maze.
#         """

#         center_row = (self.rows - 1) / 2

#         # 0 at center, increasing toward top/bottom
#         distance = abs(row - center_row)

#         # Controls the slope of the left/right edges
#         max_cut = self.cols // 4

#         cut = int(
#             (distance / max(center_row, 1)) * max_cut
#         )

#         return cut <= col < self.cols - cut

#     def _neighbors(self, row, col):
#         neighbors = []

#         for wall, (dr, dc), opposite_wall in self.DIRECTIONS:

#             other = (row + dr, col + dc)

#             if other in self.cells:
#                 neighbors.append(
#                     (other, wall, opposite_wall)
#                 )

#         return neighbors

#     def _dfs(self, start):
#         stack = [start]

#         self.cells[start]["visited"] = True

#         while stack:
#             current = stack[-1]

#             row, col = current

#             neighbors = [
#                 n for n in self._neighbors(row, col)
#                 if not self.cells[n[0]]["visited"]
#             ]

#             if not neighbors:
#                 stack.pop()
#                 continue

#             other, wall, opposite_wall = random.choice(neighbors)

#             # Remove wall between current and neighbor
#             self.cells[current][wall] = False
#             self.cells[other][opposite_wall] = False

#             self.cells[other]["visited"] = True

#             stack.append(other)

#     def generate(self):

#         if not self.cells:
#             return {}

#         # Prefer left-most valid cell near vertical center
#         center_row = self.rows // 2

#         candidates = [
#             cell
#             for cell in self.cells
#             if cell[0] == center_row
#         ]

#         if candidates:
#             start = min(candidates, key=lambda x: x[1])
#         else:
#             start = next(iter(self.cells))

#         self._dfs(start)

#         # Remove temporary visited property
#         for cell in self.cells.values():
#             cell.pop("visited", None)

#         return self.cells



import random


class HexBoundaryMazeGenerator:
    """
    Generates a rectangular-cell maze whose overall
    silhouette is approximately hexagonal.

    Each cell has four walls:
        top
        right
        bottom
        left
    """

    DIRECTIONS = (
        ("top", (-1, 0), "bottom"),
        ("right", (0, 1), "left"),
        ("bottom", (1, 0), "top"),
        ("left", (0, -1), "right"),
    )

    def __init__(self, rows=21, cols=25):
        # Odd sizes make the shape more symmetrical
        if rows % 2 == 0:
            rows += 1

        if cols % 2 == 0:
            cols += 1

        self.rows = rows
        self.cols = cols

        self.cells = {}

        # Create only cells that belong to the
        # hexagonal-shaped region
        for row in range(rows):
            for col in range(cols):

                if self._inside_hexagon(row, col):

                    self.cells[(row, col)] = {
                        "top": True,
                        "right": True,
                        "bottom": True,
                        "left": True,
                        "visited": False,
                    }

    def _inside_hexagon(self, row, col):
        """
        Makes the rectangular grid narrower near
        the top and bottom.
        """

        center_row = (self.rows - 1) / 2

        distance = abs(row - center_row)

        max_cut = self.cols // 4

        if center_row == 0:
            cut = 0
        else:
            cut = int(
                (distance / center_row) * max_cut
            )

        return cut <= col < self.cols - cut

    def _neighbors(self, row, col):

        neighbors = []

        for wall, (dr, dc), opposite in self.DIRECTIONS:

            nr = row + dr
            nc = col + dc

            other = (nr, nc)

            if other in self.cells:

                neighbors.append(
                    (other, wall, opposite)
                )

        return neighbors

    def _dfs(self, start):

        stack = [start]

        self.cells[start]["visited"] = True

        while stack:

            current = stack[-1]

            row, col = current

            neighbors = [
                item
                for item in self._neighbors(row, col)
                if not self.cells[item[0]]["visited"]
            ]

            if not neighbors:
                stack.pop()
                continue

            other, wall, opposite = random.choice(
                neighbors
            )

            # Remove wall between the cells
            self.cells[current][wall] = False
            self.cells[other][opposite] = False

            self.cells[other]["visited"] = True

            stack.append(other)

    def generate(self):

        if not self.cells:
            return {}

        # Start near the left side of the middle row
        middle = self.rows // 2

        candidates = [
            cell
            for cell in self.cells
            if cell[0] == middle
        ]

        if candidates:
            start = min(
                candidates,
                key=lambda cell: cell[1]
            )
        else:
            start = next(iter(self.cells))

        self._dfs(start)

        # Remove temporary visited flag
        for cell in self.cells.values():
            cell.pop("visited", None)

        return self.cells