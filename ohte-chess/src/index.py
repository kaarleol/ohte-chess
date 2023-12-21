from board import Board
from turn import Turn
from console_io import ConsoleIO
from app import App

def main():
    console_io = ConsoleIO()
    turns = Turn()
    gameboard = Board(console_io)

    game = App(gameboard, turns, console_io)
    game.run()


if __name__ == "__main__":
    main()
