import time

from bfs import BFS
from dfs import DFS
from ucs import UCS
from greedy import Greedy
from astart import AStar
from bidirectional import BidirectionalSearch
from maze_utils import (
    maze_size,
    start_goal,
    wall_keys,
    iter_cells,
    cell_count,
    heuristic as _heuristic
)


class AIAgent:

    def __init__(self, maze):

        self.maze = maze

        self.rows, self.cols = maze_size(maze)
        self.cells = cell_count(maze)

    # ----------------------------------------------------
    # Count Walls
    # ----------------------------------------------------

    def maze_density(self):

        keys = wall_keys(self.maze)

        walls = sum(
            sum(cell[k] for k in keys)
            for cell in iter_cells(self.maze)
        )

        maximum = self.cells * len(keys)

        return round(walls / maximum, 2)

    # ----------------------------------------------------
    # Dead Ends
    # ----------------------------------------------------

    def dead_ends(self):

        keys = wall_keys(self.maze)
        count = 0

        for cell in iter_cells(self.maze):

            openings = sum(1 for k in keys if not cell[k])

            if openings == 1:
                count += 1

        return count

    # ----------------------------------------------------
    # Branching Factor
    # ----------------------------------------------------

    def branching_factor(self):

        keys = wall_keys(self.maze)
        total = 0

        for cell in iter_cells(self.maze):
            total += sum(1 for k in keys if not cell[k])

        return round(total / self.cells, 2)

    # ----------------------------------------------------
    # Corridor Length (Approx.)
    # ----------------------------------------------------

    def corridor_length(self):

        return round(max(2, self.branching_factor() * 2), 2)

    # ----------------------------------------------------
    # Manhattan Distance
    # ----------------------------------------------------

    def goal_distance(self):

        start, goal = start_goal(self.maze)
        return _heuristic(start, goal)

    # ----------------------------------------------------
    # Difficulty
    # ----------------------------------------------------

    def difficulty(self):

        score = 0

        if self.cells > 400:
            score += 1

        if self.maze_density() > 0.60:
            score += 1

        if self.dead_ends() > self.cells * 0.20:
            score += 1

        if self.branching_factor() > 2:
            score += 1

        if score <= 1:
            return "Easy"

        elif score == 2:
            return "Medium"

        else:
            return "Hard"

    # ----------------------------------------------------
    # Rule Evaluation
    # ----------------------------------------------------

    def rules(self):

        return {

            "Rule 1 (Small Maze)": self.cells < 150,

            "Rule 2 (Many Dead Ends)":
                self.dead_ends() > self.cells * 0.20,

            "Rule 3 (Large Maze)":
                self.cells > 500,

            "Rule 4 (Open Maze)":
                self.branching_factor() > 2.5,

            "Rule 5 (Shortest Path Required)": True,

            "Rule 6 (Weighted Maze)": False
        }

    # ----------------------------------------------------
    # Algorithm Selection
    # ----------------------------------------------------

    def choose_algorithm(self):

        r = self.rules()

        if r["Rule 3 (Large Maze)"]:
            return "Bidirectional Search"

        if r["Rule 2 (Many Dead Ends)"]:
            return "A* Search"

        if r["Rule 1 (Small Maze)"]:
            return "Breadth First Search"

        if r["Rule 4 (Open Maze)"]:
            return "Greedy Best First Search"

        return "A* Search"

    # ----------------------------------------------------
    # Run Selected Algorithm
    # ----------------------------------------------------

    def solve(self):

        algorithm = self.choose_algorithm()

        if algorithm == "Breadth First Search":
            solver = BFS(self.maze)

        elif algorithm == "Depth First Search":
            solver = DFS(self.maze)

        elif algorithm == "Uniform Cost Search":
            solver = UCS(self.maze)

        elif algorithm == "Greedy Best First Search":
            solver = Greedy(self.maze)

        elif algorithm == "Bidirectional Search":
            solver = BidirectionalSearch(self.maze)

        else:
            solver = AStar(self.maze)

        start = time.perf_counter()

        path, explored = solver.solve()

        end = time.perf_counter()

        execution = round((end - start) * 1000, 2)

        metrics = {

            "Execution Time": execution,

            "Nodes Explored": len(explored),

            "Path Length": len(path),

            "Memory Usage": len(explored) * 64,

            "Difficulty": self.difficulty(),

            "Search Efficiency":
                round(len(path) / len(explored), 2),

            "Exploration Percentage":
                round((len(explored) / self.cells) * 100, 2),

            "Optimality":
                "Optimal"
                if algorithm in
                [
                    "Breadth First Search",
                    "Uniform Cost Search",
                    "A* Search",
                    "Bidirectional Search"
                ]
                else
                "Non-Optimal"
        }

        analysis = {

            "Rows": self.rows,

            "Columns": self.cols if self.cols is not None else "N/A (triangle maze)",

            "Total Cells": self.cells,

            "Maze Density": self.maze_density(),

            "Dead Ends": self.dead_ends(),

            "Branching Factor": self.branching_factor(),

            "Average Corridor": self.corridor_length(),

            "Goal Distance": self.goal_distance(),

            "Difficulty": self.difficulty(),

            "Rules": self.rules(),

            "Selected Algorithm": algorithm
        }

        return path, explored, metrics, analysis