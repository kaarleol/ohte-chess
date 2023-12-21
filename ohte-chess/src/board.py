class Board:
    '''
    A class that remembers the board-state and takes care of moving pieces

    Atrributes:
        io: Some io for drawing the board-state
        previous_move (dict): Remembers the previous move in case the move needs to be reversed
        rows: Boardstate
    
    Methods:
        draw_board(): Draws the board using a helper function and io
        location_translator(): Returns the piece in a given square
        piece_owner(): Return the owner of piece in a given square
        move_piece(): Moves a piece from a square to another and takes care of special moves
        move_to_direction(): Helper function. Returns the anjacent square to direction
        break_move(): Helper function for breaking a square coordinate into column and row
        log_move(): Logs the previous move in case the move needs to be reversed
        go_back(): Reverse previous move
        add_piece: Adds a piece to a square for testing or different game formats
        remove_piece: Removes a piece from a square
        
    '''
    def __init__(self, io):
        self.io = io
        self.previous_move = {'move_from':'', 'move_to':'', 'moved_piece':'',
                               'takes':None, 'pawn_double_move':False, 'player':None,
                               'promoted':False}
        self.row8 = ["8|", "r", "n", "b", "q", "k", "b", "n", "r"]
        self.row7 = ["7|", "p", "p", "p", "p", "p", "p", "p", "p"]
        self.row6 = ["6|"] + [None] * 8
        self.row5 = ["5|"] + [None] * 8
        self.row4 = ["4|"] + [None] * 8
        self.row3 = ["3|"] + [None] * 8
        self.row2 = ["2|", "P", "P", "P", "P", "P", "P", "P", "P"]
        self.row1 = ["1|", "R", "N", "B", "Q", "K", "B", "N", "R"]

    def draw_board(self):
        '''
        Draws the board using io
        '''
        self.__draw_row__(self.row8)
        self.__draw_row__(self.row7)
        self.__draw_row__(self.row6)
        self.__draw_row__(self.row5)
        self.__draw_row__(self.row4)
        self.__draw_row__(self.row3)
        self.__draw_row__(self.row2)
        self.__draw_row__(self.row1)
        self.__draw_row__(["‾|", "‾", "‾", "‾", "‾", "‾", "‾", "‾", "‾"])
        self.__draw_row__([" |", "A", "B", "C", "D", "E", "F", "G", "H"])

    def __draw_row__(self, row):
        newrow = []
        for i in row:
            newrow.append(i)
        for i, v in enumerate(newrow, start=0):
            if v is None:
                newrow[i] = "_"

        self.io.write(" ".join(newrow))

    def location_translator(self, column, row):
        '''
        Returns the piece in a square

        Args:
            column (str): Column of the square (abcedfgh)
            row (int): Row of the square (1-8)

        Returns:
            Piece (KQRBNPkqrbnp), None or (False, 'Error msg')
        '''
        if column and column.lower() in "abcdefgh":
            column = "abcdefgh".index(column.lower()) + 1
        else:
            return False, "Err: Incorrect position"

        row_mapping = {
            1: "row1",
            2: "row2",
            3: "row3",
            4: "row4",
            5: "row5",
            6: "row6",
            7: "row7",
            8: "row8",
        }

        mapped_row = row_mapping.get(row, False)

        if mapped_row:
            row = getattr(self, mapped_row)
            return row[column]

        return False, "Err: incorrect position"

    def piece_owner(self, column, row):
        '''
        Returns the owner of the piece in a square

        Args:
            column (str): Column of the square (abcedfgh)
            row (int): Row of the square (1-8)

        Returns:
            'Black' or 'White or (False, 'Error msg')
        '''
        val = self.location_translator(column, row)
        if val is None:
            return False, "Err: No piece there"
        if len(val) == 2:
            return val

        if val.islower():
            return "Black"

        if val.isupper():
            return "White"

        return False, "Err: something went wrong with determining piece owner"

    # Chatgpt: generated code asking changes to my location_translator, edited heavily
    def move_piece(self, move_from, move_to, player, no_log):
        '''
        Moves piece from square to another and handles special moves and calls for log

        Args:
            move_from (str): Square, eg. 'a1'
            move_to (str): Square, eg. 'a1'
            player (str): 'Black' or 'White'
            no_log (bool): If the move is logged or maybe a call from override

        Returns:
            True or (False, 'Error msg')
        '''
        if no_log is False:
            val = self.__log_move__(move_from, move_to, player)
            if val is not True:
                return False, 'Something very bad has happened with the log'
        column_from, row_from = move_from[0], int(move_from[1])
        column_to, row_to = move_to[0], int(move_to[1])

        if column_from.lower() not in "abcdefgh" or column_to.lower() not in "abcdefgh" \
                or row_from not in range(1, 9) or row_to not in range(1, 9):
            return False, "Err: Incorrect position"

        column_from = "abcdefgh".index(column_from.lower()) + 1
        column_to = "abcdefgh".index(column_to.lower()) + 1

        mapped_row_from = f"row{row_from}"
        mapped_row_to = f"row{row_to}"

        if not hasattr(self, mapped_row_from) or not hasattr(self, mapped_row_to):
            return False, "Err: Incorrect position"

        row_from = getattr(self, mapped_row_from)
        row_to = getattr(self, mapped_row_to)

        #auto-promote to queen
        c1, r1 = self.break_move(move_from)
        piece = self.location_translator(c1, r1)
        c2, r2 = self.break_move(move_to)
        if piece == 'P' and r2 == 8:
            piece = 'Q'
        if piece == 'p' and r2 == 1:
            piece = 'q'

        #en passant
        if piece.lower() == 'p' and c1 != c2 and self.location_translator(c2, r2) is None:
            self.remove_piece(c2+str(r1))

        #castling, legality already checked
        if piece == 'K' and move_from == 'e1' and move_to == 'g1':
            self.move_piece('h1', 'f1', player, False)
        if piece == 'K' and move_from == 'e1' and move_to == 'c1':
            self.move_piece('a1', 'd1', player, False)
        if piece == 'k' and move_from == 'e8' and move_to == 'g8':
            self.move_piece('h8', 'f8', player, False)
        if piece == 'k' and move_from == 'e8' and move_to == 'c8':
            self.move_piece('a8', 'd8', player, False)

        row_from[column_from] = None

        row_to[column_to] = piece

        return True
    # generated code ends

    def move_to_direction(self, move_from, direction):
        '''
        Returns adjacent square in direction
        Could have been broken up but I ran out of time for refactoring

        Args:
            move_from (str): Square, eg. 'a1'
            direction (str): 'up' or 'down' or 'right' or 'left
            
        Returns:
            square (str) or (False, 'Err msg')
        '''
        if move_from[0] is not False:
            column_from, row_from = move_from[0], int(move_from[1])
        else:
            return move_from

        if direction == "up":
            column_to, row_to = column_from, (row_from + 1)
        elif direction == "down":
            column_to, row_to = column_from, (row_from - 1)
        elif direction == "right":
            if column_from.lower() not in "abcdefg":
                return False, "Error moving the piece right"

            column_from = "abcdefgh".index(column_from.lower())
            column_to = "abcdefgh"[column_from + 1]
            row_to = row_from
        elif direction == "left":
            if column_from.lower() not in "bcdefgh":
                return False, "Error moving the piece left"

            column_from = "abcdefgh".index(column_from.lower())
            column_to = "abcdefgh"[column_from - 1]
            row_to = row_from
        else:
            return False, "Invalid direction"

        move_to = column_to + str(row_to)
        val = self.location_translator(column_to, row_to)

        if val is None:
            return move_to
        if val[0] is not False:
            return move_to

        return False, f"Error moving the piece {direction}"

    def break_move(self, move):
        '''
        Returns column and row of the suare

        Args:
            move (str): Square, eg. 'a1'
        Returns:
            'a', 1
        '''
        return move[0], int(move[1])

    def __log_move__(self, move_from, move_to, current_turn):
        '''
        Updated the previous move to memory

        Args:
            move_from (str): Square, eg. 'a1'
            move_to (str): Square, eg. 'a1'
            current_turn (str): player, 'white' or 'black'
            
        Returns:
            True or (False, 'Err msg')
        '''
        self.previous_move['move_from'] = move_from
        self.previous_move['move_to'] = move_to
        column_from, row_from = self.break_move(move_from)
        column_to, row_to = self.break_move(move_to)
        moved_piece = self.location_translator(column_from, row_from)
        if moved_piece:
            #check for double pawn move for en passant
            if moved_piece == 'P':
                if self.move_to_direction(self.move_to_direction(
                    move_from, 'up'), 'up') == move_to:
                    self.previous_move['pawn_double_move']=True
                if row_to == 8:
                    self.previous_move['promoted'] = True
            elif moved_piece == 'p':
                if self.move_to_direction(self.move_to_direction(
                    move_from, 'down'), 'down') == move_to:
                    self.previous_move['pawn_double_move']=True
                if row_to == 1:
                    self.previous_move['promoted'] = True
            else:
                self.previous_move['pawn_double_move']=False
            self.previous_move['moved_piece'] = moved_piece
        else:
            return False, "Please report this error - everything is wrong"
        self.previous_move['takes'] = self.location_translator(column_to, row_to)
        self.previous_move['player'] = current_turn
        return True

    def go_back(self):
        '''
        Cancels the previous move using memory
            
        Returns:
            Nothing or (False, 'Err msg')
        '''
        val = self.move_piece(self.previous_move['move_to'],
                         self.previous_move['move_from'], self.previous_move['player'], True)
        if val is not True:
            return val
        if self.previous_move['takes'] is not None:
            self.add_piece(self.previous_move['move_to'], self.previous_move['takes'])
        if self.previous_move['promoted'] is True:
            self.add_piece(self.previous_move['move_from'], 'p')

    def add_piece(self, square, piece):
        '''
        Adds any piece besides kings to square

        Args:
            square (str): Square, eg. 'a1'
            piece (str): Piece, 'QRBNPqrbnp'
            
        Returns:
            True or (False, 'Err msg')
        '''
        column_to, row_to = self.break_move(square)
        if  column_to.lower() not in "abcdefgh" \
                 or row_to not in range(1, 9):
            return False, "Err: Incorrect position"
        column_to = "abcdefgh".index(column_to.lower()) + 1
        mapped_row_to = f"row{row_to}"

        if not hasattr(self, mapped_row_to):
            return False, "Err: Incorrect position"
        row_to = getattr(self, mapped_row_to)
        row_to[column_to] = piece
        return True

    def remove_piece(self, square):
        '''
        Removes piece prom square

        Args:
            square (str): Square, eg. 'a1'  
        Returns:
            True or (False, 'Err msg')
        '''
        column_to, row_to = self.break_move(square)
        if  column_to.lower() not in "abcdefgh" \
                 or row_to not in range(1, 9):
            return False, "Err: Incorrect position"
        column_to = "abcdefgh".index(column_to.lower()) + 1
        mapped_row_to = f"row{row_to}"

        if not hasattr(self, mapped_row_to):
            return False, "Err: Incorrect position"
        row_to = getattr(self, mapped_row_to)
        row_to[column_to] = None
        return True
