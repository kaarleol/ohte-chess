import unittest
from board import Board


class testBoard(unittest.TestCase):
    def setUp(self):
        self.test_board = Board()

    def test_location_translater_with_correct_pos(self):
        val = self.test_board.location_translator('a', 1)

        self.assertEqual(val, "R")

    def test_location_translater_with_incorrect_pos(self):
        val = self.test_board.location_translator('i', 9)

        self.assertEqual(val[0], False)

    def test_piece_owner_with_correct_pos(self):
        val = self.test_board.piece_owner('a', 1)
        self.assertEqual(val, "White")

        val = self.test_board.piece_owner('a', 8)
        self.assertEqual(val, "Black")

    def test_piece_owner_with_incorrect_pos(self):
        val = self.test_board.piece_owner('a', 9)
        self.assertEqual(val[0], False)

    def test_move_piece_with_correct_positions(self):
        val = self.test_board.location_translator('a', 2)
        self.assertEqual(val, "P")

        self.test_board.move_piece('a2', 'a3')

        val = self.test_board.location_translator('a', 2)
        self.assertEqual(val, None)

        val2 = self.test_board.location_translator('a', 3)
        self.assertEqual(val2, "P")
