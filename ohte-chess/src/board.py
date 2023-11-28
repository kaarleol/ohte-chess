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
        for i in enumerate(newrow):
            if newrow[i] is None:
                newrow[i] = "_"

        print(" ".join(newrow))

    def location_translator(self, column, row):
        if column and column.lower() in "abcdefgh":
            column = "abcdefgh".index(column.lower()) + 1
        else:
            return False

        if row == 1:
            row = self.row1
        elif row == 2:
            row = self.row2
        elif row == 3:
            row = self.row3
        elif row == 4:
            row = self.row4
        elif row == 5:
            row = self.row5
        elif row == 6:
            row = self.row6
        elif row == 7:
            row = self.row7
        elif row == 8:
            row = self.row8
        else:
            return False

        return row[column]

    def piece_owner(self, column, row):
        val = self.location_translator(column, row)
        if val is None or not val:
            print("none or false")
            return False

        elif val.islower():
            print("black")
            return "Black"

        elif val.isupper():
            print("white")
            return "White"

        return False
