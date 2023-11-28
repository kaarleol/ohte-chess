from services.legal_moves import Legal_move

class App:
    def __init__(self, board, turn, io):
        self.board = board
        self.turn = turn
        self.io = io
        self.legality = Legal_move(self.board)

    
    def run(self):
        while True:
            self.board.draw_board()
            self.currentPlayer = self.turn.which_player()
            self.io.write(f"{self.currentPlayer}'s move")
            self.move = self.io.read("Give the square you would like to move from (eg. a1):")

            if self.move == "exit":
                break
            self.io.write(f"{self.currentPlayer}, {move[0]}, {move[1]}")
            if self.legality.correct_player(self.currentPlayer, move):
                self.io.write("yay this works")
            else: 
                self.io.write("nope wrong playa")






            self.turn.pass_turn()
