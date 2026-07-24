import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

from bfs import BFS
from dfs import DFS
from ucs import UCS
from greedy import Greedy
from astart import AStar
from bidirectional import BidirectionalSearch


def compare_algorithms(maze):
    algorithms = {
        "BFS": BFS,
        "DFS": DFS,
        "UCS": UCS,
        "Greedy": Greedy,
        "A*": AStar,
        "Bidirectional": BidirectionalSearch,
    }

    results = []

    for name, algo in algorithms.items():
        try:
            solver = algo(maze)
            start = time.time()
            path, explored = solver.solve()
            end = time.time()

            results.append(
                {
                    "Algorithm": name,
                    "Path Length": len(path),
                    "Nodes Explored": len(explored),
                    "Execution Time": round(end - start, 5),
                }
            )
        except Exception as e:
            st.error(f"{name} failed: {e}")

    return pd.DataFrame(results)


def show_table(df):
    st.subheader("📋 Performance Table")
    st.dataframe(df, use_container_width=True)


def plot_path(df):
    st.subheader("📊 Path Length Comparison")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["Algorithm"], df["Path Length"], color="#4b79a1")
    ax.set_ylabel("Path Length")
    ax.set_xlabel("Algorithm")
    ax.set_xticklabels(df["Algorithm"], rotation=30, ha="right")
    st.pyplot(fig)


def plot_nodes(df):
    st.subheader("📊 Nodes Explored")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["Algorithm"], df["Nodes Explored"], color="#a14b4b")
    ax.set_ylabel("Nodes")
    ax.set_xlabel("Algorithm")
    ax.set_xticklabels(df["Algorithm"], rotation=30, ha="right")
    st.pyplot(fig)


def plot_time(df):
    st.subheader("📊 Execution Time")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["Algorithm"], df["Execution Time"], color="#4ba14a")
    ax.set_ylabel("Seconds")
    ax.set_xlabel("Algorithm")
    ax.set_xticklabels(df["Algorithm"], rotation=30, ha="right")
    st.pyplot(fig)


def plot_pie(df):
    st.subheader("🥧 Search Effort Distribution")
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(df["Nodes Explored"], labels=df["Algorithm"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)


def show_best(df):
    best = df.sort_values("Execution Time").iloc[0]
    st.success(
        f"""
🏆 Best Algorithm : {best['Algorithm']}

Execution Time : {best['Execution Time']} sec

Path Length : {best['Path Length']}

Nodes Explored : {best['Nodes Explored']}
"""
    )
