import unittest
from turn import Turn


class TestTurn(unittest.TestCase):
    def setUp(self):
        self.test_turn = Turn()

    def test_starting_turn_correct(self):
        self.assertEqual(self.test_turn.turn, 1)

    def test_pass_turn_works(self):
        self.assertEqual(self.test_turn.turn, 1)
        self.test_turn.pass_turn()

        self.assertEqual(self.test_turn.turn, 2)

    def test_which_player_works(self):
        self.assertEqual(self.test_turn.turn, 1)
        self.assertEqual(self.test_turn.which_player(), "White")

        self.test_turn.pass_turn()
        self.assertEqual(self.test_turn.which_player(), "Black")
