class LegalMove:
    def __init__(self, board):
        self.board = board
        self.previous_move = ''
        self.white_king_moved = False
        self.a1_rook_moved = False
        self.h1_rook_moved = False
        self.black_king_moved = False
        self.a8_rook_moved = False
        self.h8_rook_moved = False

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

    def legal_moves(self, move_from):
        column, row = self.board.break_move(move_from)
        piece = self.board.location_translator(column, row)
        if piece == 'P':
            return self.white_pawn_legal_moves(move_from)
        if piece == 'p':
            return self.black_pawn_legal_moves(move_from)
        if piece.lower() == 'n':
            return self.knight_legal_moves(move_from)
        if piece.lower() == 'b':
            return self.bishop_legal_moves(move_from)
        if piece.lower() == 'r':
            return self.rook_legal_moves(move_from)
        if piece.lower() == 'q':
            return self.queen_legal_moves(move_from)
        if piece.lower() == 'k':
            return self.king_legal_moves(move_from)


    def white_pawn_legal_moves(self, move_from):
        legal_moves = []
        column, row = self.board.break_move(move_from)

        #pawn not moved yet
        if row == 2:
            move_two_squares = self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'up'), 'up')
            if move_two_squares[0] is not False:
                c, r = self.board.break_move(move_two_squares)
                piece_in_front = self.board.location_translator(c, r)
            if piece_in_front is None:
                legal_moves.append(move_two_squares)
        #other cases, first check moving up one
        move_up = self.board.move_to_direction(move_from, 'up')
        if move_up[0] is not False:
            c, r = self.board.break_move(move_up)
            piece_in_front = self.board.location_translator(c, r)
        if piece_in_front is None:
            legal_moves.append(move_up)
        #check takes right (diagonally ofc)
        takes_right = self.board.move_to_direction(
            self.board.move_to_direction(move_from, 'up'), 'right')
        if takes_right[0] is not False:
            c, r = self.board.break_move(takes_right)
            piece_to_the_right = self.board.location_translator(c, r)
            if piece_to_the_right is not None:
                if piece_to_the_right.islower():
                    legal_moves.append(takes_right)
        #check takes left
        takes_left = self.board.move_to_direction(
            self.board.move_to_direction(move_from, 'up'), 'left')
        if takes_left[0] is not False:
            c, r = self.board.break_move(takes_left)
            piece_to_the_left = self.board.location_translator(c, r)
            if piece_to_the_left is not None:
                if piece_to_the_left.islower():
                    legal_moves.append(takes_left)
        #en passant, promotion tba

        return legal_moves

    def black_pawn_legal_moves(self, move_from):
        legal_moves = []
        column, row = self.board.break_move(move_from)

        #pawn not moved yet
        if row == 7:
            move_two_squares = self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'down'), 'down')
            if move_two_squares[0] is not False:
                c, r = self.board.break_move(move_two_squares)
                piece_in_front = self.board.location_translator(c, r)
            if piece_in_front is None:
                legal_moves.append(move_two_squares)
        #other cases, first check moving up one
        move_down = self.board.move_to_direction(move_from, 'down')
        if move_down[0] is not False:
            c, r = self.board.break_move(move_down)
            piece_in_front = self.board.location_translator(c, r)
        if piece_in_front is None:
            legal_moves.append(move_down)
        #check takes right (diagonally ofc)
        takes_right = self.board.move_to_direction(self.board.move_to_direction(
            move_from, 'down'), 'right')
        if takes_right[0] is not False:
            c, r = self.board.break_move(takes_right)
            piece_to_the_right = self.board.location_translator(c, r)
            if piece_to_the_right is not None:
                if piece_to_the_right.isupper():
                    legal_moves.append(takes_right)
        #check takes left
        takes_left = self.board.move_to_direction(self.board.move_to_direction(
            move_from, 'down'), 'left')
        if takes_left[0] is not False:
            c, r = self.board.break_move(takes_left)
            piece_to_the_left = self.board.location_translator(c, r)
            if piece_to_the_left is not None:
                if piece_to_the_left.isupper():
                    legal_moves.append(takes_left)
        #en passant, promotion tba

        return legal_moves

    def knight_legal_moves(self, move_from):
        column, row = self.board.break_move(move_from)
        piece_color  = self.board.piece_owner(column, row)
        move_tries = []
        legal_moves = []
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'right'), 'up'), 'up'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'left'), 'up'), 'up'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'right'), 'down'), 'down'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'left'), 'down'), 'down'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'right'), 'rigth'), 'up'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'left'), 'left'), 'up'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'right'), 'right'), 'down'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(
                self.board.move_to_direction(move_from, 'left'), 'left'), 'down'))

        for i in move_tries:
            if i[0] is not False:
                c, r = self.board.break_move(i)
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(i)

        return legal_moves

    def bishop_legal_moves(self, move_from):
        column, row = self.board.break_move(move_from)
        piece_color = self.board.piece_owner(column, row)
        legal_moves = []
        current_location = move_from
        #up-right-diagonal
        while True:
            current_location = self.board.move_to_direction(
                self.board.move_to_direction(current_location, 'up'), 'right')
            if current_location[0] is False:
                break
            c, r =self.board.break_move(current_location)
            if self.board.location_translator(c, r) is None:
                legal_moves.append(current_location)
            else:
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(current_location)
                    break
                if self.board.piece_owner(c, r) is piece_color:
                    break
        current_location = move_from
        #up-left-diagonal
        while True:
            current_location = self.board.move_to_direction(
                self.board.move_to_direction(current_location, 'up'), 'left')
            if current_location[0] is False:
                break
            c, r =self.board.break_move(current_location)
            if self.board.location_translator(c, r) is None:
                legal_moves.append(current_location)
            else:
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(current_location)
                    break
                if self.board.piece_owner(c, r) is piece_color:
                    break
        current_location = move_from
        #down-right-diagonal
        while True:
            current_location = self.board.move_to_direction(
                self.board.move_to_direction(current_location, 'down'), 'right')
            if current_location[0] is False:
                break
            c, r =self.board.break_move(current_location)
            if self.board.location_translator(c, r) is None:
                legal_moves.append(current_location)
            else:
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(current_location)
                    break
                if self.board.piece_owner(c, r) is piece_color:
                    break
        current_location = move_from
        #down-left-diagonal
        while True:
            current_location = self.board.move_to_direction(
                self.board.move_to_direction(current_location, 'down'), 'left')
            if current_location[0] is False:
                break
            c, r =self.board.break_move(current_location)
            if self.board.location_translator(c, r) is None:
                legal_moves.append(current_location)
            else:
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(current_location)
                    break
                if self.board.piece_owner(c, r) is piece_color:
                    break

        return legal_moves

    def rook_legal_moves(self, move_from):
        column, row = self.board.break_move(move_from)
        piece_color = self.board.piece_owner(column, row)
        legal_moves = []
        current_location = move_from
        #right
        while True:
            current_location = self.board.move_to_direction(current_location, 'right')
            if current_location[0] is False:
                break
            c, r =self.board.break_move(current_location)
            if self.board.location_translator(c, r) is None:
                legal_moves.append(current_location)
            else:
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(current_location)
                    break
                if self.board.piece_owner(c, r) is piece_color:
                    break
        current_location = move_from
        #left
        while True:
            current_location = self.board.move_to_direction(current_location, 'left')
            if current_location[0] is False:
                break
            c, r =self.board.break_move(current_location)
            if self.board.location_translator(c, r) is None:
                legal_moves.append(current_location)
            else:
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(current_location)
                    break
                if self.board.piece_owner(c, r) is piece_color:
                    break
        current_location = move_from
        #up
        while True:
            current_location = self.board.move_to_direction(current_location, 'up')
            if current_location[0] is False:
                break
            c, r =self.board.break_move(current_location)
            if self.board.location_translator(c, r) is None:
                legal_moves.append(current_location)
            else:
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(current_location)
                    break
                if self.board.piece_owner(c, r) is piece_color:
                    break
        current_location = move_from
        #down
        while True:
            current_location = self.board.move_to_direction(current_location, 'down')
            if current_location[0] is False:
                break
            c, r =self.board.break_move(current_location)
            if self.board.location_translator(c, r) is None:
                legal_moves.append(current_location)
            else:
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(current_location)
                    break
                if self.board.piece_owner(c, r) is piece_color:
                    break

        return legal_moves

    def queen_legal_moves(self, move_from):
        l1 = self.bishop_legal_moves(move_from)
        l2 = self.rook_legal_moves(move_from)

        return l1 + l2

    def king_legal_moves(self, move_from):
        column, row = self.board.break_move(move_from)
        piece_color  = self.board.piece_owner(column, row)
        move_tries = []
        legal_moves = []
        move_tries.append(self.board.move_to_direction(move_from, 'up'))
        move_tries.append(self.board.move_to_direction(move_from, 'down'))
        move_tries.append(self.board.move_to_direction(move_from, 'right'))
        move_tries.append(self.board.move_to_direction(move_from, 'left'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(move_from, 'rigth'), 'up'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(move_from, 'left'), 'up'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(move_from, 'right'), 'down'))
        move_tries.append(self.board.move_to_direction(
            self.board.move_to_direction(move_from, 'left'), 'down'))

        for i in move_tries:
            if i[0] is not False:
                c, r = self.board.break_move(i)
                if self.board.piece_owner(c, r) is not piece_color:
                    legal_moves.append(i)

        return legal_moves
