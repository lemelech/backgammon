class BkgPlayer:
    """abstract class for backgammon player classes"""
    def __init__(self, player_name):
        self.name = player_name

    def offer_move(self, board, turn, dice):
        raise NotImplementedError
