
import cv2
import numpy as np
import math

from maze_utils import maze_size, start_goal


class MazeDrawer:
    """
    Draws the maze, player, explored nodes and solution path.
    """

    def __init__(
        self,
        maze,
        cell_size=40,
        player=None,
        path=None,
        explored=None
    ):

        self.maze = maze
        self.cell_size = cell_size
        self.player = player
        self.path = path
        self.explored = explored

        self.rows = len(maze)
        self.cols = len(maze[0])

        self.width = self.cols * cell_size
        self.height = self.rows * cell_size

    # -------------------------------------------------

    def draw(self):

        image = np.ones(
            (self.height + 1, self.width + 1, 3),
            dtype=np.uint8
        ) * 255

        # -----------------------------
        # Draw Maze Walls
        # -----------------------------

        for row in range(self.rows):

            for col in range(self.cols):

                cell = self.maze[row][col]

                x = col * self.cell_size
                y = row * self.cell_size

                if cell["top"]:
                    cv2.line(image, (x, y),
                             (x + self.cell_size, y),
                             (0, 0, 0), 2)

                if cell["left"]:
                    cv2.line(image, (x, y),
                             (x, y + self.cell_size),
                             (0, 0, 0), 2)

                if cell["right"]:
                    cv2.line(image,
                             (x + self.cell_size, y),
                             (x + self.cell_size,
                              y + self.cell_size),
                             (0, 0, 0), 2)

                if cell["bottom"]:
                    cv2.line(image,
                             (x, y + self.cell_size),
                             (x + self.cell_size,
                              y + self.cell_size),
                             (0, 0, 0), 2)

        # -----------------------------
        # Start Cell
        # -----------------------------

        cv2.rectangle(
            image,
            (5, 5),
            (self.cell_size - 5, self.cell_size - 5),
            (0, 255, 0),
            -1
        )

        # -----------------------------
        # Goal
        # -----------------------------

        goal_x = (self.cols - 1) * self.cell_size + self.cell_size // 2
        goal_y = (self.rows - 1) * self.cell_size + self.cell_size // 2

        cv2.circle(
            image,
            (goal_x, goal_y),
            self.cell_size // 4,
            (0, 0, 255),
            -1
        )

        # -----------------------------
        # Explored Nodes
        # -----------------------------

        if self.explored is not None:

            for row, col in self.explored:

                cx = col * self.cell_size + self.cell_size // 2
                cy = row * self.cell_size + self.cell_size // 2

                cv2.circle(
                    image,
                    (cx, cy),
                    self.cell_size // 8,
                    (255, 150, 0),
                    -1
                )

        # -----------------------------
        # Final Path
        # -----------------------------

        if self.path is not None:

            for row, col in self.path:

                cx = col * self.cell_size + self.cell_size // 2
                cy = row * self.cell_size + self.cell_size // 2

                cv2.circle(
                    image,
                    (cx, cy),
                    self.cell_size // 6,
                    (255, 0, 255),
                    -1
                )

        # -----------------------------
        # Player
        # -----------------------------

        if self.player is not None:

            row, col = self.player.get_position()

            cx = col * self.cell_size + self.cell_size // 2
            cy = row * self.cell_size + self.cell_size // 2

            cv2.circle(
                image,
                (cx, cy),
                self.cell_size // 4,
                (255, 0, 0),
                -1
            )

        return image

class TriangleMazeDrawer:
    """
    Draws a true triangular-cell maze (3 walls per cell).
    Produces a BGR image (same convention as MazeDrawer) so it can be
    passed straight to st.image(..., channels="BGR").
    """

    def __init__(
        self,
        maze,
        cell_size=40,
        player=None,
        path=None,
        explored=None
    ):

        self.maze = maze
        self.cell_size = cell_size
        self.player = player
        self.path = path
        self.explored = explored

        self.size, _ = maze_size(maze)
        self.h = math.sqrt(3) / 2  # equilateral triangle height factor

        self.x_offset = (self.size / 2 + 1) * cell_size
        self.y_offset = cell_size // 2

        self.width = int((self.size + 2) * cell_size)
        self.height = int(self.size * self.h * cell_size) + cell_size

    # -------------------------------------------------

    def _point(self, row, col_index):

        x = self.x_offset + col_index * self.cell_size
        y = self.y_offset + row * self.h * self.cell_size

        return int(round(x)), int(round(y))

    # -------------------------------------------------

    def _cell_geometry(self, r, k):
        """Return (centroid, {wall_name: (pointA, pointB)})."""

        if k % 2 == 0:
            col = k // 2
            apex = self._point(r, col - r / 2)
            left = self._point(r + 1, col - (r + 1) / 2)
            right = self._point(r + 1, col - (r + 1) / 2 + 1)

            edges = {
                "left": (apex, left),
                "right": (apex, right),
                "vert": (left, right)
            }

            centroid = (
                (apex[0] + left[0] + right[0]) // 3,
                (apex[1] + left[1] + right[1]) // 3
            )

        else:
            col = (k - 1) // 2
            bottom = self._point(r + 1, col - (r + 1) / 2 + 1)
            topleft = self._point(r, col - r / 2)
            topright = self._point(r, col - r / 2 + 1)

            edges = {
                "left": (topleft, bottom),
                "right": (topright, bottom),
                "vert": (topleft, topright)
            }

            centroid = (
                (bottom[0] + topleft[0] + topright[0]) // 3,
                (bottom[1] + topleft[1] + topright[1]) // 3
            )

        return centroid, edges

    # -------------------------------------------------

    def draw(self):

        image = np.ones(
            (self.height + 1, self.width + 1, 3),
            dtype=np.uint8
        ) * 255

        centroids = {}

        # -----------------------------
        # Walls
        # -----------------------------

        for (r, k), cell in self.maze.items():

            centroid, edges = self._cell_geometry(r, k)
            centroids[(r, k)] = centroid

            for wall_name, present in cell.items():
                if present:
                    (x1, y1), (x2, y2) = edges[wall_name]
                    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 0), 2)

        # -----------------------------
        # Start / Goal
        # -----------------------------

        start, goal = start_goal(self.maze)

        sx, sy = centroids[start]
        gx, gy = centroids[goal]

        cv2.circle(image, (sx, sy), self.cell_size // 4, (0, 255, 0), -1)
        cv2.circle(image, (gx, gy), self.cell_size // 4, (0, 0, 255), -1)

        # -----------------------------
        # Explored Nodes
        # -----------------------------

        if self.explored is not None:
            for cell in self.explored:
                cx, cy = centroids[cell]
                cv2.circle(image, (cx, cy), self.cell_size // 8, (255, 150, 0), -1)

        # -----------------------------
        # Final Path
        # -----------------------------

        if self.path is not None:
            for cell in self.path:
                cx, cy = centroids[cell]
                cv2.circle(image, (cx, cy), self.cell_size // 6, (255, 0, 255), -1)

        # -----------------------------
        # Player
        # -----------------------------

        if self.player is not None:
            pos = self.player.get_position()
            cx, cy = centroids[pos]
            cv2.circle(image, (cx, cy), self.cell_size // 4, (255, 0, 0), -1)

        return image

class HexMazeDrawer:
    """Draw a pointy-top hexagonal maze stored in axial-offset rows/columns."""

    WALL_EDGES = {
        "top_left": (0, 5), "top_right": (0, 1), "right": (1, 2),
        "bottom_right": (2, 3), "bottom_left": (3, 4), "left": (4, 5),
    }

    def __init__(self, maze, cell_size=24, player=None, path=None, explored=None):
        self.maze = maze
        self.cell_size = cell_size
        self.player = player
        self.path = path
        self.explored = explored
        self.rows = max(row for row, _ in maze) + 1
        self.cols = max(col for _, col in maze) + 1
        self.radius = cell_size
        self.margin = cell_size + 4
        self.width = int(math.sqrt(3) * self.radius * (self.cols + (self.rows - 1) / 2) + 2 * self.margin)
        self.height = int(self.radius * (1.5 * (self.rows - 1) + 2) + 2 * self.margin)

    def _center(self, row, col):
        return (
            int(round(self.margin + math.sqrt(3) * self.radius * (col + row / 2))),
            int(round(self.margin + self.radius + 1.5 * self.radius * row)),
        )

    def _points(self, row, col):
        cx, cy = self._center(row, col)
        return [
            (int(round(cx + self.radius * math.cos(math.radians(angle)))),
             int(round(cy + self.radius * math.sin(math.radians(angle)))))
            for angle in (-90, -30, 30, 90, 150, 210)
        ]

    def draw(self):
        image = np.ones((self.height + 1, self.width + 1, 3), dtype=np.uint8) * 255
        centers = {}
        for cell_id, cell in self.maze.items():
            row, col = cell_id
            points = self._points(row, col)
            centers[cell_id] = self._center(row, col)
            for wall, (first, second) in self.WALL_EDGES.items():
                if cell[wall]:
                    cv2.line(image, points[first], points[second], (0, 0, 0), 2)

        start, goal = start_goal(self.maze)
        marker_radius = max(3, self.radius // 3)
        cv2.circle(image, centers[start], marker_radius, (0, 255, 0), -1)
        cv2.circle(image, centers[goal], marker_radius, (0, 0, 255), -1)

        if self.explored is not None:
            for cell_id in self.explored:
                cv2.circle(image, centers[cell_id], max(2, self.radius // 6), (255, 150, 0), -1)
        if self.path is not None:
            for cell_id in self.path:
                cv2.circle(image, centers[cell_id], max(2, self.radius // 5), (255, 0, 255), -1)
        if self.player is not None:
            cv2.circle(image, centers[self.player.get_position()], marker_radius, (255, 0, 0), -1)
        return image

class CircleMazeDrawer:
    """Draw a maze made of concentric circular rings."""

    def __init__(self, maze, cell_size=22, player=None, path=None, explored=None):
        self.maze, self.cell_size, self.player = maze, cell_size, player
        self.path, self.explored = path, explored
        self.rings = max(r for r, _ in maze) + 1
        self.sectors = max(s for _, s in maze) + 1
        self.margin = cell_size + 8
        self.radius = self.rings * cell_size + self.margin
        self.size = self.radius * 2 + 2

    def _center(self, ring, sector):
        angle = 2 * math.pi * (sector + .5) / self.sectors - math.pi / 2
        distance = self.margin + (ring + .5) * self.cell_size
        return int(self.radius + distance * math.cos(angle)), int(self.radius + distance * math.sin(angle))

    def _arc(self, image, radius, start, end):
        cv2.ellipse(image, (self.radius, self.radius), (radius, radius), 0, start, end, (0, 0, 0), 2)

    def draw(self):
        image = np.ones((self.size, self.size, 3), dtype=np.uint8) * 255
        for (ring, sector), cell in self.maze.items():
            start = 360 * sector / self.sectors - 90
            end = 360 * (sector + 1) / self.sectors - 90
            inner = self.margin + ring * self.cell_size
            outer = inner + self.cell_size
            if cell["inner"]: self._arc(image, inner, start, end)
            if cell["outer"]: self._arc(image, outer, start, end)
            for wall, angle in (("ccw", start), ("cw", end)):
                if cell[wall]:
                    radians = math.radians(angle)
                    p1 = (int(self.radius + inner * math.cos(radians)), int(self.radius + inner * math.sin(radians)))
                    p2 = (int(self.radius + outer * math.cos(radians)), int(self.radius + outer * math.sin(radians)))
                    cv2.line(image, p1, p2, (0, 0, 0), 2)
        start, goal = start_goal(self.maze)
        marker = max(3, self.cell_size // 4)
        for cell in self.explored or []: cv2.circle(image, self._center(*cell), max(2, marker // 2), (255, 150, 0), -1)
        for cell in self.path or []: cv2.circle(image, self._center(*cell), max(2, marker // 2), (255, 0, 255), -1)
        cv2.circle(image, self._center(*start), marker, (0, 255, 0), -1)
        cv2.circle(image, self._center(*goal), marker, (0, 0, 255), -1)
        if self.player: cv2.circle(image, self._center(*self.player.get_position()), marker, (255, 0, 0), -1)
        return image
