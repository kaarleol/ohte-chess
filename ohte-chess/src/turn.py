class Turn:
    def __init__(self):
        self.turn = 1
    
    def pass_turn(self):
        self.turn += 1

    def which_player(self):
        if self.turn % 2 == 0:
            return "black"
        elif not (self.turn % 2 == 0 ):
            return "white"
        else:
            return False