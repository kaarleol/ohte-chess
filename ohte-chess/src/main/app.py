from services.legal_moves import LegalMove
from services.turn import Turn
from entities.board import Board


class App:
    '''
    Game loop, handles inputs, commands, verifies rules 

    Atrributes:
        board: connection to the Board class for saving game state and drawing the board
        turn: connection to Turn class for keeping turncount and current player
        io: IO for prompting for moves, printin errors
        legality: connection to the LegalMove class for verifying rules
        move_from (str): Saves square from prompt between loops
        move_to (str): Saves square from prompt between loops
        did_exit (bool): Saves exit command between loops to skip them
        command_written: Saves if a command has been written to skip loop

    
    Methods:
        run(): Game loop, prompts for moves, verifies moves, sends moves to Board
            Commands: exit, resign, draw, help, new, override
        help(): runs with 'help' command, lists commands
        new(): runs with 'new' command. Begins a new game
        resign(): runs with 'resign' command. End the game and prompts for a new one
        draw(): runs with 'resign' command. End the game and prompts for a new one
        override(): runs with 'override' command to override mistakes by the program
            or tests or for fun
        mate(): mate handling when one is reached
    '''
    def __init__(self, board, turn, io):
        self.board = board
        self.turn = turn
        self.io = io
        self.legality = LegalMove(self.board)

        self.move_from = None
        self.move_to = None
        self.did_exit = False
        self.command_written = False

    def run(self):
        self.io.write("Write help for help")
        while True:
            self.board.draw_board()
            current_player = self.turn.which_player()
            self.legality.current_turn = current_player
            self.command_written = False
            self.io.write("")
            self.io.write(f"{current_player}'s move")
            legal_moves = []
            did_cancel = False

            val = self.legality.check_checker()
            if val is True:
                self.io.write('Check!')
                val = self.legality.mate_checker()
                if val is True:
                    self.mate()
                    self.did_exit = True
                    break

            while True:
                move = self.io.read(
                    "Give the square you would like to move from:")

                if move == "exit":
                    self.did_exit = True
                    break
                elif move == "resign":
                    self.resign()
                    self.command_written = True
                    break
                elif move == "draw":
                    self.draw()
                    self.command_written = True
                    break
                elif move == "help":
                    self.help()
                    self.command_written = True
                    break
                elif move == "new":
                    self.new()
                    self.command_written = True
                    break
                elif move == "override":
                    self.override()
                    self.command_written = True
                    break


                val = self.legality.correct_player(current_player, move)
                if val is True:
                    legal_moves = self.legality.legal_moves(move)
                    self.io.write(f'Possible moves: {legal_moves}')
                else:
                    self.io.write(val[1])

                if len(legal_moves) >= 1:
                    self.move_from = move
                    break
                else:
                    self.io.write('Piece has no legal moves')

            while True:
                if self.command_written is True:
                    break
                if self.did_exit is True:
                    break
                move = self.io.read(
                    "Give the square you would like to move to:")

                if move == "exit":
                    self.did_exit = True
                    break
                if move == 'cancel':
                    did_cancel = True
                    break
                elif move == "resign":
                    self.resign()
                    break
                elif move == "new":
                    self.new()
                    break
                elif move == "draw":
                    self.draw()
                    break
                elif move == "help":
                    self.help()
                    break
                elif move == "override":
                    self.override()
                    break

                val = self.legality.legal_pos(move)
                if val[0] is not False:
                    if move in legal_moves:
                        self.move_to = move
                        break
                    else:
                        self.io.write('Not a legal move for that piece')
                self.io.write(val[1])

            if self.did_exit is True:
                break

            if did_cancel is False and self.command_written is False:
                val = self.legality.log_move(self.move_from, self.move_to)
                if val is not True:
                    self.io.write(val[1])
                    return
                val = self.board.move_piece(self.move_from, self.move_to, current_player, False)
                if val is not True:
                    self.io.write(val[1])
                    break
                val = self.legality.would_be_in_check()
                if val is True:
                    self.io.write('Not a legal move due to check')
                    self.board.go_back()
                    self.legality.go_back_log()
                else:
                    self.turn.pass_turn()

    def help(self):
        '''
        Help. Runs with 'help' during game
        '''
        self.io.write('Commands:')
        self.io.write('exit - closes the app')
        self.io.write('new - resets the board and begins a new game')
        self.io.write('cancel - cancels selection of the piece if you do not want to move it')
        self.io.write('resign - ends the game and prompts for a new one. Current player loses')
        self.io.write('draw - ends the game and prompts for a one. The game is declared a draw')
        self.io.write('override - allows you to add, remove, or move a piece anywhere ingame')
        self.io.write('help - lists commands')
        self.io.write('')
        self.io.write('How to play:')
        self.io.write('To move a piece, input the square you want to move from')
        self.io.write('The input the square you want to move to')
        self.io.write('')
        self.io.write('The game tries to follow the logic of chess')
        self.io.write('')
        self.io.write('In case of mistakes, input override command')

    def new(self):
        '''
        Handles creating a new game. Can be called by command 'new' 
        or by other functions that start a new game
        '''
        self.board = Board(self.io)
        self.turn = Turn()
        self.legality = LegalMove(self.board)

    def resign(self):
        '''
        Resing game and prompt for a new one. Can be called by command 'resign'
        '''
        current_player = self.turn.which_player()
        if current_player == "White":
            other_player = 'Black'
        else:
            other_player = 'White'
        self.io.write(f'{current_player} resigns!')
        self.io.write(f'{other_player} is the winner!')

        val = self.io.read('Would you like to start a new game (y/n)?')
        if val.lower() == 'y':
            self.new()
        else:
            self.io.write('Closing the game')
            self.did_exit = True

    def draw(self):
        '''
        Draw game and prompt for a new one. Can be called by command 'draw'
        '''
        self.io.write('DRAW!')

        val = self.io.read('Would you like to start a new game (y/n)?')
        if val.lower() == 'y':
            self.new()
        else:
            self.io.write('Closing the game')
            self.did_exit = True

    def override(self):
        '''
        Allow player to manually move pieces outside the rules of the game,
        delete pieces (besides the king) or add pieces (besides the king or on king's square)
        Called wit 'override' and prompts for further commands
        '''
        current_player = self.turn.which_player()
        command = self.io.read("What would you like to do (move, add, delete)")

        if command == 'move':
            move_from = self.io.read("Give the square you would like to move from:")
            val = self.legality.legal_pos(move_from)
            if val[0] is not False:
                move_to = self.io.read("Give the square you would like to move to:")
                val = self.legality.legal_pos(move_to)
                if val[0] is not False:
                    val = self.board.move_piece(move_from, move_to, current_player, True)
                    if val:
                        self.io.write("MOVED!")
                    else:
                        self.io.write("Something went wrong. Aborting")
                else:
                    self.io.write("Incorrect square")
            else:
                self.io.write("Incorrect square")
        if command == 'add':
            square = self.io.read("Give the square you would like to add a piece to:")
            c, r = self.legality.legal_pos(square)
            piece = self.board.location_translator(c, r)
            if piece is None or piece.lower() != 'k':
                if c is not False:
                    piece = self.io.read("Enter the piece's symbol (QRBNPqrbnp):")
                    if piece in "QRBNPqrbnp":
                        val = self.board.add_piece(square, piece)
                        if val:
                            self.io.write("ADDED!")
                        else:
                            self.io.write("Something went wrong. Aborting")
                    else:
                        self.io.write("Incorrect symbol")
                else:
                    self.io.write("Incorrect sqaure")
            else:
                self.io.write("Cannot overwrite kings")
        if command == 'delete':
            square = self.io.read("Give the square you would like to empty:")
            c, r = self.legality.legal_pos(square)
            if c is not False:
                piece = self.board.location_translator(c, r)
                if piece.lower() != 'k':
                    val = self.board.remove_piece(square)
                    if val is True:
                        self.io.write("DELETED!")
                    else:
                        self.io.write("Something went wrong. Aborting")
                else:
                    self.io.write("Cannot delete kings")
            else:
                self.io.write("Incorrect symbol")

    def mate(self):
        '''
        Handles mate and end of the game
        '''
        self.io.write('MATE!')
        if self.turn.which_player == 'White':
            self.io.write('Black wins!!')
        else:
            self.io.write('White wins!!')

        val = self.io.read('Would you like to start a new game (y/n)?')
        if val.lower() == 'y':
            self.new()
        else:
            self.io.write('Closing the game')
            self.did_exit = True
