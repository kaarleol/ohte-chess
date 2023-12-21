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
            self.legality.current_turn = current_player
            self.io.write(f"{current_player}'s move")
            legal_moves = []

            did_exit = False
            did_cancel = False
            val = self.legality.check_checker()
            if val is True:
                self.io.write('Check!')

            while True:
                move = self.io.read(
                    "Give the square you would like to move from:")

                if move == "exit":
                    did_exit = True
                    break

                val = self.legality.correct_player(current_player, move)
                if val is True:
                    legal_moves = self.legality.legal_moves(move)
                    print(legal_moves)
                else:
                    self.io.write(val[1])

                if len(legal_moves) >= 1:
                    self.move_from = move
                    break
                else:
                    self.io.write('Piece has no legal moves')

            while True:
                if did_exit is True:
                    break
                move = self.io.read(
                    "Give the square you would like to move to:")

                if move == "exit":
                    did_exit = True
                    break
                if move == 'cancel':
                    did_cancel = True
                    break

                val = self.legality.legal_pos(move)
                if val[0] is not False:
                    if move in legal_moves:
                        self.move_to = move
                        break
                    else:
                        self.io.write('Not a legal move for that piece')
                self.io.write(val[1])

            if did_exit is True:
                break

            if did_cancel is False:
                val = self.legality.log_move(self.move_from, self.move_to)
                if val is not True:
                    self.io.write(val[1])
                    return
                val = self.board.move_piece(self.move_from, self.move_to, current_player, False)
                if val is not True:
                    self.io.write(val[1])
                    break
                val = self.legality.would_be_in_check()
                if val is True:
                    self.io.write('Not a legal move due to check')
                    self.board.go_back()
                    self.legality.go_back_log()
                else:
                    self.turn.pass_turn()
