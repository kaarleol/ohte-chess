import unittest
from unittest.mock import Mock, MagicMock, call
from main.app import App
from entities.board import Board
from services.legal_moves import LegalMove
from services.turn import Turn


class TestApp(unittest.TestCase):
    def setUp(self):
        self.io = Mock()
        self.board = Board(self.io)
        self.turn = Turn()
        self.test_app = App(self.board, self.turn, self.io)
        self.test_app.legality = LegalMove(self.board)

    def test_app_run_exits_properly(self):
        self.test_app.io.read = MagicMock(return_value="exit")

        self.test_app.run()

        self.assertEqual(self.test_app.turn.which_player(), 'White')
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_run_exits_properly_after_a_move(self):
        self.test_app.io.read = MagicMock(side_effect=['a2', 'a4', 'exit'])

        self.test_app.run()

        self.assertEqual(self.test_app.turn.which_player(), 'Black')
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_mate_works_properly(self):
        self.test_app.io.read = MagicMock(return_value="n")
        self.test_app.mate()

        expected_write_calls = [
        call('MATE!'),
        call('Closing the game')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_resign_works_properly(self):
        self.test_app.io.read = MagicMock(return_value="n")
        self.test_app.resign()

        expected_write_calls = [
        call('White resigns!'),
        call('Closing the game')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_draw_works_properly(self):
        self.test_app.io.read = MagicMock(return_value="n")
        self.test_app.draw()

        expected_write_calls = [
        call('DRAW!'),
        call('Closing the game')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_help_works_properly(self):
        self.test_app.help()

        self.assertEqual(self.test_app.io.write.call_count, 16)

    def test_app_override_works_with_move_command(self):

        self.test_app.io.read = MagicMock(side_effect=['override', 'move', 'd1', 'd5', 'exit'])

        self.assertEqual(self.test_app.board.location_translator('d', 1), 'Q')
        self.assertEqual(self.test_app.board.location_translator('d', 5), None)
        self.test_app.run()

        self.assertEqual(self.test_app.board.location_translator('d', 1), None)
        self.assertEqual(self.test_app.board.location_translator('d', 5), 'Q')

        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_works_with_add_command(self):

        self.test_app.io.read = MagicMock(side_effect=['override', 'add', 'd5', 'Q', 'exit'])


        self.assertEqual(self.test_app.board.location_translator('d', 5), None)
        self.test_app.run()
        self.assertEqual(self.test_app.board.location_translator('d', 5), 'Q')

        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_works_with_delete_command(self):

        self.test_app.io.read = MagicMock(side_effect=['override', 'delete', 'd1', 'exit'])

        self.assertEqual(self.test_app.board.location_translator('d', 1), 'Q')
        self.test_app.run()
        self.assertEqual(self.test_app.board.location_translator('d', 1), None)

        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_works_with_move_command_during_move_to(self):

        self.test_app.io.read = MagicMock(side_effect=['a2','override', 'move', 'd1', 'd5', 'exit'])

        self.assertEqual(self.test_app.board.location_translator('d', 1), 'Q')
        self.assertEqual(self.test_app.board.location_translator('d', 5), None)
        self.test_app.run()

        self.assertEqual(self.test_app.board.location_translator('d', 1), None)
        self.assertEqual(self.test_app.board.location_translator('d', 5), 'Q')

        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_works_with_add_command_during_move_to(self):

        self.test_app.io.read = MagicMock(side_effect=['a2','override', 'add', 'd5', 'Q', 'exit'])


        self.assertEqual(self.test_app.board.location_translator('d', 5), None)
        self.test_app.run()
        self.assertEqual(self.test_app.board.location_translator('d', 5), 'Q')

        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_works_with_delete_command_during_move_to(self):

        self.test_app.io.read = MagicMock(side_effect=['a2', 'override', 'delete', 'd1', 'exit'])

        self.assertEqual(self.test_app.board.location_translator('d', 1), 'Q')
        self.test_app.run()
        self.assertEqual(self.test_app.board.location_translator('d', 1), None)

        self.assertEqual(self.test_app.did_exit, True)

    def test_app_new_clears_board_and_turn_counter(self):
        self.test_app.turn.turn = 5

        self.test_app.io.read = MagicMock(side_effect=['override', 'delete', 'd1', 'exit', 'exit'])

        self.assertEqual(self.test_app.board.location_translator('d', 1), 'Q')
        self.test_app.run()
        self.assertEqual(self.test_app.board.location_translator('d', 1), None)

        self.test_app.new()
        self.assertEqual(self.test_app.turn.turn, 1)
        self.assertEqual(self.test_app.board.location_translator('d', 1), 'Q')

    def test_app_resign_start_new_game_during_move_from(self):
        self.test_app.io.read = MagicMock(side_effect=['resign', 'y', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('White resigns!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_resign_start_new_game_during_move_to(self):
        self.test_app.io.read = MagicMock(side_effect=['a2', 'resign', 'y', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('White resigns!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)


    def test_app_draw_start_new_game_during_move_from(self):
        self.test_app.io.read = MagicMock(side_effect=['draw', 'y', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('DRAW!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_draw_start_new_game_during_move_to(self):
        self.test_app.io.read = MagicMock(side_effect=['a2', 'draw', 'y', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('DRAW!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_start_new_game_during_move_from(self):
        self.test_app.io.read = MagicMock(side_effect=['new', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Starting a new game!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_start_new_game_during_move_to(self):
        self.test_app.io.read = MagicMock(side_effect=['new', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Starting a new game!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_cancel_move_selection(self):
        self.test_app.io.read = MagicMock(side_effect=['a2', 'cancel', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('CANCELLED!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_no_legal_moves(self):
        self.test_app.io.read = MagicMock(side_effect=['a1', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Piece has no legal moves'),
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_exit_during_move_to(self):
        self.test_app.io.read = MagicMock(side_effect=['a2', 'exit'])
        self.test_app.run()

        self.assertEqual(self.test_app.did_exit, True)

    def test_app_help_during_move_from(self):
        self.test_app.io.read = MagicMock(side_effect=['help', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Commands:')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_help_during_move_to(self):
        self.test_app.io.read = MagicMock(side_effect=['a1', 'help', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Commands:')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_check_works(self):
        self.test_app.io.read = MagicMock(side_effect=['override', 'move', 'd1', 'd2', 'd2', 'd7', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Check!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)
        self.assertEqual(self.test_app.turn.turn, 2)

    def test_app_mate_works(self):
        self.test_app.io.read = MagicMock(side_effect=['override', 'move', 'd1', 'f2', 'override', 'move','a1', 'f1', 'f2', 'f7', 'n'])
        self.test_app.run()

        expected_write_calls = [
        call('MATE!'),
        call('Closing the game')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)
        self.assertEqual(self.test_app.turn.turn, 2)
    
    def test_app_mate_new_gameworks(self):
        self.test_app.io.read = MagicMock(side_effect=['override', 'move', 'd1', 'f2', 'override', 'move','a1', 'f1', 'f2', 'f7', 'y', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('MATE!'),
        call('Starting a new game!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_check_that_cannot_move_to_check(self):
        self.test_app.io.read = MagicMock(side_effect=['override', 'move', 'e1', 'e2', 'override', 'move', 'd8', 'd7', 'e2', 'd3', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Not a legal move due to check')
        ]
        self.assertEqual(self.test_app.board.location_translator('e', 2), 'K')
        self.assertEqual(self.test_app.board.location_translator('d', 3), None)
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)
        
    def test_app_new_game_during_move_to(self):
        self.test_app.io.read = MagicMock(side_effect=['e2', 'new', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Starting a new game!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_not_a_real_move(self):
        self.test_app.io.read = MagicMock(side_effect=['d2', 'd6', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Not a legal move for that piece')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_black_resign(self):
        self.test_app.io.read = MagicMock(side_effect=['d2', 'd4', 'resign', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Black resigns!')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_wrong_piece(self):
        
        self.test_app.io.read = MagicMock(side_effect=['override', 'add', 'a1', 'h', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Incorrect symbol')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_wrong_location(self):
        self.test_app.io.read = MagicMock(side_effect=['override', 'move', 'a9', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Incorrect square')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_wrong_location_move_to(self):
        self.test_app.io.read = MagicMock(side_effect=['override', 'move', 'a2', 'a9', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Incorrect square')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_delete_king(self):
        self.test_app.io.read = MagicMock(side_effect=['override', 'delete', 'e1', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Cannot delete kings')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_add_over_king(self):

        self.test_app.io.read = MagicMock(side_effect=['override', 'add', 'e1', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Cannot overwrite kings')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)

    def test_app_override_add_wrong_square(self):
        
        self.test_app.io.read = MagicMock(side_effect=['override', 'add', 'a9', 'exit'])
        self.test_app.run()

        expected_write_calls = [
        call('Incorrect square')
        ]
        self.test_app.io.write.assert_has_calls(expected_write_calls, any_order=True)
        self.assertEqual(self.test_app.did_exit, True)