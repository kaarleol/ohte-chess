import unittest
from unittest.mock import Mock, MagicMock
from app import App


class TestApp(unittest.TestCase):
    def setUp(self):
        self.board = Mock()
        self.turn = Mock()
        self.io = Mock()
        self.legality = Mock()
        self.test_app = App(self.board, self.turn, self.io)

    def test_app_run_exits_properly(self):
        self.test_app.turn.which_player = MagicMock(return_value="White")
        self.test_app.io.read = MagicMock(return_value="exit")

        self.test_app.run()

        self.test_app.board.draw_board.assert_called()
        self.test_app.turn.which_player.assert_called()

        self.test_app.io.read.assert_called()

        self.test_app.turn.pass_turn.assert_not_called()
