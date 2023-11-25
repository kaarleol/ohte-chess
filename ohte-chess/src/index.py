import services.draw_board as draw_board

def board(board):
    draw_board.print_chessboard(board)
    return

def create_chessboard():
    chessboard = [["#" for _ in range(8)] for _ in range(9)]

    chessboard[0] = ["r", "n", "b", "q", "k", "b", "n", "r"]
    chessboard[1] = ["p"] * 8
    chessboard[6] = ["P"] * 8
    chessboard[7] = ["R", "N", "B", "Q", "K", "B", "N", "R"]
    chessboard[8] = ["A̅", "B̅", "C̅", "D̅", "E̅", "F̅", "G̅", "H̅"]

    return chessboard

if __name__ == "__main__":
    initial_chessboard = create_chessboard()
    board(initial_chessboard)