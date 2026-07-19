import os
import streamlit.components.v1 as components

_component = components.declare_component(
    "maze_component",
    path=os.path.join(os.path.dirname(__file__), "frontend")
)

def maze_component():
    """Render the keyboard listener without serializing maze state."""
    return _component(default=None)