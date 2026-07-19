from streamlit_javascript import st_javascript


class KeyboardHandler:

    def get_key(self):

        key = st_javascript(
            """
            await new Promise(resolve => {

                function listener(event) {

                    if (
                        event.key === "ArrowUp" ||
                        event.key === "ArrowDown" ||
                        event.key === "ArrowLeft" ||
                        event.key === "ArrowRight"
                    ) {

                        document.removeEventListener("keydown", listener);
                        resolve(event.key);
                    }
                }

                document.addEventListener("keydown", listener);

            });
            """
        )

        if key == "ArrowUp":
            return "UP"

        if key == "ArrowDown":
            return "DOWN"

        if key == "ArrowLeft":
            return "LEFT"

        if key == "ArrowRight":
            return "RIGHT"

        return None