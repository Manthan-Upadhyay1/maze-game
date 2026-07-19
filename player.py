from maze_utils import is_circle_maze, is_hex_maze, is_triangle_maze, start_goal


class Player:
    """Track and move the player in square, triangle, and hex mazes."""

    HEX_MOVES = {
        "NW": ("top_left", -1, 0), "NE": ("top_right", -1, 1),
        "E": ("right", 0, 1), "SE": ("bottom_right", 1, 0),
        "SW": ("bottom_left", 1, -1), "W": ("left", 0, -1),
    }

    def __init__(self, maze):
        self.maze = maze
        self.is_triangle = is_triangle_maze(maze)
        self.is_hex = is_hex_maze(maze)
        self.is_circle = is_circle_maze(maze)
        start, goal = start_goal(maze)
        self.row, self.col = start
        self.goal_row, self.goal_col = goal
        self.start_row, self.start_col = start

    def get_position(self):
        return self.row, self.col

    def _move_circle(self, wall):
        cell = self.maze[(self.row, self.col)]
        sectors = max(c for _, c in self.maze) + 1
        moves = {"inner": (self.row - 1, self.col), "outer": (self.row + 1, self.col), "ccw": (self.row, (self.col - 1) % sectors), "cw": (self.row, (self.col + 1) % sectors)}
        if not cell[wall] and moves[wall] in self.maze:
            self.row, self.col = moves[wall]

    def _move_hex(self, direction):
        wall, dr, dc = self.HEX_MOVES[direction]
        cell = self.maze.get((self.row, self.col))
        if cell is None:
            # Player position is out of sync with the current maze
            # (e.g. maze was rebuilt without resetting the player).
            self.reset()
            return
        other = (self.row + dr, self.col + dc)
        if not cell.get(wall, True) and other in self.maze:
            self.row, self.col = other

    def move_up(self):
        if self.is_circle:
            return self._move_circle("outer")
        if self.is_hex:
            return self._move_hex("NW")
        if self.is_triangle:
            cell = self.maze[(self.row, self.col)]
            if self.col % 2 == 1 and not cell["vert"]:
                self.row, self.col = self.row - 1, self.col - 1
            return
        if not self.maze[self.row][self.col]["top"] and self.row > 0:
            self.row -= 1

    def move_down(self):
        if self.is_circle:
            return self._move_circle("inner")
        if self.is_hex:
            return self._move_hex("SE")
        if self.is_triangle:
            cell = self.maze[(self.row, self.col)]
            if self.col % 2 == 0 and not cell["vert"]:
                self.row, self.col = self.row + 1, self.col + 1
            return
        if not self.maze[self.row][self.col]["bottom"] and self.row < len(self.maze) - 1:
            self.row += 1

    def move_left(self):
        if self.is_circle:
            return self._move_circle("ccw")
        if self.is_hex:
            return self._move_hex("W")
        if self.is_triangle:
            cell = self.maze[(self.row, self.col)]
            if not cell["left"] and (self.row, self.col - 1) in self.maze:
                self.col -= 1
            return
        if not self.maze[self.row][self.col]["left"] and self.col > 0:
            self.col -= 1

    def move_right(self):
        if self.is_circle:
            return self._move_circle("cw")
        if self.is_hex:
            return self._move_hex("E")
        if self.is_triangle:
            cell = self.maze[(self.row, self.col)]
            if not cell["right"] and (self.row, self.col + 1) in self.maze:
                self.col += 1
            return
        if not self.maze[self.row][self.col]["right"] and self.col < len(self.maze[0]) - 1:
            self.col += 1

    def move_north_east(self):
        if self.is_hex:
            self._move_hex("NE")

    def move_south_west(self):
        if self.is_hex:
            self._move_hex("SW")

    def reached_goal(self):
        return (self.row, self.col) == (self.goal_row, self.goal_col)

    def reset(self):
        self.row, self.col = self.start_row, self.start_col
