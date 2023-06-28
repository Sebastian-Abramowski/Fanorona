import pygame
from board import Board
from pawn import Pawn
from pawns import Pawns
from fanorona import Fanorona
from constants import RED, FPS, ROWS, COLS, BLACK
from constants import SOUND_EFFECTS, MIN_WIDTH, MIN_HEIGHT
from bot import FanoronaBot
from constants import MainArguemntRandomException
from constants import MainArguemntCompException
from user_interface import user_interface

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Fanorona")

# loading sounds
game_start_sound = pygame.mixer.Sound("Audio/board-start-sound.wav")
game_start_sound.set_volume(0.3)
move_sound = pygame.mixer.Sound("Audio/move-sound2.wav")
move_sound.set_volume(0.3)
win_sound = pygame.mixer.Sound("Audio/win-sound.wav")
win_sound.set_volume(0.3)


def determine_clicked_square(board: "Board", pawns: "Pawns"):
    """
    Returns either an instance of clicked Pawn or tuple - center of
    clicked Rect (square box)

    Should be called after click event
    """
    mouse_pos = pygame.mouse.get_pos()
    for rectangles_row in board.rectangles_boxes:
        for rectangle in rectangles_row:
            if rectangle.collidepoint(mouse_pos):
                for pawn in pawns.pawns:
                    center_of_pawn = pawn._take_the_center_of_pawn(board)
                    if rectangle.center == center_of_pawn:
                        return pawn
                return rectangle.center


def main_comp(comp=0, random=0):
    """
    Main function for playing fanorona on board
    different from 3x3;

    comp = 0 and random = 0 means playing with two players (DEFAULT)

    comp = 1 and random = 1 means playing vs computer that
    makes random moves

    comp = 1 and random = 0 means playing vs computer that makes
    good moves depending on the number of possible captures
    """
    if comp not in [0, 1]:
        raise MainArguemntCompException()
    if random not in [0, 1]:
        raise MainArguemntRandomException()

    window = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)

    clock = pygame.time.Clock()
    fanorona = Fanorona()
    play = True

    if SOUND_EFFECTS == 1:
        game_start_sound.play(0)  # 0 means play one time

    while play:
        clock.tick(FPS)
        window.fill(RED)

        fanorona.printer.draw(window)

        if fanorona.logic.check_for_winner():
            if SOUND_EFFECTS == 1:
                win_sound.play(0)
            fanorona.printer.draw_winner(window)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if fanorona.round == 1:
                        if fanorona.selected_pawn is None:
                            fanorona.change_turn()
                            if comp == 1:
                                pygame.time.set_timer(pygame.USEREVENT, 250)
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                # setting the minimal screen size
                if width < MIN_WIDTH:
                    width = MIN_WIDTH
                if height < MIN_HEIGHT:
                    height = MIN_HEIGHT
                window = pygame.display.set_mode(
                    (width, height), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    board = fanorona.board
                    pawns = fanorona.pawns
                    clicked_pawn_or_center_empty_space = (
                        determine_clicked_square(board, pawns)
                        )
                    if isinstance(clicked_pawn_or_center_empty_space, Pawn):
                        clicked_pawn = clicked_pawn_or_center_empty_space
                        if ROWS == 3 and COLS == 3:
                            if fanorona.turn == clicked_pawn.colour:
                                fanorona.pick_your_pawn(clicked_pawn)
                        else:
                            if fanorona.problematic_cap is False:
                                fanorona.pick_your_pawn(clicked_pawn)
                            else:
                                clicked_row = clicked_pawn.row
                                clicked_col = clicked_pawn.column

                                fanorona.turn_problematic_move(
                                    clicked_row, clicked_col, move_sound)
                                if fanorona.turn == BLACK and comp == 1:
                                    pygame.time.set_timer(
                                        pygame.USEREVENT, 500)

                    elif isinstance(clicked_pawn_or_center_empty_space, tuple):
                        center_empty_space = clicked_pawn_or_center_empty_space
                        x, y = board.row_col_from_center_of_square(
                                center_empty_space)
                        clicked_row, clicked_col = x, y
                        if ROWS == 3 and COLS == 3:
                            if fanorona.selected_pawn is not None:
                                possibilities = fanorona.possibilities
                                if (clicked_row, clicked_col) in possibilities:
                                    fanorona.turn_paika(
                                            clicked_row, clicked_col,
                                            move_sound)
                                if comp == 1:
                                    pygame.time.set_timer(
                                        pygame.USEREVENT, 400)
                        else:
                            if fanorona.selected_pawn is not None:
                                capt_mv_w = fanorona.capturing_moves_withdrawal
                                cond2 = (clicked_row, clicked_col) in capt_mv_w
                                capt_mv_ap = fanorona.capturing_moves_approach
                                cond1 = (clicked_row, clicked_col) in capt_mv_ap
                                if cond1 and cond2:
                                    # indicate problematic capture
                                    fanorona.indicate_problematic_capture(
                                        clicked_row, clicked_col)
                                else:
                                    if fanorona.capturing_moves_withdrawal:
                                        fanorona.turn_withdrawal(
                                            clicked_row, clicked_col,
                                            move_sound)
                                        if fanorona.turn == BLACK and comp == 1:
                                            pygame.time.set_timer(
                                                pygame.USEREVENT, 400)

                                    if fanorona.capturing_moves_approach:
                                        fanorona.turn_approach(
                                            clicked_row, clicked_col,
                                            move_sound)
                                        if fanorona.turn == BLACK and comp == 1:
                                            pygame.time.set_timer(
                                                pygame.USEREVENT, 400)

                                    c1 = not fanorona.capturing_moves_withdrawal
                                    c2 = not fanorona.capturing_moves_approach
                                    if c1 and c2:
                                        # paika move
                                        fanorona.turn_paika(
                                            clicked_row, clicked_col, move_sound)
                                        if fanorona.turn == BLACK and comp == 1:
                                            pygame.time.set_timer(
                                                pygame.USEREVENT, 400)
            if event.type == pygame.USEREVENT:
                if ROWS == 3 and COLS == 3:
                    FanoronaBot.make_random_paika_move(
                        window, fanorona, move_sound)
                else:
                    fanorona.update_able_to_capture()
                    if random == 0:
                        FanoronaBot.make_good_move(window, fanorona, move_sound)
                    else:
                        FanoronaBot.make_random_move(window, fanorona, move_sound)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    comp, rand = user_interface()
    """
    because of taking inputs, now application such as vs code
    has focus, so pygame display is shown below it on the screen
    """
    main_comp(comp, rand)
