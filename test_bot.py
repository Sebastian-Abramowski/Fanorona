from bot import Best_move_picker
from bot import Best_pawn_picker
from fanorona import Fanorona
from constants import WHITE, BLACK
from pawn import Pawn
from pawns import Pawns


# test on typical board (ROWS = 5, COLS = 9)
def test_best_pawn_picker_starting():
    fanorona = Fanorona()
    # we have pawns placed on starting points
    fanorona.turn = WHITE
    picked_pawn = Best_pawn_picker._calc_best_pawn_to_pick(fanorona)
    assert (picked_pawn.row == 4 and picked_pawn.column in [4, 5, 6]) is True


def test_best_pawn_picker_typical():
    fanorona = Fanorona()
    fanorona.turn = WHITE
    fanorona.pawns.pawns.clear()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(3, 2, BLACK)
    pawn3 = Pawn(4, 2, BLACK)
    pawn4 = Pawn(1, 4, BLACK)
    pawn5 = Pawn(1, 6, WHITE)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3, pawn4, pawn5])
    picked_pawn = Best_pawn_picker._calc_best_pawn_to_pick(fanorona)
    assert picked_pawn == pawn1


def test_best_pawn_picked_more_complicated_test():
    fanorona = Fanorona()
    fanorona.turn = WHITE
    fanorona.pawns.pawns.clear()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(3, 2, BLACK)
    pawn3 = Pawn(4, 2, BLACK)
    pawn4 = Pawn(1, 4, BLACK)
    pawn5 = Pawn(1, 6, WHITE)
    pawn6 = Pawn(4, 1, BLACK)
    pawn7 = Pawn(4, 3, BLACK)
    pawn8 = Pawn(4, 4, WHITE)
    fanorona.pawns = Pawns([
        pawn1, pawn2, pawn3, pawn4, pawn5, pawn6, pawn7, pawn8
        ])
    picked_pawn = Best_pawn_picker._calc_best_pawn_to_pick(fanorona)
    assert picked_pawn == pawn8

# ------------------------------


def test_best_move_picker_calc_withdrawal():
    fanorona = Fanorona()
    fanorona.turn = WHITE
    fanorona.pawns.pawns.clear()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(3, 2, BLACK)
    pawn3 = Pawn(4, 2, BLACK)
    pawn4 = Pawn(1, 4, BLACK)
    pawn5 = Pawn(1, 6, WHITE)
    pawn6 = Pawn(4, 1, BLACK)
    pawn7 = Pawn(4, 3, BLACK)
    pawn8 = Pawn(4, 4, WHITE)
    pawn9 = Pawn(5, 4, BLACK)
    fanorona.pawns = Pawns([
        pawn1, pawn2, pawn3, pawn4, pawn5, pawn6, pawn7, pawn8, pawn9
        ])
    fanorona.selected_pawn = Best_pawn_picker._calc_best_pawn_to_pick(fanorona)
    best_move_with = Best_move_picker._calc_best_withdrawal_move(fanorona)
    best_move_app = Best_move_picker._calc_best_approach_move(fanorona)
    assert best_move_app == (0, None)
    assert best_move_with == (3, (4, 5))
    # pawn will capture 3 enemy's pawn by withdrawal
    # if he moves to (4, 5)


def test_best_move_picker_calc_double():
    fanorona = Fanorona()
    fanorona.turn = WHITE
    fanorona.pawns.pawns.clear()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(3, 2, BLACK)
    pawn3 = Pawn(4, 2, BLACK)
    pawn4 = Pawn(1, 4, BLACK)
    pawn5 = Pawn(1, 6, WHITE)
    pawn7 = Pawn(4, 3, BLACK)
    pawn8 = Pawn(4, 4, WHITE)
    pawn9 = Pawn(5, 4, BLACK)
    pawn10 = Pawn(2, 4, BLACK)
    fanorona.pawns = Pawns([
        pawn1, pawn2, pawn3, pawn4, pawn5, pawn7, pawn8, pawn9, pawn10
        ])
    fanorona.selected_pawn = Best_pawn_picker._calc_best_pawn_to_pick(fanorona)
    # pawn1 is the first pawn in fanorona.pawns that
    # has possible two-pawn capture
    assert fanorona.selected_pawn == pawn1
    best_move_with = Best_move_picker._calc_best_withdrawal_move(fanorona)
    assert best_move_with[0] == 0
    best_move_app = Best_move_picker._calc_best_approach_move(fanorona)
    assert best_move_app[0] == 2
    assert best_move_app[1] == (2, 2)


def test_best_move_picker_calc_double_test_forced():
    fanorona = Fanorona()
    fanorona.turn = WHITE
    fanorona.pawns.pawns.clear()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(3, 2, BLACK)
    pawn3 = Pawn(4, 2, BLACK)
    pawn4 = Pawn(1, 4, BLACK)
    pawn5 = Pawn(1, 6, WHITE)
    pawn7 = Pawn(4, 3, BLACK)
    pawn8 = Pawn(4, 4, WHITE)
    pawn9 = Pawn(5, 4, BLACK)
    pawn10 = Pawn(2, 4, BLACK)
    fanorona.pawns = Pawns([
        pawn1, pawn2, pawn3, pawn4, pawn5, pawn7, pawn8, pawn9, pawn10
        ])
    fanorona.selected_pawn = pawn8
    best_move_with = Best_move_picker._calc_best_withdrawal_move(fanorona)
    assert best_move_with[0] == 2
    assert best_move_with[1] == (4, 5)
    best_move_app = Best_move_picker._calc_best_approach_move(fanorona)
    assert best_move_app[0] == 2
    assert best_move_app[1] == (3, 4)
