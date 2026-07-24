class GameController:
    """Handle player movement commands."""

    def __init__(self, player):
        self.player = player

    def move(self, direction):
        direction = direction.upper()

        moves = {
            "UP": self.player.move_up,
            "DOWN": self.player.move_down,
            "LEFT": self.player.move_left,
            "RIGHT": self.player.move_right,
            "NE": self.player.move_north_east,
            "SW": self.player.move_south_west,
        }

        move_function = moves.get(direction)

        if move_function:
            move_function()

        return self.player.get_position()