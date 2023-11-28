class Turn:
    def __init__(self):
        self.turn = 1

    def pass_turn(self):
        self.turn += 1

    def which_player(self):
        if self.turn % 2 == 0:
            return "Black"
        elif not (self.turn % 2 == 0):
            return "White"
        else:
            return False
