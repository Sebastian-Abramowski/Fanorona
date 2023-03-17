from fanorona import Fanorona, FanoronaLogic
from constants import WrongUseOfCaptureByAppOrWithFunc
from constants import WHITE, BLACK
from pawn import Pawn
from pawns import Pawns
import pytest


def test_init():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    assert f_logic.fanorona == fanorona

def test_capture_exception_approach():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 2, WHITE)
    fanorona.selected_pawn = pawn
    with pytest.raises(WrongUseOfCaptureByAppOrWithFunc):
        f_logic.capture_by_approach(1, 4)

def test_capture_exception_withdrawal():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 2, WHITE)
    fanorona.selected_pawn = pawn
    with pytest.raises(WrongUseOfCaptureByAppOrWithFunc):
        f_logic.capture_by_withdrawal(3, 3)

def test_capture_by_approach_1():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 2, WHITE)
    pawn2 = Pawn(3, 4, BLACK)
    pawn3= Pawn(4, 5, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_approach(2, 3)
    assert cap == [(3, 4), (4, 5)]

def test_capture_by_approach_2():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 2, WHITE)
    pawn2 = Pawn(3, 2, BLACK)
    pawn3= Pawn(4, 2, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_approach(2, 2)
    assert cap == [(3, 2), (4, 2)]

def test_capture_by_approach_3():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 5, WHITE)
    pawn2 = Pawn(3, 3, BLACK)
    pawn3= Pawn(4, 2, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_approach(2, 4)
    assert cap == [(3, 3), (4, 2)]

def test_capture_by_approach_4():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 1, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3= Pawn(1, 4, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_approach(1, 2)
    assert cap == [(1, 3), (1, 4)]

def test_capture_by_approach_5():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 5, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3= Pawn(1, 2, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_approach(1, 4)
    assert cap == [(1, 3), (1, 2)]

def test_capture_by_approach_6():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(4, 2, WHITE)
    pawn2 = Pawn(2, 2, BLACK)
    pawn3= Pawn(1, 2, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_approach(3, 2)
    assert cap == [(2, 2), (1, 2)]

def test_capture_by_approach_7():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(4, 1, WHITE)
    pawn2 = Pawn(2, 3, BLACK)
    pawn3= Pawn(1, 4, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_approach(3, 2)
    assert cap == [(2, 3), (1, 4)]

def test_capture_by_approach_8():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(4, 4, WHITE)
    pawn2 = Pawn(2, 2, BLACK)
    pawn3= Pawn(1, 1, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_approach(3, 3)
    assert cap == [(2, 2), (1, 1)]


def test_capture_by_withdrawal_1():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(2, 3, WHITE)
    pawn2 = Pawn(3, 4, BLACK)
    pawn3= Pawn(4, 5, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_withdrawal(1, 2)
    assert cap == [(3, 4), (4, 5)]

def test_capture_by_withdrawal_2():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(3, 4, WHITE)
    pawn2 = Pawn(1, 2, BLACK)
    pawn3= Pawn(2, 3, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_withdrawal(4, 5)
    assert cap == [(2, 3), (1, 2)]

def test_capture_by_withdrawal_3():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(3, 2, WHITE)
    pawn2 = Pawn(1, 4, BLACK)
    pawn3= Pawn(2, 3, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_withdrawal(4, 1)
    assert cap == [(2, 3), (1, 4)]

def test_capture_by_withdrawal_4():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(2, 3, WHITE)
    pawn2 = Pawn(4, 1, BLACK)
    pawn3= Pawn(3, 2, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_withdrawal(1, 4)
    assert cap == [(3, 2), (4, 1)]


def test_capture_by_withdrawal_5():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 3, WHITE)
    pawn2 = Pawn(1, 4, BLACK)
    pawn3= Pawn(1, 5, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_withdrawal(1, 2)
    assert cap == [(1, 4), (1, 5)]

def test_capture_by_withdrawal_6():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 3, WHITE)
    pawn2 = Pawn(1, 1, BLACK)
    pawn3= Pawn(1, 2, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_withdrawal(1, 4)
    assert cap == [(1, 2), (1, 1)]

def test_capture_by_withdrawal_7():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(3, 1, WHITE)
    pawn2 = Pawn(1, 1, BLACK)
    pawn3= Pawn(2, 1, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_withdrawal(4, 1)
    assert cap == [(2, 1), (1, 1)]


def test_capture_by_withdrawal_8():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(2, 1, WHITE)
    pawn2 = Pawn(3, 1, BLACK)
    pawn3= Pawn(4, 1, BLACK)
    fanorona.selected_pawn = pawn
    fanorona.pawns = Pawns([pawn, pawn2, pawn3])
    cap = f_logic.capture_by_withdrawal(1, 1)
    assert cap == [(3, 1), (4, 1)]

def test_empty_space_validator_list():
    poss = [(1, 1), (1, 2), (1, 3)]
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(1, 1, WHITE)
    pawn2 = Pawn(1, 2, BLACK)
    fanorona.pawns = Pawns([pawn, pawn2])
    new_poss = f_logic.empty_space_validator_list(poss)
    assert new_poss == [(1, 3)]

def test_last_move_validator_poss():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    poss = [(1, 1), (2, 2), (1, 3)]
    pawn = Pawn(1, 2, WHITE)
    fanorona.selected_pawn = pawn
    fanorona.possibilities = poss
    fanorona.last_move = "E"
    new_poss = f_logic.last_move_validator_poss()
    assert new_poss == [(1, 1), (2, 2)]

def test_possibilities_of_pawn():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(2, 2, WHITE)
    assert f_logic.possibilities_of_pawn(pawn) == [
        (1, 2), (3, 2), (2, 1), (2, 3), (1, 1), (3, 3), (1, 3), (3, 1)]
    pawn = Pawn(1, 1, WHITE)
    assert f_logic.possibilities_of_pawn(pawn) == [
        (2, 1), (2, 2), (1, 2)]
    pawn = Pawn(1, 3, WHITE)
    assert f_logic.possibilities_of_pawn(pawn) == [
        (2, 3), (2, 4), (2, 2), (1, 4), (1, 2)]
    pawn = Pawn(3, 2, WHITE)
    assert f_logic.possibilities_of_pawn(pawn) == [
        (2, 2), (4, 2), (3, 1), (3, 3)]
    pawn = Pawn(3, 1, WHITE)
    assert f_logic.possibilities_of_pawn(pawn) == [
        (3, 2), (2, 2), (4, 2), (2, 1), (4, 1)]
    pawn = Pawn(4, 1, WHITE)
    assert f_logic.possibilities_of_pawn(pawn) == [
        (4, 2), (3, 1), (5, 1)]

def test_possible_captures_approach():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn1 = Pawn(3, 3, WHITE)
    pawn2 = Pawn(1, 1, BLACK)
    pawn3 = Pawn(1, 3, BLACK)
    pawn4 = Pawn(1, 5, BLACK)
    pawn5 = Pawn(3, 5, BLACK)
    pawn6 = Pawn(3, 1, BLACK)
    pawn7 = Pawn(5, 1, BLACK)
    pawn8 = Pawn(5, 3, BLACK)
    pawn9 = Pawn(5, 5, BLACK)
    fanorona.pawns = Pawns([
        pawn1, pawn2, pawn3, pawn4, pawn5, pawn6, pawn7, pawn8, pawn9])
    poss = f_logic.possibilities_of_pawn(pawn1)
    poss_cap = f_logic.possible_captures_approach(pawn1, poss)
    assert poss_cap == poss
    assert poss_cap == [
        (2, 3), (4, 3), (3, 2), (3, 4), (2, 2), (4, 4), (2, 4), (4, 2)]

def test_possible_captures_withdrawal_half1():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn1 = Pawn(2, 2, WHITE)
    pawn2 = Pawn(1, 1, BLACK)
    pawn3 = Pawn(1, 2, BLACK)
    pawn4 = Pawn(1, 3, BLACK)
    pawn5 = Pawn(2, 1, BLACK)
    fanorona.pawns = Pawns([
        pawn1, pawn2, pawn3, pawn4, pawn5])
    poss = f_logic.possibilities_of_pawn(pawn1)
    poss_cap = f_logic.possible_captures_withdrowal(pawn1, poss)
    assert poss_cap == [(3, 2), (2, 3), (3, 3), (3, 1)]

def test_possible_captures_withdrawal_half2():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn1 = Pawn(3, 3, WHITE)
    pawn2 = Pawn(3, 4, BLACK)
    pawn3 = Pawn(4, 4, BLACK)
    pawn4 = Pawn(4, 3, BLACK)
    pawn5 = Pawn(4, 2, BLACK)
    fanorona.pawns = Pawns([
        pawn1, pawn2, pawn3, pawn4, pawn5])
    poss = f_logic.possibilities_of_pawn(pawn1)
    poss_cap = f_logic.possible_captures_withdrowal(pawn1, poss)
    assert poss_cap == [(2, 3), (3, 2), (2, 2), (2, 4)]


def test_last_move():
    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    pawn = Pawn(2, 2, WHITE)
    assert f_logic.get_last_move(pawn, 1, 2) == 'N'
    assert f_logic.get_last_move(pawn, 3, 2) == 'S'
    assert f_logic.get_last_move(pawn, 2, 3) == 'E'
    assert f_logic.get_last_move(pawn, 2, 1) == 'W'
    assert f_logic.get_last_move(pawn, 1, 1) == 'NW'
    assert f_logic.get_last_move(pawn, 1, 3) == 'NE'
    assert f_logic.get_last_move(pawn, 3, 1) == 'SW'
    assert f_logic.get_last_move(pawn, 3, 3) == 'SE'


def test_check_for_winner():
    # winning on board 3x3 was checked manually
    # winning on board different from 3x3:

    fanorona = Fanorona()
    f_logic = FanoronaLogic(fanorona)
    fanorona.pawns.whites = 1
    fanorona.pawns.blacks = 0
    assert f_logic.check_for_winner() == WHITE
    fanorona.pawns.blacks = 1
    fanorona.pawns.whites = 0
    assert f_logic.check_for_winner() == BLACK
