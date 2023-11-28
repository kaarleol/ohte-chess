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
        for i in enumerate(newrow, start=0):
            if newrow[i] is None:
                newrow[i] = "_"

        print(" ".join(newrow))

    def location_translator(self, column, row):
        if column and column.lower() in "abcdefgh":
            column = "abcdefgh".index(column.lower()) + 1
        else:
            return False

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

        return False


    def piece_owner(self, column, row):
        val = self.location_translator(column, row)
        if val is None or not val:
            print("none or false")
            return False

        if val.islower():
            print("black")
            return "Black"

        if val.isupper():
            print("white")
            return "White"

        return False
