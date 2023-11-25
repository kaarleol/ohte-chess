import board
import turn

def main():
    currentTurn=turn.Turn()
    print(currentTurn.which_player())

    gameboard=board.Board()
    gameboard.draw_board()

    print(gameboard.location_translator("a", 1))
    print(gameboard.location_translator("c", 3))
    print(gameboard.location_translator("H", 8))  
    print(gameboard.piece_owner("a", 1))
    print(gameboard.piece_owner("c", 3))
    print(gameboard.piece_owner("H", 8))  

    currentTurn.pass_turn()
    print(currentTurn.which_player())

    return


if __name__ == "__main__":
    main()