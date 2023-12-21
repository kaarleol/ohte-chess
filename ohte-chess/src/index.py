from board import Board
from turn import Turn
from console_io import ConsoleIO
from app import App
from ui import UI

def main():
    ui = None
    console_io = ConsoleIO()
    turns = Turn()
    gameboard = Board(ui)

    game = App(gameboard, turns, console_io)
    game.run()


if __name__ == "__main__":
    main()
