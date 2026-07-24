# def is_circle_maze(maze):
#     return isinstance(maze, dict) and bool(maze) and "inner" in next(iter(maze.values()))
# def is_hex_maze(maze):
#     return isinstance(maze, dict) and bool(maze) and "top_left" in next(iter(maze.values()))
# def is_triangle_maze(maze):
#     return isinstance(maze, dict) and not is_hex_maze(maze) and not is_circle_maze(maze)
# def maze_size(maze):
#     if isinstance(maze, dict): return max(r for r,_ in maze)+1, (None if is_triangle_maze(maze) else max(c for _,c in maze)+1)
#     return len(maze), len(maze[0])
# def start_goal(maze):
#     rows, cols=maze_size(maze)
#     return ((0,0),(rows-1,2*(rows-1))) if is_triangle_maze(maze) else ((0,0),(rows-1,cols-1))
# def get_neighbors(maze,row,col):
#     if is_triangle_maze(maze):
#         cell=maze[(row,col)]; out=[]
#         for wall,other in (("left",(row,col-1)),("right",(row,col+1)),("vert",(row+1,col+1) if col%2==0 else (row-1,col-1))):
#             if not cell[wall] and other in maze: out.append(other)
#         return out
#     if is_circle_maze(maze):
#         cell=maze[(row,col)]; sectors=max(c for _,c in maze)+1
#         return [other for wall,other in (("inner",(row-1,col)),("outer",(row+1,col)),("ccw",(row,(col-1)%sectors)),("cw",(row,(col+1)%sectors))) if not cell[wall] and other in maze]
#     if is_hex_maze(maze):
#         cell=maze[(row,col)]; dirs=(("top_left",-1,0),("top_right",-1,1),("right",0,1),("bottom_right",1,0),("bottom_left",1,-1),("left",0,-1))
#         return [(row+dr,col+dc) for wall,dr,dc in dirs if not cell[wall] and (row+dr,col+dc) in maze]
#     cell=maze[row][col]; rows,cols=maze_size(maze); out=[]
#     for wall,other in (("top",(row-1,col)),("bottom",(row+1,col)),("left",(row,col-1)),("right",(row,col+1))):
#         if not cell[wall] and 0<=other[0]<rows and 0<=other[1]<cols: out.append(other)
#     return out
# def heuristic(node,goal): return abs(node[0]-goal[0])+abs(node[1]-goal[1])
# def wall_keys(maze):
#     if is_triangle_maze(maze): return ["left","right","vert"]
#     if is_circle_maze(maze): return ["inner","outer","cw","ccw"]
#     if is_hex_maze(maze): return ["top_left","top_right","right","bottom_right","bottom_left","left"]
#     return ["top","bottom","left","right"]
# def iter_cells(maze): return maze.values() if isinstance(maze,dict) else (c for row in maze for c in row)
# def cell_count(maze): return len(maze) if isinstance(maze,dict) else len(maze)*len(maze[0])



def _first_cell(maze):
    if isinstance(maze, dict) and maze:
        return next(iter(maze.values()))
    return None


def is_circle_maze(maze):
    cell = _first_cell(maze)

    return (
        cell is not None
        and "inner" in cell
        and "outer" in cell
        and "cw" in cell
        and "ccw" in cell
    )


def is_hex_maze(maze):
    """
    OLD honeycomb/hex-cell maze.
    """

    cell = _first_cell(maze)

    return (
        cell is not None
        and "top_left" in cell
        and "top_right" in cell
        and "bottom_left" in cell
        and "bottom_right" in cell
    )


def is_hex_boundary_maze(maze):
    """
    NEW maze:
    rectangular cells arranged inside
    an overall hexagonal boundary.
    """

    cell = _first_cell(maze)

    if cell is None:
        return False

    required = {
        "top",
        "right",
        "bottom",
        "left"
    }

    return required.issubset(cell.keys())


def is_triangle_maze(maze):
    cell = _first_cell(maze)

    if cell is None:
        return False

    return (
        "left" in cell
        and "right" in cell
        and "vert" in cell
    )


def maze_size(maze):

    if isinstance(maze, dict):

        rows = max(
            r for r, _ in maze
        ) + 1

        cols = max(
            c for _, c in maze
        ) + 1

        if is_triangle_maze(maze):
            return rows, None

        return rows, cols

    return len(maze), len(maze[0])


def start_goal(maze):
    """
    Return valid start and goal cells.
    """

    # =====================================
    # TRIANGLE
    # =====================================

    if is_triangle_maze(maze):

        rows, _ = maze_size(maze)

        start = (0, 0)
        goal = (
            rows - 1,
            2 * (rows - 1)
        )

        return start, goal

    # =====================================
    # NEW HEX BOUNDARY
    # =====================================

    if is_hex_boundary_maze(maze):

        cells = list(maze.keys())

        # Vertical center
        middle_row = (
            max(r for r, _ in cells)
            // 2
        )

        # Start = left-most cell,
        # preferring vertical center
        start = min(
            cells,
            key=lambda cell: (
                cell[1],
                abs(cell[0] - middle_row)
            )
        )

        # Goal = right-most cell,
        # preferring vertical center
        goal = max(
            cells,
            key=lambda cell: (
                cell[1],
                -abs(cell[0] - middle_row)
            )
        )

        return start, goal

    # =====================================
    # OLD HEX / CIRCLE
    # =====================================

    if isinstance(maze, dict):

        cells = list(maze.keys())

        return (
            min(cells),
            max(cells)
        )

    # =====================================
    # SQUARE
    # =====================================

    rows = len(maze)
    cols = len(maze[0])

    return (
        (0, 0),
        (rows - 1, cols - 1)
    )


def get_neighbors(maze, row, col):

    # =====================================
    # TRIANGLE
    # =====================================

    if is_triangle_maze(maze):

        cell = maze[(row, col)]

        out = []

        moves = (
            (
                "left",
                (row, col - 1)
            ),
            (
                "right",
                (row, col + 1)
            ),
            (
                "vert",
                (
                    (row + 1, col + 1)
                    if col % 2 == 0
                    else (row - 1, col - 1)
                )
            ),
        )

        for wall, other in moves:

            if (
                not cell.get(wall, True)
                and other in maze
            ):
                out.append(other)

        return out

    # =====================================
    # CIRCLE
    # =====================================

    if is_circle_maze(maze):

        cell = maze[(row, col)]

        sectors = (
            max(c for _, c in maze)
            + 1
        )

        moves = (
            (
                "inner",
                (row - 1, col)
            ),
            (
                "outer",
                (row + 1, col)
            ),
            (
                "ccw",
                (
                    row,
                    (col - 1) % sectors
                )
            ),
            (
                "cw",
                (
                    row,
                    (col + 1) % sectors
                )
            ),
        )

        return [
            other
            for wall, other in moves
            if (
                not cell.get(wall, True)
                and other in maze
            )
        ]

    # =====================================
    # OLD HEX CELL
    # =====================================

    if is_hex_maze(maze):

        cell = maze[(row, col)]

        directions = (
            ("top_left", -1, 0),
            ("top_right", -1, 1),
            ("right", 0, 1),
            ("bottom_right", 1, 0),
            ("bottom_left", 1, -1),
            ("left", 0, -1),
        )

        return [
            (row + dr, col + dc)
            for wall, dr, dc in directions
            if (
                not cell.get(wall, True)
                and (row + dr, col + dc)
                in maze
            )
        ]

    # =====================================
    # NEW HEX BOUNDARY
    # =====================================

    if is_hex_boundary_maze(maze):

        current = (row, col)

        if current not in maze:
            return []

        cell = maze[current]

        directions = (
            ("top", -1, 0),
            ("bottom", 1, 0),
            ("left", 0, -1),
            ("right", 0, 1),
        )

        neighbors = []

        for wall, dr, dc in directions:

            other = (
                row + dr,
                col + dc
            )

            if (
                not cell.get(wall, True)
                and other in maze
            ):
                neighbors.append(other)

        return neighbors

    # =====================================
    # SQUARE
    # =====================================

    cell = maze[row][col]

    rows = len(maze)
    cols = len(maze[0])

    neighbors = []

    directions = (
        ("top", -1, 0),
        ("bottom", 1, 0),
        ("left", 0, -1),
        ("right", 0, 1),
    )

    for wall, dr, dc in directions:

        nr = row + dr
        nc = col + dc

        if (
            not cell.get(wall, True)
            and 0 <= nr < rows
            and 0 <= nc < cols
        ):
            neighbors.append(
                (nr, nc)
            )

    return neighbors


def heuristic(node, goal):

    return (
        abs(node[0] - goal[0])
        + abs(node[1] - goal[1])
    )


def wall_keys(maze):

    if is_triangle_maze(maze):
        return [
            "left",
            "right",
            "vert"
        ]

    if is_circle_maze(maze):
        return [
            "inner",
            "outer",
            "cw",
            "ccw"
        ]

    if is_hex_maze(maze):
        return [
            "top_left",
            "top_right",
            "right",
            "bottom_right",
            "bottom_left",
            "left"
        ]

    if is_hex_boundary_maze(maze):
        return [
            "top",
            "bottom",
            "left",
            "right"
        ]

    return [
        "top",
        "bottom",
        "left",
        "right"
    ]


def iter_cells(maze):

    if isinstance(maze, dict):
        return maze.values()

    return (
        cell
        for row in maze
        for cell in row
    )


def cell_count(maze):

    if isinstance(maze, dict):
        return len(maze)

    return (
        len(maze)
        * len(maze[0])
    )