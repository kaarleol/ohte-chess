class LegalMove:
    def __init__(self, board):
        self.board = board

    def legal_pos(self, move):
        if not len(move) == 2:
            return False, "Err: not a legal position"
        if not move[0].lower() in "abcdefgh":
            return False, "Err: not a legal position"
        if not move[1].isdigit():
            return False, "Err: not a legal position"
        if not (int(move[1]) >= 0 and int(move[1]) <= 8):
            return False, "Err: not a legal position"
        return move[0], int(move[1])

    def correct_player(self, player, move):
        if player is None or move == '':
            return False, "Err: missing player or move"

        move = self.legal_pos(move)
        if move[0] is False:
            return move

        if self.board.piece_owner(move[0], move[1]) == player:
            return True

        return False, "Err: wrong player's piece or empty square"
