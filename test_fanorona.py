from fanorona import Fanorona
from board import Board
from pawns import Pawns
from pawn import Pawn
from fanorona import FanoronaPrinter, FanoronaLogic
from constants import WHITE, BLACK


def test_init():
    fanorona = Fanorona()
    assert isinstance(fanorona.board, Board) is True
    assert isinstance(fanorona.pawns, Pawns) is True
    assert isinstance(fanorona.printer, FanoronaPrinter) is True
    assert isinstance(fanorona.logic, FanoronaLogic) is True
    assert fanorona.selected_pawn is None
    assert fanorona.turn == WHITE
    assert isinstance(fanorona.possibilities, list) is True
    assert isinstance(fanorona.capturing_moves_approach, list) is True
    assert isinstance(fanorona.capturing_moves_withdrawal, list) is True
    assert fanorona.round == 1
    assert fanorona.change is True
    assert isinstance(fanorona.where_was_pawn, list) is True
    assert isinstance(fanorona.able_to_capture, list) is True
    assert fanorona.last_move is None
    assert fanorona.problematic_cap is False
    assert isinstance(fanorona.approach_choices, list) is True
    assert isinstance(fanorona.withdrowal_choices, list) is True


def test_highlight_clicked():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 4, WHITE, True)
    fanorona.pawns = Pawns([pawn1, pawn2])
    assert pawn2.if_selected is True
    fanorona.highlight_clicked(pawn1)
    assert pawn2.if_selected is False
    assert pawn1.if_selected is True
    assert fanorona.selected_pawn == pawn1


def test_move_selected_piece():
    fanorona = Fanorona()
    pawn = Pawn(1, 2, WHITE)
    fanorona.selected_pawn = pawn
    fanorona.move_selected_piece(2, 3)
    assert pawn.row == 2
    assert pawn.column == 3


def test_remove_captured_and_count():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, BLACK)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3 = Pawn(1, 5, WHITE)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3])
    fanorona.pawns.whites = 1
    fanorona.pawns.blacks = 2
    fanorona.selected_pawn = pawn3
    fanorona.remove_captured_and_count([(pawn1.row, pawn1.column),
                                        (pawn2.row, pawn2.column)])
    assert fanorona.pawns.blacks == 0
    assert len(fanorona.pawns.pawns) == 1


def test_move_and_capture_by_approach():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, BLACK)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3 = Pawn(1, 5, WHITE)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3])
    fanorona.pawns.whites = 1
    fanorona.pawns.blacks = 2
    fanorona.selected_pawn = pawn3
    fanorona.move_and_capture_by_approach(1, 4)
    assert fanorona.pawns.blacks == 0
    assert fanorona.last_move == 'W'
    assert fanorona.selected_pawn.column == 4
    assert fanorona.where_was_pawn == [(1, 4)]
    assert len(fanorona.able_to_capture) == 0


def test_move_and_capture_by_withdrawal():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, BLACK)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3 = Pawn(1, 4, WHITE)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3])
    fanorona.pawns.whites = 1
    fanorona.pawns.blacks = 2
    fanorona.selected_pawn = pawn3
    fanorona.move_and_capture_by_withdrawal(1, 5)
    assert fanorona.pawns.blacks == 0
    assert fanorona.last_move == 'E'
    assert fanorona.selected_pawn.column == 5
    assert fanorona.where_was_pawn == [(1, 5)]
    assert len(fanorona.able_to_capture) == 0


def test_empty_space_validator():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2])
    fanorona.selected_pawn = pawn1
    fanorona.possibilities = [(1, 3), (2, 2), (1, 1)]
    fanorona.empty_space_validator()
    assert fanorona.possibilities == [(2, 2), (1, 1)]


def test_last_move_validator():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2])
    fanorona.selected_pawn = pawn1
    fanorona.possibilities = [(1, 3), (2, 2), (1, 1)]
    fanorona.last_move = "W"
    fanorona.last_move_validator()
    assert fanorona.possibilities == [(1, 3), (2, 2)]


def test_capturing_moves_validator():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2])
    fanorona.selected_pawn = pawn1
    fanorona.capturing_moves_approach = []
    fanorona.capturing_moves_withdrawal = [(1, 1)]
    fanorona.where_was_pawn = [(1, 1)]
    fanorona.capturing_moves_validator()
    assert len(fanorona.capturing_moves_withdrawal) == 0


def test_reset():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2])
    fanorona.turn = BLACK
    fanorona.reset()
    assert fanorona.turn == WHITE
    assert len(fanorona.pawns.pawns) > 2


def test_next_round():
    fanorona = Fanorona()
    fanorona.round = 2
    fanorona.next_round()
    assert fanorona.round == 3


def test_change_turn():
    fanorona = Fanorona()
    fanorona.turn = WHITE
    fanorona.change_turn()
    assert fanorona.turn == BLACK


def test_return_able_to_capture():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2])
    assert fanorona.return_able_to_capture() == [pawn1, pawn2]


def test_last_move():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    fanorona.pawns = Pawns([pawn1])
    fanorona.selected_pawn = pawn1
    assert fanorona.last_move is None
    fanorona.update_last_move(1, 3)
    assert fanorona.last_move == 'E'


def test_update_possibilities():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2])
    fanorona.selected_pawn = pawn1
    fanorona.possibilities = [(1, 3), (2, 2), (1, 1)]
    fanorona.last_move = "W"
    fanorona.update_possibilities() == [(2, 2)]


def test_update_possible_captures():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3 = Pawn(1, 4, BLACK)
    pawn4 = Pawn(3, 2, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3, pawn4])
    fanorona.selected_pawn = pawn1
    fanorona.update_possible_captures()
    assert fanorona.capturing_moves_approach == [(2, 2)]
    assert fanorona.capturing_moves_withdrawal == [(1, 1)]
    fanorona.where_was_pawn = [(1, 1)]
    fanorona.update_possible_captures()
    assert len(fanorona.capturing_moves_withdrawal) == 0


def test_update_able_to_capture():
    fanorona = Fanorona()
    fanorona.turn = WHITE
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2])
    assert fanorona.return_able_to_capture() == [pawn1, pawn2]
    fanorona.update_able_to_capture()
    assert fanorona.able_to_capture == [pawn1]
    assert pawn1.if_capture is True


def test_update_turn_approach():
    fanorona = Fanorona()
    fanorona.round = 1
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3 = Pawn(1, 4, BLACK)
    pawn4 = Pawn(3, 2, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3, pawn4])
    fanorona.selected_pawn = pawn1
    fanorona.update_possible_captures()
    fanorona.turn_approach(2, 2)
    assert fanorona.round == 2
    assert len(fanorona.pawns.pawns) == 3
    assert pawn1.column == 2
    assert fanorona.turn == BLACK
    assert len(fanorona.where_was_pawn) == 0
    assert len(fanorona.possibilities) == 0


def test_update_turn_approach_not_the_end_of_the_round():
    fanorona = Fanorona()
    fanorona.round = 3
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3 = Pawn(1, 4, BLACK)
    pawn4 = Pawn(3, 2, BLACK)
    pawn5 = Pawn(2, 4, BLACK)
    pawn6 = Pawn(1, 1, WHITE)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3, pawn4, pawn5, pawn6])
    fanorona.selected_pawn = pawn1
    fanorona.update_possible_captures()
    fanorona.turn_approach(2, 2)
    fanorona.last_move = 'S'
    fanorona.where_was_pawn = [(1, 2)]
    assert fanorona.round == 3
    assert fanorona.capturing_moves_approach == [(2, 3)]
    assert fanorona.possibilities == [(1, 2), (2, 1), (2, 3), (3, 3), (3, 1)]
    assert fanorona.change is False


def test_update_turn_withdrawal():
    fanorona = Fanorona()
    fanorona.round = 1
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3 = Pawn(1, 4, BLACK)
    pawn4 = Pawn(3, 2, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3, pawn4])
    fanorona.selected_pawn = pawn1
    fanorona.update_possible_captures()
    fanorona.turn_withdrawal(1, 1)
    assert fanorona.round == 2
    assert len(fanorona.pawns.pawns) == 2
    assert pawn1.column == 1
    assert fanorona.turn == BLACK
    assert len(fanorona.where_was_pawn) == 0
    assert len(fanorona.possibilities) == 0


def test_update_turn_withdrawal_not_the_end_of_the_round():
    fanorona = Fanorona()
    fanorona.round = 3
    pawn1 = Pawn(1, 2, WHITE)
    pawn2 = Pawn(1, 3, BLACK)
    pawn3 = Pawn(1, 4, BLACK)
    pawn4 = Pawn(3, 2, BLACK)
    pawn5 = Pawn(3, 1, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3, pawn4, pawn5])
    fanorona.selected_pawn = pawn1
    fanorona.update_possible_captures()
    fanorona.turn_withdrawal(1, 1)
    fanorona.last_move = 'W'
    fanorona.where_was_pawn = [(1, 2)]
    assert fanorona.round == 3
    assert fanorona.capturing_moves_approach == [(2, 1)]
    assert len(fanorona.capturing_moves_withdrawal) == 0
    assert fanorona.possibilities == [(2, 1), (2, 2), (1, 2)]
    print(fanorona.possibilities)
    assert fanorona.change is False


def test_register_poss_of_pawn():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 2, WHITE)
    fanorona.selected_pawn = pawn1
    fanorona.register_poss_of_pawn()
    assert fanorona.where_was_pawn == [(1, 2)]


def test_problematic_move_withdrawal():
    fanorona = Fanorona()
    fanorona.round = 4
    pawn1 = Pawn(1, 1, BLACK)
    pawn2 = Pawn(1, 2, WHITE)
    pawn3 = Pawn(1, 4, BLACK)
    pawn4 = Pawn(1, 5, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3, pawn4])
    fanorona.selected_pawn = pawn2
    fanorona.indicate_problematic_capture(1, 3)
    assert fanorona.approach_choices == [(1, 4), (1, 5)]
    assert fanorona.withdrowal_choices == [(1, 1)]

    fanorona.turn_problematic_move(1, 1)
    assert fanorona.round == 5
    assert len(fanorona.pawns.pawns) == 3
    assert pawn1 not in fanorona.pawns.pawns
    assert len(fanorona.able_to_capture) == 0
    assert fanorona.problematic_cap is False


def test_problematic_move_approach():
    fanorona = Fanorona()
    fanorona.round = 4
    pawn1 = Pawn(1, 1, BLACK)
    pawn2 = Pawn(1, 2, WHITE)
    pawn3 = Pawn(1, 4, BLACK)
    pawn4 = Pawn(1, 5, BLACK)
    pawn5 = Pawn(3, 3, BLACK)
    fanorona.pawns = Pawns([pawn1, pawn2, pawn3, pawn4, pawn5])
    fanorona.selected_pawn = pawn2
    fanorona.indicate_problematic_capture(1, 3)
    assert fanorona.approach_choices == [(1, 4), (1, 5)]
    assert fanorona.withdrowal_choices == [(1, 1)]

    fanorona.turn_problematic_move(1, 5)
    assert fanorona.round == 4
    assert len(fanorona.pawns.pawns) == 3
    assert pawn3 not in fanorona.pawns.pawns
    assert len(fanorona.able_to_capture) == 0
    assert fanorona.problematic_cap is False
    assert len(fanorona.capturing_moves_approach) == 1
    assert len(fanorona.capturing_moves_withdrawal) == 0
    assert fanorona.possibilities == [(2, 3), (2, 4), (2, 2), (1, 2)]


def test_end_of_turn_conf():
    fanorona = Fanorona()
    fanorona.round = 4
    fanorona.turn = WHITE
    fanorona.possibilities = [(1, 1), (1, 2)]
    fanorona.where_was_pawn = [(2, 2), (2, 3)]
    fanorona.capturing_moves_approach = [(1, 1)]
    fanorona.capturing_moves_withdrawal = [(1, 2), (1, 3)]
    fanorona.change = False
    fanorona.last_move = 'NW'
    fanorona.end_of_turn_conf()
    assert fanorona.round == 5
    assert fanorona.turn == BLACK
    assert len(fanorona.possibilities) == 0
    assert len(fanorona.where_was_pawn) == 0
    assert len(fanorona.capturing_moves_approach) == 0
    assert len(fanorona.capturing_moves_withdrawal) == 0
    assert fanorona.change is True
    assert fanorona.last_move is None


def test_clear_possibilities():
    fanorona = Fanorona()
    fanorona.possibilities = [(1, 1), (1, 2)]
    fanorona.clear_possibilities()
    assert len(fanorona.possibilities) == 0


def test_clear_capturing_moves():
    fanorona = Fanorona()
    fanorona.capturing_moves_approach = [(1, 1)]
    fanorona.capturing_moves_withdrawal = [(1, 2), (1, 3)]
    fanorona.clear_capturing_moves()
    assert len(fanorona.capturing_moves_approach) == 0
    assert len(fanorona.capturing_moves_withdrawal) == 0


def test_clear_highlighted():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 1, WHITE)
    fanorona.selected_pawn = pawn1
    pawn2 = Pawn(1, 2, WHITE)
    pawn2.if_selected = True
    fanorona.pawns = Pawns([pawn1, pawn2])
    fanorona.clear_highlighted()
    assert pawn2.if_selected is False
    assert fanorona.selected_pawn is None


def test_clear_where_was_pawn():
    fanorona = Fanorona()
    fanorona.where_was_pawn = [(1, 1), (1, 2)]
    fanorona.clear_where_was_pawn()
    assert len(fanorona.where_was_pawn) == 0


def test_clear_able_to_capture():
    fanorona = Fanorona()
    pawn1 = Pawn(1, 1, WHITE)
    pawn2 = Pawn(1, 2, WHITE)
    pawn2.if_capture = True
    pawn1.if_capture = True
    fanorona.pawns = Pawns([pawn1, pawn2])
    fanorona.able_to_capture = [pawn1, pawn2]
    fanorona.clear_able_to_capture()
    assert len(fanorona.able_to_capture) == 0
    assert pawn2.if_capture is False
    assert pawn1.if_capture is False
