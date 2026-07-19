class GameController:

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
        if direction in moves:
            moves[direction]()
        return self.player.get_position()
