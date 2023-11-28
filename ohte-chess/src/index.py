from board import Board
from turn import Turn
from console_io import ConsoleIO
from app import App


def main():
    consoleIO = ConsoleIO()
    turns = Turn()
    gameboard = Board()

    game = App(gameboard, turns, consoleIO)
    game.run()


if __name__ == "__main__":
    main()
