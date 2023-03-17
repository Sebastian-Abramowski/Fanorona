from pawn import Pawn
from pawn import Board
from constants import WHITE


def test_init():
    pawn = Pawn(5, 12, WHITE)
    assert pawn.row == 5
    assert pawn.column == 12
    assert pawn.colour == WHITE
    assert pawn.if_selected is False
    assert pawn.if_capture is False


def test_move():
    pawn = Pawn(5, 12, WHITE)
    pawn.move(1, 1)
    assert pawn.row == 1
    assert pawn.column == 1


def test_take_the_center_of_pawn():
    board = Board()
    board.centers_of_squares = [
        [(0, 0), (1, 1)], [(2, 2), (3, 3)]]
    pawn = Pawn(2, 2, WHITE)
    assert pawn._take_the_center_of_pawn(board) == (3, 3)
    assert pawn._take_the_center_of_pawn(board, 1, 1) == (0, 0)


def test_str():
    pawn = Pawn(5, 12, WHITE)
    assert str(pawn) == ("Row: 5, Column: 12, "
                         "colour: (255, 255, 255), selected: False")
