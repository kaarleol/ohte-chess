def print_chessboard(chessboard):
    i = 8
    for row in chessboard:
        if i> 0:
            print(f"{i}|" + " ".join(row))
        else: 
            print("‾|" + " ".join(row))
        i -=1


