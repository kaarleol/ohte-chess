class Turn:
    '''
    Class for keeping the turn and current player 

    Attributes:
        turn (int): Turn count
        
    Methods:
        pass_turn(): Ticks the turn counter by one
        which_player(): Returns the current player 
    '''
    def __init__(self):
        self.turn = 1

    def pass_turn(self):
        '''
        Pass turn
        '''
        self.turn += 1

    def which_player(self):
        '''
        Returns current player basedd on the turn count
        '''
        if self.turn % 2 == 0:
            return "Black"
        if self.turn % 2 != 0:
            return "White"
        return False, "Err: something is definitely not right"
