from entities.board import Board
from services.turn import Turn
from services.console_io import ConsoleIO
from main.app import App

def main():
    '''
    Creates the game and starts the game loop
    '''
    console_io = ConsoleIO()
    turns = Turn()
    gameboard = Board(console_io)

    game = App(gameboard, turns, console_io)
    game.run()


if __name__ == "__main__":
    main()
