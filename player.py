from maze_utils import (
    is_circle_maze,
    is_hex_maze,
    is_hex_boundary_maze,
    is_triangle_maze,
    start_goal
)


class Player:
    """
    Player movement for:

    - Square maze
    - Triangle maze
    - Old hex-cell maze
    - New hexagonal-boundary maze
    - Circle maze
    """

    # ==========================================
    # OLD HEXAGONAL CELL MOVEMENT
    # ==========================================

    HEX_MOVES = {
        "NW": ("top_left", -1, 0),
        "NE": ("top_right", -1, 1),
        "E": ("right", 0, 1),
        "SE": ("bottom_right", 1, 0),
        "SW": ("bottom_left", 1, -1),
        "W": ("left", 0, -1),
    }

    def __init__(self, maze):

        self.maze = maze

        # --------------------------------------
        # Detect maze type
        # --------------------------------------

        # self.is_circle = is_circle_maze(maze)
        # self.is_triangle = is_triangle_maze(maze)

        # self.is_hex_cell = False
        # self.is_hex_boundary = False
        # self.is_square = False


        self.is_circle = is_circle_maze(maze)
        self.is_triangle = is_triangle_maze(maze)
        self.is_hex_cell = is_hex_maze(maze)
        self.is_hex_boundary = is_hex_boundary_maze(maze)
        self.is_square = isinstance(maze, list)

        # Look at one cell to determine wall format
        # if isinstance(maze, dict) and maze:

        #     first_cell = next(iter(maze.values()))

        #     # OLD honeycomb hexagon
        #     if (
        #         "top_left" in first_cell
        #         or "top_right" in first_cell
        #         or "bottom_left" in first_cell
        #         or "bottom_right" in first_cell
        #     ):
        #         self.is_hex_cell = True

        #     # NEW hexagonal-boundary maze
        #     elif all(
        #         wall in first_cell
        #         for wall in (
        #             "top",
        #             "right",
        #             "bottom",
        #             "left"
        #         )
        #     ):
        #         self.is_hex_boundary = True

        # # Normal square maze uses list-of-lists
        # elif isinstance(maze, list):
        #     self.is_square = True

        # --------------------------------------
        # Start / Goal
        # --------------------------------------

        start, goal = start_goal(maze)

        self.row, self.col = start

        self.goal_row, self.goal_col = goal

        self.start_row, self.start_col = start

    # ==========================================
    # POSITION
    # ==========================================

    def get_position(self):
        return self.row, self.col

    # ==========================================
    # NEW HEX BOUNDARY MOVEMENT
    # ==========================================

    def _move_hex_boundary(self, wall, dr, dc):

        current = (
            self.row,
            self.col
        )

        # Safety check
        if current not in self.maze:
            self.reset()
            return False

        cell = self.maze[current]

        # Wall exists -> cannot move
        if cell.get(wall, True):
            return False

        target = (
            self.row + dr,
            self.col + dc
        )

        # Target must actually exist because
        # the maze has missing corner cells.
        if target not in self.maze:
            return False

        self.row, self.col = target

        return True

    # ==========================================
    # OLD HEX CELL MOVEMENT
    # ==========================================

    def _move_hex_cell(self, direction):

        wall, dr, dc = self.HEX_MOVES[direction]

        current = (
            self.row,
            self.col
        )

        cell = self.maze.get(current)

        if cell is None:
            self.reset()
            return False

        target = (
            self.row + dr,
            self.col + dc
        )

        if (
            not cell.get(wall, True)
            and target in self.maze
        ):

            self.row, self.col = target

            return True

        return False

    # ==========================================
    # CIRCLE MOVEMENT
    # ==========================================

    def _move_circle(self, wall):

        current = (
            self.row,
            self.col
        )

        if current not in self.maze:
            self.reset()
            return False

        cell = self.maze[current]

        sectors = (
            max(c for _, c in self.maze)
            + 1
        )

        moves = {
            "inner": (
                self.row - 1,
                self.col
            ),

            "outer": (
                self.row + 1,
                self.col
            ),

            "ccw": (
                self.row,
                (self.col - 1) % sectors
            ),

            "cw": (
                self.row,
                (self.col + 1) % sectors
            ),
        }

        target = moves[wall]

        if (
            not cell.get(wall, True)
            and target in self.maze
        ):

            self.row, self.col = target

            return True

        return False

    # ==========================================
    # MOVE UP
    # ==========================================

    def move_up(self):

        # Circle
        if self.is_circle:
            return self._move_circle("outer")

        # New hexagonal-boundary maze
        if self.is_hex_boundary:

            return self._move_hex_boundary(
                "top",
                -1,
                0
            )

        # Old honeycomb maze
        if self.is_hex_cell:

            return self._move_hex_cell(
                "NW"
            )

        # Triangle
        if self.is_triangle:

            current = (
                self.row,
                self.col
            )

            if current not in self.maze:
                self.reset()
                return False

            cell = self.maze[current]

            if (
                self.col % 2 == 1
                and not cell.get(
                    "vert",
                    True
                )
            ):

                target = (
                    self.row - 1,
                    self.col - 1
                )

                if target in self.maze:

                    self.row, self.col = target

                    return True

            return False

        # Square
        if (
            self.row > 0
            and not self.maze[
                self.row
            ][self.col]["top"]
        ):

            self.row -= 1

            return True

        return False

    # ==========================================
    # MOVE DOWN
    # ==========================================

    def move_down(self):

        # Circle
        if self.is_circle:
            return self._move_circle("inner")

        # New hexagonal-boundary maze
        if self.is_hex_boundary:

            return self._move_hex_boundary(
                "bottom",
                1,
                0
            )

        # Old honeycomb maze
        if self.is_hex_cell:

            return self._move_hex_cell(
                "SE"
            )

        # Triangle
        if self.is_triangle:

            current = (
                self.row,
                self.col
            )

            if current not in self.maze:
                self.reset()
                return False

            cell = self.maze[current]

            if (
                self.col % 2 == 0
                and not cell.get(
                    "vert",
                    True
                )
            ):

                target = (
                    self.row + 1,
                    self.col + 1
                )

                if target in self.maze:

                    self.row, self.col = target

                    return True

            return False

        # Square
        if (
            self.row < len(self.maze) - 1
            and not self.maze[
                self.row
            ][self.col]["bottom"]
        ):

            self.row += 1

            return True

        return False

    # ==========================================
    # MOVE LEFT
    # ==========================================

    def move_left(self):

        # Circle
        if self.is_circle:
            return self._move_circle("ccw")

        # New hexagonal-boundary maze
        if self.is_hex_boundary:

            return self._move_hex_boundary(
                "left",
                0,
                -1
            )

        # Old honeycomb
        if self.is_hex_cell:

            return self._move_hex_cell(
                "W"
            )

        # Triangle
        if self.is_triangle:

            current = (
                self.row,
                self.col
            )

            if current not in self.maze:
                self.reset()
                return False

            cell = self.maze[current]

            target = (
                self.row,
                self.col - 1
            )

            if (
                not cell.get(
                    "left",
                    True
                )
                and target in self.maze
            ):

                self.col -= 1

                return True

            return False

        # Square
        if (
            self.col > 0
            and not self.maze[
                self.row
            ][self.col]["left"]
        ):

            self.col -= 1

            return True

        return False

    # ==========================================
    # MOVE RIGHT
    # ==========================================

    def move_right(self):

        # Circle
        if self.is_circle:
            return self._move_circle("cw")

        # New hexagonal-boundary maze
        if self.is_hex_boundary:

            return self._move_hex_boundary(
                "right",
                0,
                1
            )

        # Old honeycomb
        if self.is_hex_cell:

            return self._move_hex_cell(
                "E"
            )

        # Triangle
        if self.is_triangle:

            current = (
                self.row,
                self.col
            )

            if current not in self.maze:
                self.reset()
                return False

            cell = self.maze[current]

            target = (
                self.row,
                self.col + 1
            )

            if (
                not cell.get(
                    "right",
                    True
                )
                and target in self.maze
            ):

                self.col += 1

                return True

            return False

        # Square
        if (
            self.col < len(
                self.maze[0]
            ) - 1
            and not self.maze[
                self.row
            ][self.col]["right"]
        ):

            self.col += 1

            return True

        return False

    # ==========================================
    # OLD HEXAGON EXTRA DIRECTIONS
    # ==========================================

    def move_north_east(self):

        if self.is_hex_cell:
            return self._move_hex_cell(
                "NE"
            )

        return False

    def move_south_west(self):

        if self.is_hex_cell:
            return self._move_hex_cell(
                "SW"
            )

        return False

    # ==========================================
    # GOAL
    # ==========================================

    def reached_goal(self):

        return (
            self.row,
            self.col
        ) == (
            self.goal_row,
            self.goal_col
        )

    # ==========================================
    # RESET
    # ==========================================

    def reset(self):

        self.row = self.start_row
        self.col = self.start_col