import streamlit as st
#from maze.generator import MazeGenerator
#from visualization.draw_maze import MazeDrawer
#from game.player import Player
from generator import MazeGenerator
from triangle_generator import TriangleMazeGenerator
from hex_generator import HexMazeGenerator
from circle_generator import CircleMazeGenerator
from draw_maze import MazeDrawer, TriangleMazeDrawer, HexMazeDrawer, CircleMazeDrawer
from maze_utils import is_circle_maze, is_hex_maze, is_triangle_maze
from player import Player
from controler import GameController
from dfs import DFS
from ucs import UCS
import time
from ai import AIAgent
from astart import AStar
from greedy import Greedy
from bidirectional import BidirectionalSearch
from visualization import (
    compare_algorithms,
    show_table,
    plot_path,
    plot_nodes,
    plot_time,
    plot_pie,
    show_best,
)
import inspect

#st.write(inspect.getfile(MazeDrawer))

from bfs import BFS
from maze_component import maze_component

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Maze Runner",
    page_icon="🧩",
    layout="wide"
)

# ==========================================
# Title
# ==========================================

st.title("🧩 Maze Runner")
st.markdown("### AI Powered Maze Solving and Visualization")

st.divider()

# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("Maze Settings")

maze_shape = st.sidebar.selectbox(
    "Maze Shape",
    ("Square", "Triangle", "Hexagon", "Circle")
)

if maze_shape == "Square":
    maze_rows = st.sidebar.slider("Rows", min_value=5, max_value=30, value=15)
    maze_cols = st.sidebar.slider("Columns", min_value=5, max_value=30, value=15)
elif maze_shape == "Triangle":
    triangle_size = st.sidebar.slider("Size (rows)", min_value=4, max_value=25, value=12)
elif maze_shape == "Hexagon":
    hex_rows = st.sidebar.slider("Rows", min_value=4, max_value=20, value=10, key="hex_rows")
    hex_cols = st.sidebar.slider("Columns", min_value=4, max_value=20, value=10, key="hex_cols")
else:
    circle_rings = st.sidebar.slider("Rings", min_value=3, max_value=18, value=8)
    circle_sectors = st.sidebar.slider("Sectors", min_value=8, max_value=24, value=16)

def build_maze():
    """Create a new maze matching the selected shape."""
    if maze_shape == "Square":
        return MazeGenerator(maze_rows, maze_cols).generate()
    if maze_shape == "Triangle":
        return TriangleMazeGenerator(triangle_size).generate()
    if maze_shape == "Hexagon":
        return HexMazeGenerator(hex_rows, hex_cols).generate()
    return CircleMazeGenerator(circle_rings, circle_sectors).generate()

generate = st.sidebar.button("Generate New Maze")

# Track everything that should force a fresh maze: the shape itself
# plus whatever size parameters apply to that shape.
if maze_shape == "Square":
    maze_params = (maze_shape, maze_rows, maze_cols)
elif maze_shape == "Triangle":
    maze_params = (maze_shape, triangle_size)
elif maze_shape == "Hexagon":
    maze_params = (maze_shape, hex_rows, hex_cols)
else:
    maze_params = (maze_shape, circle_rings, circle_sectors)

# Create a maze the first time the app runs, or if the shape/size changed
if (
    "maze" not in st.session_state
    or st.session_state.get("maze_params") != maze_params
):

    maze = build_maze()

    st.session_state["maze"] = maze
    st.session_state["player"] = Player(maze)
    st.session_state["maze_shape"] = maze_shape
    st.session_state["maze_params"] = maze_params
    st.session_state["solution_path"] = None

# ==========================================
# Generate Maze
# ==========================================

if generate:

    maze = build_maze()

    st.session_state["maze"] = maze
    st.session_state["player"] = Player(maze)
    st.session_state["maze_shape"] = maze_shape
    st.session_state["maze_params"] = maze_params
    st.session_state["solution_path"] = None

    st.success("Maze Generated Successfully!")
# ==========================================
# Display Maze Placeholder
# ==========================================

st.subheader("Maze")
st.markdown(
    """
    <style>
    /* Preserve the maze aspect ratio and keep it inside the viewport. */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    [data-testid="stImage"] img {
        width: auto !important;
        height: auto !important;
        max-width: 100% !important;
        max-height: 45vh !important;
        object-fit: contain !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_drawer_class(maze):
    if is_triangle_maze(maze):
        return TriangleMazeDrawer
    if is_hex_maze(maze):
        return HexMazeDrawer
    if is_circle_maze(maze):
        return CircleMazeDrawer
    return MazeDrawer


def compute_cell_size(maze):
    if is_triangle_maze(maze):
        size = max(row for row, _ in maze) + 1
        return max(12, min(28, 420 // max(1, size)))
    if is_hex_maze(maze):
        rows = max(row for row, _ in maze) + 1
        cols = max(col for _, col in maze) + 1
        return max(12, min(25, 360 // max(1, rows), 620 // max(1, cols)))
    if is_circle_maze(maze):
        rings = max(row for row, _ in maze) + 1
        return max(12, min(24, 210 // max(1, rings)))
    return max(12, min(28, 420 // max(len(maze), len(maze[0]))))

if "maze" in st.session_state:
    cell_size = compute_cell_size(st.session_state["maze"])
    drawer = get_drawer_class(st.session_state["maze"])(
    st.session_state["maze"],
    cell_size=cell_size,
    player=st.session_state["player"],
    path=st.session_state.get("solution_path")
)

    
    image = drawer.draw()

    st.image(
        image,
        channels="BGR",
        width="content"
    )

else:

    st.info("Click 'Generate New Maze' to create a maze.")

st.divider()

# ==========================================
# Choose Mode
# ==========================================

st.subheader("Choose Mode")

mode = st.radio(
    "",
    (
        "🎮 Solve Manually",
        "🤖 AI Solve"
    ),
    horizontal=True
)

# ==========================================
# Manual Mode
# ==========================================

# ==========================================
# Manual Mode
# ==========================================

if mode == "🎮 Solve Manually":

    st.success("Manual Mode Selected")

    controller = GameController(
        st.session_state["player"]
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎮 Controls")
    control_mode = st.sidebar.radio(
        "Control method",
        ("Keyboard (Arrow keys / WASD)", "On-screen buttons"),
        key="control_method",
    )

    if control_mode == "Keyboard (Arrow keys / WASD)":
        st.sidebar.caption("Hex maze: W/A/S/D plus Q (northeast) and Z (southwest)." if is_hex_maze(st.session_state["maze"]) else "Keyboard mode is active. Arrow keys and WASD move the player.")

        # The component restores focus after each Streamlit rerun, so a key
        # press moves one cell without requiring another click.
        keyboard_input = maze_component()
        if isinstance(keyboard_input, dict):
            direction = keyboard_input.get("direction")
            event_id = keyboard_input.get("event_id")
            if (
                direction in {"UP", "DOWN", "LEFT", "RIGHT", "NE", "SW"}
                and event_id != st.session_state.get("last_keyboard_event")
            ):
                st.session_state["last_keyboard_event"] = event_id
                controller.move(direction)
                st.rerun()

        if st.sidebar.button("Reset maze", key="keyboard_reset"):
            st.session_state["player"].reset()
            st.rerun()

    else:
        st.sidebar.caption("Hex mazes also use ↗️ and ↙️ for their extra exits." if is_hex_maze(st.session_state["maze"]) else "Use the on-screen arrow buttons to move.")
        if is_hex_maze(st.session_state["maze"]):
            d1, d2 = st.sidebar.columns(2)
            with d1:
                if st.button("↗️", key="north_east"):
                    controller.move("NE")
                    st.rerun()
            with d2:
                if st.button("↙️", key="south_west"):
                    controller.move("SW")
                    st.rerun()

        c1, c2, c3 = st.sidebar.columns(3)

        with c2:
            if st.button("⬆️", key="up"):
                controller.move("UP")
                st.rerun()

        c1, c2, c3 = st.sidebar.columns(3)

        with c1:
            if st.button("⬅️", key="left"):
                controller.move("LEFT")
                st.rerun()

        with c2:
            if st.button("🔄", key="reset"):
                st.session_state["player"].reset()
                st.rerun()

        with c3:
            if st.button("➡️", key="right"):
                controller.move("RIGHT")
                st.rerun()

        c1, c2, c3 = st.sidebar.columns(3)

        with c2:
            if st.button("⬇️", key="down"):
                controller.move("DOWN")
                st.rerun()
    if st.session_state["player"].reached_goal():
        st.balloons()
        st.success("🎉 Congratulations!")
# ==========================================
# AI Mode
# ==========================================

else:

    st.success("AI Mode Selected")

    ai_mode = st.radio(
        "Choose AI Mode",
        (
            "Agent Automatic",
            "Solve Using Algorithms"
        )
    )

    # --------------------------------------

    if ai_mode == "Agent Automatic":

     st.write("The AI Agent will automatically choose the best algorithm.")

     if st.button("Start Agent"):

        agent = AIAgent(st.session_state["maze"])

        path, explored, metrics, analysis = agent.solve()

        placeholder = st.empty()

        st.subheader("Maze Analysis")

        for key, value in analysis.items():

             if key != "Rules":
                st.write(f"**{key}:** {value}")

        st.subheader("Decision Rules")

        for rule, result in analysis["Rules"].items():

            if result:
                st.success(f"✓ {rule}")
            else:
                st.error(f"✗ {rule}")

        st.subheader("Performance Metrics")

        for key, value in metrics.items():
            st.write(f"**{key}:** {value}")

        # Animate explored nodes
        for i in range(len(explored)):

            drawer = get_drawer_class(st.session_state["maze"])(
                st.session_state["maze"],
                cell_size=cell_size,
                explored=explored[:i+1]
            )

            placeholder.image(
                drawer.draw(),
                channels="BGR",
                width="content"
            )

            time.sleep(0.03)

        # Draw final path
        drawer = get_drawer_class(st.session_state["maze"])(
            st.session_state["maze"],
            cell_size=cell_size,
            path=path
        )

        placeholder.image(
            drawer.draw(),
            channels="BGR",
            width="content"
        )

        st.success("Maze Solved!")

        st.subheader("AI Decision")

        st.write(f"**Selected Algorithm:** {analysis['Selected Algorithm']}")
        st.write(f"**Difficulty:** {analysis['Difficulty']}")
        st.write(f"**Maze Density:** {analysis['Maze Density']}")
        st.write(f"**Dead Ends:** {analysis['Dead Ends']}")
        st.write(f"**Branching Factor:** {analysis['Branching Factor']}")
        st.write(f"**Goal Distance:** {analysis['Goal Distance']}")

        st.subheader("Performance Metrics")

        for key, value in metrics.items():
            st.write(f"**{key}:** {value}")

    # --------------------------------------

    else:

        st.subheader("Select Algorithm")

        algorithm = st.selectbox(
            "",
            (
                "Breadth First Search (BFS)",
                "Depth First Search (DFS)",
                "Uniform Cost Search (UCS)",
                "Greedy Best First Search",
                "A* Search",
                "Bidirectional Search"
            )
        )

        if st.button("Compare All Algorithms"):
            comparison_df = compare_algorithms(st.session_state["maze"])
            if not comparison_df.empty:
                show_table(comparison_df)
                plot_path(comparison_df)
                plot_nodes(comparison_df)
                plot_time(comparison_df)
                plot_pie(comparison_df)
                show_best(comparison_df)

        if st.button("Run Algorithm"):

            # -----------------------------
            # Select Algorithm
            # -----------------------------

            if algorithm == "Breadth First Search (BFS)":
                solver = BFS(st.session_state["maze"])

            elif algorithm == "Depth First Search (DFS)":
                solver = DFS(st.session_state["maze"])

            elif algorithm == "Uniform Cost Search (UCS)":
                solver = UCS(st.session_state["maze"])

            elif algorithm == "Greedy Best First Search":
                solver = Greedy(st.session_state["maze"])

            elif algorithm == "A* Search":
                solver = AStar(st.session_state["maze"])

            elif algorithm == "Bidirectional Search":
                solver = BidirectionalSearch(st.session_state["maze"])

            else:
                st.warning("Algorithm not implemented yet.")
                st.stop()

            # -----------------------------
            # Solve Maze
            # -----------------------------

            path, explored = solver.solve()

            # -----------------------------
            # Animation Placeholder
            # -----------------------------

            placeholder = st.empty()

            # -----------------------------
            # Animate Search
            # -----------------------------

            for i in range(len(explored)):

                drawer = get_drawer_class(st.session_state["maze"])(
                    st.session_state["maze"],
                    cell_size=cell_size,
                    explored=explored[:i+1],
                )

                placeholder.image(
                    drawer.draw(),
                    channels="BGR",
                    width="content",
                )

                time.sleep(0.03)

            # -----------------------------
            # Draw Final Path
            # -----------------------------

            drawer = get_drawer_class(st.session_state["maze"])(
                st.session_state["maze"],
                cell_size=cell_size,
                path=path,
            )

            placeholder.image(
                drawer.draw(),
                channels="BGR",
                width="content",
            )

            st.success("Maze Solved!")

            c1, c2 = st.columns(2)

            c1.metric("Path Length", len(path))
            c2.metric("Nodes Explored", len(explored))