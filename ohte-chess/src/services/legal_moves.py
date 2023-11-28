class Legal_move:
    def __init__(self, board):
        self.board = board

    def legal_pos(self, move):
        if not len(move) == 2:
            return False
        elif not move[0].lower() in "abcdefgh":
            return False
        elif not move[1].isdigit():
            return False
        elif not (int(move[1]) >= 0 and int(move[1]) <= 8):
            return False
        else:
            return move[0], int(move[1])

    def correct_player(self, player, move):
        if not (player and move):
            return False

        move = self.legal_pos(move)
        if not move:
            return False

        print(f"thishappened, {move[0]}, {move[1]}")

        if self.board.piece_owner(move[0], move[1]) == player:
            return True
        else:
            return False
