class LegalMove:
    def __init__(self, board):
        self.board = board
        self.previous_move = {'move_from':'', 'move_to':'', 'moved_piece':'',
                               'takes':None, 'pawn_double_move':False, 
                               'player':None,
                               'white_king_moved':False,
                               'a1_rook_moved':False,
                               'h1_rook_moved':False,
                               'black_king_moved':False, 
                               'a8_rook_moved':False, 
                               'h8_rook_moved':False }
        self.previous_previous_move = {'move_from':'', 'move_to':'', 'moved_piece':'',
                               'takes':None, 'pawn_double_move':False,
                               'player':None,
                               'white_king_moved':False, 
                               'a1_rook_moved':False, 
                               'h1_rook_moved':False,
                               'black_king_moved':False, 
                               'a8_rook_moved':False, 
                               'h8_rook_moved':False }
        self.white_king_location = 'e1'
        self.black_king_location = 'e8'
        self.current_turn = 'White'

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
        #en passant
        if self.previous_move['pawn_double_move'] is True and row == 5:
            move_right = self.board.move_to_direction(move_from, 'right')
            if move_right == self.previous_move['move_to']:
                legal_moves.append(self.board.move_to_direction(move_right, 'up'))
            move_left = self.board.move_to_direction(move_from, 'left')
            if move_left == self.previous_move['move_to']:
                legal_moves.append(self.board.move_to_direction(move_left, 'up'))

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
        #en passant
        if self.previous_move['pawn_double_move'] is True and row == 5:
            move_right = self.board.move_to_direction(move_from, 'right')
            if move_right == self.previous_move['move_to']:
                legal_moves.append(self.board.move_to_direction(move_right, 'down'))
            move_left = self.board.move_to_direction(move_from, 'left')
            if move_left == self.previous_move['move_to']:
                legal_moves.append(self.board.move_to_direction(move_left, 'down'))

        return legal_moves

    def knight_legal_moves(self, move_from):
        piece_color  = self.current_turn
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
                self.board.move_to_direction(move_from, 'right'), 'right'), 'up'))
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
        piece_color  = self.current_turn
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
        piece_color  = self.current_turn
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
        piece_color  = self.current_turn
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

    def square_under_threat(self, square, player=None):
        c, r = self.board.break_move(square)
        val = self.board.location_translator(c, r)
        if val is not None and player is None:
            if val.islower():
                current_player = 'Black'
            else:
                current_player = 'White'
        elif player is not None:
            current_player = player
        else:
            current_player = self.current_turn

        possible_threats = []
        #check diagonals for enemy queen or bishop
        diagonal_threats = self.bishop_legal_moves(square)
        for i in diagonal_threats:
            c, r = self.board.break_move(i)
            piece = self.board.location_translator(c, r)
            if piece is not None:
                if piece.isupper():
                    owner = 'White'
                else: 
                    owner = 'Black'

                if (piece.lower() == 'q' or piece.lower() == 'b') and owner != current_player:
                    possible_threats.append(i)
        #check rows & columns for enemy rook or queen
        rooklike_threats = self.rook_legal_moves(square)
        for i in rooklike_threats:
            c, r = self.board.break_move(i)
            piece = self.board.location_translator(c, r)
            if piece is not None:
                if piece.isupper():
                    owner = 'White'
                else:
                    owner = 'Black'

                if (piece.lower() == 'q' or piece.lower() == 'r') and owner != current_player:
                    possible_threats.append(i)
        #check for enemy knights
        knight_threats = self.knight_legal_moves(square)
        for i in knight_threats:
            c, r = self.board.break_move(i)
            piece = self.board.location_translator(c, r)
            if piece is not None:
                if piece.isupper():
                    owner = 'White'
                else:
                    owner = 'Black'

                if piece.lower() == 'n' and owner != current_player:
                    possible_threats.append(i)
        #check for enemy pawns
        pawn_threats = []
        if current_player == 'White':
            pawn_threats.append(self.board.move_to_direction(
                self.board.move_to_direction(square, 'right'), 'up'))
            pawn_threats.append(self.board.move_to_direction(
                self.board.move_to_direction(square, 'left'), 'up'))
        else:
            pawn_threats.append(self.board.move_to_direction(
                self.board.move_to_direction(square, 'right'), 'down'))
            pawn_threats.append(self.board.move_to_direction(
                self.board.move_to_direction(square, 'left'), 'down'))
        for i in pawn_threats:
            c, r = self.board.break_move(i)
            piece = self.board.location_translator(c, r)
            if piece is not None:
                if piece.isupper():
                    owner = 'White'
                else:
                    owner = 'Black'

                if piece.lower() == 'p' and owner != current_player:
                    possible_threats.append(i)
        return possible_threats

    def check_checker(self):
        if self.check_checker_white() or self.check_checker_black():
            return True
        return False

    def would_be_in_check(self):
        if self.current_turn == 'White':
            return self.check_checker_white()
        return self.check_checker_black()

    def check_checker_white(self):
        return len(self.square_under_threat(self.white_king_location)) > 0

    def check_checker_black(self):
        return len(self.square_under_threat(self.black_king_location)) > 0

    #the following is a bit complicated so some explanations
    def mate_checker(self):
        if self.current_turn == 'Black':
            threats = self.square_under_threat(self.black_king_location)
            king_moves = self.king_legal_moves(self.black_king_location)
            king_location = self.black_king_location
            threatening_player = "White"
        if self.current_turn == 'White':
            threats = self.square_under_threat(self.white_king_location)
            king_moves = self.king_legal_moves(self.white_king_location)
            king_location = self.white_king_location
            threatening_player = 'Black'
        #check if king can escape
        for i in king_moves:
            if not self.square_under_threat(i, self.current_turn):
                return False
        #just making sure there are no duplicates
        unique_threats = []
        for item in threats:
            if item not in unique_threats:
                unique_threats.append(item)
        #check if the attacker can be taken
        #if there are more than one threat(double check) taking won't help
        if len(unique_threats) == 1:
            threats = self.square_under_threat(unique_threats[0])
            for i in threats:
                if self.can_piece_move(i, unique_threats[0]):
                    return False
        #check if the treats are blockable (not a knight or multiple attackers)
        if len(unique_threats) == 1:
            #couldn't take and cannot block a knight so mate
            if unique_threats[0].lower() == 'n':
                return True
            #squares that could remove the check if blocked
            possible_blockable_squares = self.queen_legal_moves(king_location)
            for i in possible_blockable_squares:
                #can one of your pieces make it to that square
                can_a_piece_block = self.square_under_threat(i, threatening_player)
                #can the piece move or is it pinned
                for j in can_a_piece_block:
                    #if one move is found, not a mate
                    if self.can_piece_move(j, i):
                        return False
        return True

    #checks if a piece could move to some square without you being in check after
    def can_piece_move(self, move_from, move_to):
        self.board.move_piece(move_from, move_to, self.current_turn, True)
        if self.current_turn == 'White':
            val = self.check_checker_white()
            self.board.go_back()
            return not val
        if self.current_turn == 'Black':
            val = self.check_checker_white()
            self.board.go_back()
            return not val


    def log_move(self, move_from, move_to):
        self.previous_previous_move = self.previous_move
        self.previous_move['move_from'] = move_from
        self.previous_move['move_to'] = move_to
        column_from, row_from = self.board.break_move(move_from)
        column_to, row_to = self.board.break_move(move_to)
        moved_piece = self.board.location_translator(column_from, row_from)
        if moved_piece:
            #check for double pawn move for en passant
            if moved_piece == 'P':
                if self.board.move_to_direction(self.board.move_to_direction(
                    move_from, 'up'), 'up') == move_to:
                    self.previous_move['pawn_double_move']=True
            elif moved_piece == 'p':
                if self.board.move_to_direction(self.board.move_to_direction(
                    move_from, 'down'), 'down') == move_to:
                    self.previous_move['pawn_double_move']=True
            else:
                self.previous_move['pawn_double_move']=False
            #save if king or rook moved to prevent castling in the future
            if moved_piece == 'K':
                self.previous_move['white_king_moved'] = True
                self.white_king_location = move_to
            if moved_piece == 'k':
                self.previous_move['black_king_moved'] = True
                self.black_king_location = move_to
            if moved_piece == 'R' and move_from.lower() == 'a1':
                self.previous_move['a1_rook_moved'] = True
            if moved_piece == 'R' and move_from.lower() == 'h1':
                self.previous_move['h1_rook_moved'] = True
            if moved_piece == 'r' and move_from.lower() == 'a8':
                self.previous_move['a8_rook_moved'] = True
            if moved_piece == 'r' and move_from.lower() == 'h8':
                self.previous_move['h8_rook_moved'] = True
            self.previous_move['moved_piece'] = moved_piece
        else:
            return False, "Please report this error - everything is wrong"
        self.previous_move['takes'] = self.board.location_translator(column_to, row_to)
        self.previous_move['player'] = self.current_turn
        return True

    def go_back_log(self):
        self.previous_move = self.previous_previous_move
