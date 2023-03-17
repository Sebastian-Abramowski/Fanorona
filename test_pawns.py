from pawns import Pawns
from pawn import Pawn
from constants import WHITE, BLACK, WHITE2


def test_init():
    pawn = Pawn(1, 1, WHITE)
    pawn2 = Pawn(2, 2, WHITE)
    pawn3 = Pawn(3, 3, BLACK)
    pawns = Pawns([pawn, pawn2, pawn3])
    assert pawns.whites == 0
    assert pawns.blacks == 0
    assert pawns.pawns == [pawn, pawn2, pawn3]


def test_init2():
    # testings casual board (ROW=5, COLS=9)
    pawns = Pawns()
    assert pawns.whites == 22
    assert pawns.blacks == 22
    assert len(pawns.pawns) == 44


def test_clear_highlights():
    pawn = Pawn(1, 1, WHITE, True)
    pawn2 = Pawn(2, 2, WHITE, True)
    assert pawn2.if_selected is True
    pawn3 = Pawn(3, 3, BLACK)
    pawns = Pawns([pawn, pawn2, pawn3])
    pawns.clear_highlights()
    assert pawn.if_selected is False
    assert pawn2.if_selected is False


def test_clear_if_capture():
    pawn = Pawn(1, 1, WHITE, True)
    pawn2 = Pawn(2, 2, WHITE, True)
    pawn.if_capture = True
    pawn2.if_capture = True
    pawns = Pawns([pawn, pawn2])
    pawns.clear_if_capture()
    assert pawn.if_capture is False
    assert pawn2.if_capture is False


def test_is_place_empty():
    pawn = Pawn(1, 1, WHITE)
    pawn2 = Pawn(2, 2, WHITE)
    pawn3 = Pawn(3, 3, BLACK)
    pawns = Pawns([pawn, pawn2, pawn3])
    assert pawns.is_place_empty(4, 4) == (True, None)
    assert pawns.is_place_empty(2, 2) == (False, WHITE)


def test_remove_pawn():
    pawn = Pawn(1, 1, WHITE)
    pawn2 = Pawn(2, 2, WHITE)
    pawn3 = Pawn(3, 3, BLACK)
    pawns = Pawns([pawn, pawn2, pawn3])
    pawns.remove_pawn(2, 2)
    assert len(pawns.pawns) == 2
    assert pawns.pawns == [pawn, pawn3]


def test_colour_of_pawn():
    pawn = Pawn(1, 1, WHITE)
    pawn2 = Pawn(2, 2, WHITE)
    pawn3 = Pawn(3, 3, BLACK)
    pawns = Pawns([pawn, pawn2, pawn3])
    assert pawns._colour_of_pawn(3, 3) == BLACK


def test_colour_of_pawns_to_default():
    pawn = Pawn(1, 1, WHITE)
    pawn2 = Pawn(2, 2, WHITE)
    pawn3 = Pawn(3, 3, WHITE2)
    pawns = Pawns([pawn, pawn2, pawn3])
    pawns._change_colours_to_default()
    assert pawn3.colour == WHITE


def test_hihglight_pawn():
    pawn = Pawn(1, 1, WHITE, True)
    pawn2 = Pawn(2, 2, WHITE, True)
    pawn3 = Pawn(3, 3, WHITE2, False)
    pawns = Pawns([pawn, pawn2, pawn3])
    pawns.highlight_pawn(pawn3)
    assert pawn.if_selected is False
    assert pawn2.if_selected is False
    assert pawn3.if_selected is True
