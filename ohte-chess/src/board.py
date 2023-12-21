class Board:
    def __init__(self, io):
        self.io = io
        self.previous_move = {'move_from':'', 'move_to':'', 'moved_piece':'',
                               'takes':None, 'pawn_double_move':False, 'player':None,
                               'promoted':False}
        self.squre_sixe = 40
        self.row8 = ["8|", "r", "n", "b", "q", "k", "b", "n", "r"]
        self.row7 = ["7|", "p", "p", "p", "p", "p", "p", "p", "p"]
        self.row6 = ["6|"] + [None] * 8
        self.row5 = ["5|"] + [None] * 8
        self.row4 = ["4|"] + [None] * 8
        self.row3 = ["3|"] + [None] * 8
        self.row2 = ["2|", "P", "P", "P", "P", "P", "P", "P", "P"]
        self.row1 = ["1|", "R", "N", "B", "Q", "K", "B", "N", "R"]
        self.white_king_moved = False
        self.a1_rook_moved = False
        self.h1_rook_moved = False
        self.black_king_moved = False
        self.a8_rook_moved = False
        self.h8_rook_moved = False

    def draw_board(self):
        self.draw_row(self.row8)
        self.draw_row(self.row7)
        self.draw_row(self.row6)
        self.draw_row(self.row5)
        self.draw_row(self.row4)
        self.draw_row(self.row3)
        self.draw_row(self.row2)
        self.draw_row(self.row1)
        self.draw_row(["‾|", "‾", "‾", "‾", "‾", "‾", "‾", "‾", "‾"])
        self.draw_row([" |", "A", "B", "C", "D", "E", "F", "G", "H"])

    def draw_row(self, row):
        newrow = []
        for i in row:
            newrow.append(i)
        for i, v in enumerate(newrow, start=0):
            if v is None:
                newrow[i] = "_"

        self.io.write(" ".join(newrow))

    def location_translator(self, column, row):
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

    # Chatgpt: generated code asking changes to my location_translator, edited
    def move_piece(self, move_from, move_to, player, no_log):
        if no_log is False:
            val = self.log_move(move_from, move_to, player)
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

        row_from[column_from] = None

        row_to[column_to] = piece

        return True
    # generated code ends

    def move_to_direction(self, move_from, direction):
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
        return move[0], int(move[1])

    def combine_move(self, column, row):
        return column + str(row)

    def log_move(self, move_from, move_to, current_turn):
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
            #save if king or rook moved to prevent castling
            if moved_piece == 'K':
                self.white_king_moved = True
            if moved_piece == 'k':
                self.black_king_moved = True
            if moved_piece == 'R' and move_from.lower() == 'a1':
                self.a1_rook_moved = True
            if moved_piece == 'R' and move_from.lower() == 'h1':
                self.h1_rook_moved = True
            if moved_piece == 'r' and move_from.lower() == 'a8':
                self.a8_rook_moved = True
            if moved_piece == 'r' and move_from.lower() == 'h8':
                self.h8_rook_moved = True
            self.previous_move['moved_piece'] = moved_piece
        else:
            return False, "Please report this error - everything is wrong"
        self.previous_move['takes'] = self.location_translator(column_to, row_to)
        self.previous_move['player'] = current_turn
        return True

    def go_back(self):
        val = self.move_piece(self.previous_move['move_to'],
                         self.previous_move['move_from'], self.previous_move['player'], True)
        if val is not True:
            return val
        if self.previous_move['takes'] is not None:
            self.add_piece(self.previous_move['move_to'], self.previous_move['takes'])
        if self.previous_move['promoted'] is True:
            self.add_piece(self.previous_move['move_from'], 'p')

    def add_piece(self, square, piece):
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

    def promote_white(self, moved_to):
        self.add_piece(moved_to, 'Q')

    def promote_black(self, moved_to):
        self.add_piece(moved_to, 'q')
