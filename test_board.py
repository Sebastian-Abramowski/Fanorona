from board import Board
from constants import ROWS, COLS


def test_init():
    board = Board()
    assert board.rows == ROWS
    assert board.columns == COLS
    assert board.centers_of_squares is None
    assert isinstance(board.rectangles_boxes, list) is True
    assert len(board.rectangles_boxes) == 0
    assert board._square_size is None


def test_row_col_method():
    board = Board()
    board.centers_of_squares = [
        [(0, 0), (1, 1), (2, 2), (8, 8), (15, 12)],
        [(2, 3), (5, 3), (12, 4), (42, 21), (19, 20)]
        ]
    assert board.row_col_from_center_of_square((2, 2)) == (1, 3)
    assert board.row_col_from_center_of_square((15, 12)) == (1, 5)
    assert board.row_col_from_center_of_square((19, 20)) == (2, 5)
    assert board.row_col_from_center_of_square((20, 20)) is None
