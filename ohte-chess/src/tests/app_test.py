import unittest
from unittest.mock import Mock, MagicMock
from app import App


class TestApp(unittest.TestCase):
    def setUp(self):
        self.board = Mock()
        self.turn = Mock()
        self.io = Mock()
        self.test_app = App(self.board, self.turn, self.io)
        self.test_app.legality = Mock()

    def test_app_run_exits_properly(self):
        self.test_app.turn.which_player = MagicMock(return_value="White")
        self.test_app.io.read = MagicMock(return_value="exit")

        self.test_app.run()

        self.test_app.board.draw_board.assert_called()
        self.test_app.turn.which_player.assert_called()

        self.test_app.io.read.assert_called()
        # loop should break before pass_turn baing called
        self.test_app.turn.pass_turn.assert_not_called()

    def test_app_run_calls_services_correctly(self):
        self.test_app.turn.which_player = MagicMock(
            side_effect=["White", "Black"])
        self.test_app.io.read = MagicMock(side_effect=["a2", "a3", "exit"])
        self.test_app.legality.correct_player = MagicMock(return_value=True)
        self.test_app.board.move_piece = MagicMock(return_value=True)
        self.test_app.legality.legal_pos = MagicMock(return_value=("a", 1))

        self.test_app.run()

        self.test_app.board.draw_board.assert_called()
        self.test_app.turn.which_player.assert_called()

        self.test_app.io.read.assert_called()

        self.test_app.legality.correct_player.assert_called_with("White", "a2")

        self.test_app.turn.pass_turn.assert_called()

        self.test_app.io.read.assert_called()
        self.test_app.turn.pass_turn.assert_called_once()
