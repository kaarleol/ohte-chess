class Board:
    def __init__(self):
        self.row8 = ["8|", "r", "n", "b", "q", "k", "b", "n", "r"]
        self.row7 = ["7|", "p", "p", "p", "p", "p", "p", "p", "p"]
        self.row6 = ["6|"] + [None] * 8
        self.row5 = ["5|"] + [None] * 8
        self.row4 = ["4|"] + [None] * 8
        self.row3 = ["3|"] + [None] * 8
        self.row2 = ["2|", "P", "P", "P", "P", "P", "P", "P", "P"]
        self.row1 = ["1|", "R", "N", "B", "Q", "K", "B", "N", "R"]
        self.bottomrow1 = ["‾|", "‾", "‾", "‾", "‾", "‾", "‾", "‾", "‾"]
        self.bottomrow2 = [" |", "A", "B", "C", "D", "E", "F", "G", "H"]

    def draw_board(self):
        self.draw_row(self.row8)
        self.draw_row(self.row7)
        self.draw_row(self.row6)
        self.draw_row(self.row5)
        self.draw_row(self.row4)
        self.draw_row(self.row3)
        self.draw_row(self.row2)
        self.draw_row(self.row1)
        self.draw_row(self.bottomrow1)
        self.draw_row(self.bottomrow2)

    def draw_row(self, row):
        newrow = []
        for i in row:
            newrow.append(i)
        for i, v in enumerate(newrow, start=0):
            if v is None:
                newrow[i] = "_"

        print(" ".join(newrow))

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

    # Chatgpt: generated code asking changes to my location_translator
    def move_piece(self, move_from, move_to):
        column_from, row_from = move_from[0], int(move_from[1])
        column_to, row_to = move_to[0], int(move_to[1])

        # Check if the move_from and move_to positions are valid
        if column_from.lower() not in "abcdefgh" or column_to.lower() not in "abcdefgh" \
                or row_from not in range(1, 9) or row_to not in range(1, 9):
            return False, "Err: Incorrect position"

        # Convert column letter to index
        column_from = "abcdefgh".index(column_from.lower()) + 1
        column_to = "abcdefgh".index(column_to.lower()) + 1

        # Get the attribute name for the rows
        mapped_row_from = f"row{row_from}"
        mapped_row_to = f"row{row_to}"

        # Check if the row attributes exist
        if not hasattr(self, mapped_row_from) or not hasattr(self, mapped_row_to):
            return False, "Err: Incorrect position"

        # Get the rows
        row_from = getattr(self, mapped_row_from)
        row_to = getattr(self, mapped_row_to)

        # Get the piece from move_from and set it to None
        piece = row_from[column_from]
        row_from[column_from] = None

        # Set the piece to move_to
        row_to[column_to] = piece

        return True
    # generated code ends
