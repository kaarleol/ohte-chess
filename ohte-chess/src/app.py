from services.legal_moves import LegalMove


class App:
    def __init__(self, board, turn, io):
        self.board = board
        self.turn = turn
        self.io = io
        self.legality = LegalMove(self.board)

        self.move_from = None
        self.move_to = None

    def run(self):
        while True:
            self.board.draw_board()
            current_player = self.turn.which_player()
            self.io.write(f"{current_player}'s move")

            did_exit = False
            while True:
                move = self.io.read(
                    "Give the square you would like to move from (eg. a1):")

                if move == "exit":
                    did_exit = True
                    break

                val = self.legality.correct_player(current_player, move)
                if val is True:
                    self.move_from = move
                    break
                self.io.write(val[1])

            while True:
                if did_exit is True:
                    break
                move = self.io.read(
                    "Give the square you would like to move to (eg. a4):")

                if move == "exit":
                    did_exit = True
                    break
                val = self.legality.legal_pos(move)
                if val[0] is not False:
                    self.move_to = move
                    break
                self.io.write(val[1])

            if did_exit is True:
                break

            val = self.board.move_piece(self.move_from, self.move_to)
            if val is not True:
                self.io.write(val[1])
                break
            self.turn.pass_turn()
