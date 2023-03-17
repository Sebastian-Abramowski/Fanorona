import pygame
from random import choice
from constants import BLACK, BOT_DELAY
from fanorona import Fanorona


class FanoronaBot:
    """
    Class used for imitating the player in the game of Fanorona

    ...
    Static methods
    (no need to create an instance of this class)
    --------------
    make_random_move(window, fanorona: "Fanorona", move_sound=False)
        takes window (pygame.display), an instance
        of fanorona game (class Fanorona) an optional
        move_sound as arguments

        imitate the player with colour of pawns BLACK and makes random
        allowed moves during his turn
    make_good_move(window, fanorona: "Fanorona", move_sound=False)
        takes window (pygame.display), an instance
        of fanorona game (class Fanorona) an optional
        move_sound as arguments

        imitate the player with colour of pawns BLACK and makes allowed moves
        that capture the most enemy's pawns
    make_paika_move(window, fanorona: "Fanorona", move_sound=False)
        takes window (pygame.display), an instance
        of fanorona game (class Fanorona) an optional
        move_sound as arguments

        imitate the player with colour of pawns BLACK and makes random
        paika moves only one time, this method is used for imitating the
        player on Board 3x3 (Fanorona on board 3x3 have different rules)
    the_best_move_turn(window, fanorona: "Fanorona", move_sound=False)
        takes a turn and picks capture that would pick the most enemy's pawn

        this function helps make_good_move function
    random_move_turn(window, fanorona: "Fanorona", move_sound=False)
        takes a turn, picks random allowed capture or paika move if no
        capture is available

        this function helps make_random_move_function
    """

    @staticmethod
    def make_random_move(window, fanorona: "Fanorona", move_sound=False):
        """Imitate the player and makes random allowed moves during his turn"""
        while fanorona.turn == BLACK:
            # if there is a capture at the start or capturing keeps on
            if fanorona.able_to_capture or fanorona.change is False:
                if fanorona.change is True:
                    picked = choice(fanorona.able_to_capture)
                    fanorona.pick_your_pawn(picked)
                    fanorona.printer.draw(window)
                    pygame.display.update()
                fanorona.printer.draw(window)
                pygame.display.update()
                pygame.time.delay(BOT_DELAY)
                FanoronaBot.random_move_turn(
                    window, fanorona, move_sound)
                pygame.time.delay(BOT_DELAY)
            else:
                try_to_pick = True
                while try_to_pick:
                    fanorona.pick_your_pawn(choice(fanorona.pawns.pawns))
                    if fanorona.possibilities:
                        fanorona.printer.draw_hints(window)
                        pygame.display.update()
                        pygame.time.delay(500)
                        x, y = choice(fanorona.possibilities)
                        fanorona.turn_paika(x, y, move_sound)
                        try_to_pick = False
            fanorona.printer.draw(window)
            pygame.display.update()

    @staticmethod
    def make_random_paika_move(window, fanorona: "Fanorona", move_sound=False):
        """
        Imitate the player and makes random allowed paika moves
        during his turn

        Hint: made for playing on 3x3 board (
            there are no captures on this board)
        """
        if fanorona.turn == BLACK:
            try_to_pick = True
            while try_to_pick:
                picked = choice(fanorona.pawns.pawns)
                fanorona.pick_your_pawn(picked)
                if fanorona.possibilities:
                    try_to_pick = False
            fanorona.printer.draw(window)
            pygame.display.update()
            pygame.time.delay(BOT_DELAY)
            x, y = choice(fanorona.possibilities)
            fanorona.turn_paika(x, y, move_sound)
            pygame.time.delay(BOT_DELAY)

    @staticmethod
    def make_good_move(window, fanorona: "Fanorona", move_sound=False):
        """
        Imitate the player and makes good allowed moves during his turn
        depending on the number of possible captures
        """
        while fanorona.turn == BLACK:
            # if there is a capture at the start or capturing keeps on
            if fanorona.able_to_capture or fanorona.change is False:
                if fanorona.change is True:
                    picked = Best_pawn_picker._calc_best_pawn_to_pick(fanorona)
                    fanorona.pick_your_pawn(picked)
                    fanorona.printer.draw(window)
                    pygame.display.update()
                fanorona.printer.draw(window)
                pygame.display.update()
                pygame.time.delay(BOT_DELAY)
                FanoronaBot.the_best_move_turn(
                    window, fanorona, move_sound)
                pygame.time.delay(BOT_DELAY)
            else:
                try_to_pick = True
                while try_to_pick:
                    fanorona.pick_your_pawn(choice(fanorona.pawns.pawns))
                    if fanorona.possibilities:
                        fanorona.printer.draw_hints(window)
                        pygame.display.update()
                        pygame.time.delay(500)
                        x, y = choice(fanorona.possibilities)
                        fanorona.turn_paika(x, y, move_sound)
                        try_to_pick = False
            fanorona.printer.draw(window)
            pygame.display.update()

    def the_best_move_turn(window, fanorona: "Fanorona", move_sound=False):
        cond1 = fanorona.capturing_moves_approach
        cond2 = fanorona.capturing_moves_withdrawal
        if cond1 and cond2:
            bmp_app = Best_move_picker._calc_best_approach_move(
                fanorona)
            bmp_with = Best_move_picker._calc_best_withdrawal_move(
                fanorona)
            best_approach_move = bmp_app
            best_withdrawal_move = bmp_with

            if best_approach_move[0] > best_withdrawal_move[0]:
                x, y = best_approach_move[1]
                fanorona.turn_approach(x, y, move_sound)
            elif best_withdrawal_move[0] > best_approach_move[0]:
                x, y = best_withdrawal_move[1]
                fanorona.turn_withdrawal(x, y, move_sound)
            else:
                pick_capture = choice([
                    best_approach_move,
                    best_withdrawal_move
                    ])
                if pick_capture == best_withdrawal_move:
                    x, y = best_withdrawal_move[1]
                    fanorona.turn_withdrawal(x, y, move_sound)
                else:
                    x, y = best_approach_move[1]
                    fanorona.turn_approach(x, y, move_sound)
        elif fanorona.capturing_moves_approach:
            x, y = Best_move_picker._calc_best_approach_move(
                fanorona)[1]
            fanorona.turn_approach(x, y, move_sound)
        elif fanorona.capturing_moves_withdrawal:
            x, y = Best_move_picker._calc_best_withdrawal_move(
                fanorona)[1]
            fanorona.turn_withdrawal(x, y, move_sound)

    def random_move_turn(window, fanorona: "Fanorona", move_sound=False):
        cond1 = fanorona.capturing_moves_approach
        cond2 = fanorona.capturing_moves_withdrawal
        if cond1 and cond2:
            pick_capture = choice([
                fanorona.capturing_moves_withdrawal,
                fanorona.capturing_moves_approach
                ])
            if pick_capture == fanorona.capturing_moves_withdrawal:
                x, y = choice(fanorona.capturing_moves_withdrawal)
                fanorona.turn_withdrawal(x, y, move_sound)
            else:
                x, y = choice(fanorona.capturing_moves_approach)
                fanorona.turn_approach(x, y, move_sound)
        elif fanorona.capturing_moves_approach:
            x, y = choice(fanorona.capturing_moves_approach)
            fanorona.turn_approach(x, y, move_sound)
        elif fanorona.capturing_moves_withdrawal:
            x, y = choice(fanorona.capturing_moves_withdrawal)
            fanorona.turn_withdrawal(x, y, move_sound)
        else:
            x, y = choice(fanorona.possibilities)
            fanorona.turn_paika(x, y, move_sound)


class Best_move_picker:
    """
    Class used for picking best move in Fanorona game

    ...
    Static methods
    (no need to create an instance of this class)
    --------------
    _calc_best_approach_move(fanorona: "Fanorona")
        calculate the best approach move (that would capture the most pawns)
        and returns number of possible capture and row, col where pawn
        should move in order to make a capture
        e.g. (2, (3, 5))
    _calc_best_withdrawal_move(fanorona: "Fanorona")
        calculate the best withdrawal move (that would capture the most pawns)
        and returns number of possibe axpture and row, col where pawn should
        move in oder to make that capture
        e.g. (1, (4, 5))
    """

    @staticmethod
    def _calc_best_approach_move(fanorona: "Fanorona"):
        """
        Calculates the approach move that captures the most pawns,
        return (number of possible captures, (row, col))

        (row, col) indicate the place where pawn should be moved to make
        that capture
        """
        best_approach_move = (0, None)
        fanorona.update_possible_captures()

        for row, col in fanorona.capturing_moves_approach:
            potencial_captured = fanorona.logic.capture_by_approach(row, col)
            cond2 = len(potencial_captured) > best_approach_move[0]
            if best_approach_move[1] is None or cond2:
                best_approach_move = (len(potencial_captured), (row, col))

        return best_approach_move

    @staticmethod
    def _calc_best_withdrawal_move(fanorona: "Fanorona"):
        """
        Calculates the withdrawal move that captures the most pawns,
        return (number of possible captures, (row, col))

        (row, col) indicate the place where pawn should be moved to make
        that capture
        """
        best_withdrawal_move = (0, None)
        fanorona.update_possible_captures()

        for row, col in fanorona.capturing_moves_withdrawal:
            potencial_captured = fanorona.logic.capture_by_withdrawal(row, col)
            cond2 = len(potencial_captured) > best_withdrawal_move[0]
            if best_withdrawal_move[1] is None or cond2:
                best_withdrawal_move = (len(potencial_captured), (row, col))

        return best_withdrawal_move


class Best_pawn_picker:
    """
    Class used for picking the best pawn at the start of the round

    ...
    Static method
    (no need to create an instance of this class)
    --------------
    _calc_best_pawn_to_pick(fanorona: "Fanorona")
        calculate the best pawn to pick depending on the number of possible
        captures

        method should be called at the start of every round  to pick the best
        pawn
    """

    @staticmethod
    def _calc_best_pawn_to_pick(fanorona: "Fanorona"):
        """
        Calculates the best pawn to pick at the start of the round,
        returns an instance of Pawn that should be picked
        """
        best_pawn = (0, None)
        fanorona.update_able_to_capture()

        if fanorona.able_to_capture:
            for pawn in fanorona.able_to_capture:
                if pawn.colour == fanorona.turn:
                    fanorona.selected_pawn = pawn

                    poss = fanorona.logic.possibilities_of_pawn(pawn)
                    for x, y in poss:
                        num_of_cap1 = len(fanorona.logic.capture_by_approach(
                            x, y))
                        num_of_cap2 = len(fanorona.logic.capture_by_withdrawal(
                            x, y))

                        num_max = max(num_of_cap1, num_of_cap2)
                        if num_max > best_pawn[0]:
                            best_pawn = (num_max, pawn)

        fanorona.clear_able_to_capture()
        fanorona.selected_pawn = None
        # clearing selected_pawn since we set it in order to use
        # fanorona.logic.capture_by_approach/withdrawal
        return best_pawn[1]
