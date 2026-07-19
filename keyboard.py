'''from st_keyup import st_keyup


class Keyboard:

    def __init__(self):
        self.last_key = ""

    def listen(self):

        key = st_keyup(
            "Click here and then use the Arrow Keys",
            key="maze_keyboard"
        )

        if key is None:
            return None

        key = key.lower()

        if key == "arrowup":
            return "UP"

        elif key == "arrowdown":
            return "DOWN"

        elif key == "arrowleft":
            return "LEFT"

        elif key == "arrowright":
            return "RIGHT"

        return None
  
from st_keyup import st_keyup
import streamlit as st


class Keyboard:

    def listen(self):

        key = st_keyup(
            "Click here and press any key",
            key="maze_keyboard"
        )

        st.write("Received:", repr(key))

        return None

        '''