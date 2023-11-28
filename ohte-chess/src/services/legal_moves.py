class LegalMove:
    def __init__(self, board):
        self.board = board

    def legal_pos(self, move):
        if not len(move) == 2:
            return False
        if not move[0].lower() in "abcdefgh":
            return False
        if not move[1].isdigit():
            return False
        if not (int(move[1]) >= 0 and int(move[1]) <= 8):
            return False
        return move[0], int(move[1])

    def correct_player(self, player, move):
        if not (player and move):
            return False

        move = self.legal_pos(move)
        if not move:
            return False

        if self.board.piece_owner(move[0], move[1]) == player:
            return True
        return False
