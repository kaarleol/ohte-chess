import unittest
from unittest.mock import Mock, ANY, MagicMock
from app import App

class TestApp(unittest.TestCase):
    def setUp(self):
        self.board = Mock()
        self.turn = Mock()
        self.io = Mock()
        self.legality = Mock()
        self.testApp = App(self.board, self.turn, self.io)

    def test_app_run_exits_properly(self):
        self.testApp.turn.which_player = MagicMock(return_value="White")
        self.testApp.io.read = MagicMock(return_value="exit")

        self.testApp.run()

        self.testApp.board.draw_board.assert_called()
        self.testApp.turn.which_player.assert_called()

        self.assertEqual(self.testApp.currentPlayer, "White")

        self.testApp.io.read.assert_called()

        self.testApp.turn.pass_turn.assert_not_called()

        

        

        

