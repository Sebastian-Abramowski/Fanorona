import pygame
from pawn import Pawn
from board import Board
from pawns import Pawns
from constants import BLACK, WHITE, GREEN, RED2, ORANGE
from constants import FONT, ROWS, COLS, FONT_SMALL
from constants import IF_DRAW_NUM_OF_ROUND, SOUND_EFFECTS
from constants import BLACK2, WHITE2, PINK, YELLOW
from constants import is_even
from copy import deepcopy
from constants import WrongUseOfCaptureByAppOrWithFunc


class NoWinnerError(Exception):
    def __init__(self):
        super().__init__("Cannot draw winner if there is no winner")


class Fanorona:
    """
    Class used for representing Fanorona game

    ...
    Attributes
    ----------
    board:
        an instance of class Board
    pawns:
        an instance of class Pawns
    printer:
        an instance of class FanoronaPrinter
    logic:
        an instance of class FanoronaLogic
    selected_pawn: an instance of class Pawn
        an instance of class Pawn if some pawn is selected,
        if nothing is selected - None
    turn: tuple - (x, y, z)
        holds the colour of pawns that can be moved,
        either WHITE - (255, 255, 255) or BLACK - (0, 0, 0)
    possiblilities: list
        list of tuples - (row, column) that represents the places
        where the selected Pawn can be moved (empty boxes along the
        lines)
    round: int
        a number of round, default value is 1 (first round)
    change: bool
        informas if pawn can be changed, if it is False, it means
        that capturing continues
    where_was_pawn: list
        a list which informs about where was pawn during actual round
        e.g [(1, 2), (1, 3), (2, 3)]
    able_to_capture: list
        contains instances of Pawn that are able to capture some enemy's pawns;

        it is mainly used to highlight this pawns later at the start of the
        round
    last_move: string
        last_move of actually selected pawn, e.g 'N' means that
        self.selected_pawn was before moved into in 'N' direction

        it is mainly used to block not allowed captures, for example if pawn
        captures by moving to the right (withdrawal) and after that it
        can capture again by moving to the right (approach)
    problematic_cap: bool
        indicate if problematic capture was detected;
        problematic captures is capture that can be either by approach or
        withdrowal

        hint:
        it is needed to detect this capture since after that there is need
        for player to choose what he wants to capture
    approach_choices: list
        contains list of (row, col) that selected_pawn would capture by
        approach if he moves there

        it helps with problematic_capture (when player need to choose what he
        wants to capture)
    withdrowal_choices: list
        contains list of (row, col) that selected_pawn would capture by
        withdrawal if he moves there

        it helps with problematic_capture (when player need to choose what he
        wants to capture)

    Methods:
    -------
    highlight_clicked(clicked_pawn)
        clears highlighting and then highlights clicked_pawn
        (changes the Pawn 'if_selected' attribute)
    move_selected_piece(new_row, new_column)
        moves the selected Pawn to the square that matches
        new_row and new_column
    remove_captured_and_count(captured: "list")
        takes the list of (row, col) e.g [(1, 2), (3, 4)]
        and then removes pawns that matches that number of
        rows and column, plus updates attributes of
        self.pawns 'blacks' and 'whites' that hold information
        about number of pawns with some colour
    move_and_capture_by_approach(new_row, new_col)
        does everything connected to moving and capturing

        updating 'last_move' and 'where_was_pawn' attributes,
        calling remove_captured_and_count(), capturing by appraoch,
        moving
    move_and_capture_by_withdrawal(new_row, new_col)
        does everything connected to moving and capturing

        updating 'last_move' and 'where_was_pawn' attributes,
        calling remove_captured_and_count(), capturing by withdrawal,
        moving
    reset()
        resets the game by calling __init__ again,
        everything is as at the beginning
    empty_space_validator()
        updates 'possibilities' attribute, by removing not empty pawns
        from it
    last_move_validator()
        updates 'possibilities' attribute by removing these moves that
        would match 'last_move' attribute

        it it important since it is not allowed to move in the same
        directon twice
    capturing_moves_validator()
        updates 'capturing_moves_approach' and 'capturing_moves_withdrawal'
        attributes depending on the attribute 'where_was_pawn'

        it is important since captures can't be done by moving to
        the places the pawn was before on in the same round
    change_turn()
        changes the turn of the game (attribute 'turn')
    return_able_to_capture()
        returns the list of instance of Pawn that are able
        to capture
    update_last_move(new_row, new_col)
        updates 'last_move' attribute, takes row and col that
        pawn is moved into
    update_possibilities()
        if no Pawn is selected, returns None
        otherwise appends to attribute 'possibilities' allowed possible
        places e.g. [(1, 2), (2, 1)]
    update_possible_captures()
        updates 'capturing_moves_approach' and
        'capturing_moves_withdrawal' attributes

        if no pawn is selected, returns None
    update_able_to_capture()
        updates attribute 'able_to_capture' with instances of Pawn
        that are able to capture and matches the colour of the actual
        turn
    -------------
    turn_approach(n_row, n_col, move_sound=False)
    turn_withdrawal(n_row, n_col, move_sound=False)
        takes as arguments row, col where pawn should move and optionally
        move_sound (pygame.mixer.Sound), which will be played after calling
        this method

        this method is used to make one full turn, when we now that pawn
        will capture by APPROACH/WITHDRAWAL, it moves, captures and it
        takes care of the configuraton depending on the fact if the pawn
        can still capture or this is the end of the round or it's first
        or second round
    turn_paika(n_row, n_col, move_sound=False)
        takes as arguments row, col where pawn should move and optionally
        move_sound (pygame.mixer.Sound)

        this method is used to make one full turn, when we now that pawn
        will make paika move (no captures), it moves the pawn and takes care of
        configuration that should be done after the end of the round

        note that after paika move always will the end of the round
    turn_problematic_move(n_row, n_col, move_sound=False)
        takes as arguments row, col of clicked square and optionally
        move_sound (pygame.mixer.Sound)

        this method is used to make one full turn after problmatic capture
        (when player needs to choose what he wants to capture) and should
        be called on click.event after method that indicate problematic capture

        depending on passed row, col, it does nothing and waits or makes
        a capture by approach/withdrawal; it depends whether passed row, col
        is either in 'approach_choices' or 'withdrawal_choices'

        it also takes care of configuration after capture/the end of round
        just as turn_approach/turn_withdrawal methods
    pick_your_pawn(clicked_pawn)
        this method should be called after click.event on pawn

        if clicked pawn colour matches the actual turn, then it is selected,
        highlighted and 'possibilities' and possible captures are updated
    indicate_problematic_capture(ew_row, new_col)
        this method should be called after discovering problematic capture
        (when player needs to choose what he want to capture)

        main function of this method is to prepare for calling
        turn_problematic_move() method (mainly updating 'approach_choices'
        and 'withdrowal_choices' attributes)
    _sett_after_problematic_capture()
        this method should be called after calling turn_problematic_move()
        method, it clears after it and ends turn/prepares for next captures
    register_poss_of_pawn()
        after calling this method, current position of the pawn is added to
        'where_was_pawn' attribute e.g. (2, 5)
    end_of_turn_conf()
        should be called after every round, clears, changes rounds, turns and
        sets 'last_move' and 'change' attribute back to default
    clear_possibilities()
        clears 'possibilities' attribute
    clear_capturing_moves()
        clears 'capturing_moves_approach' and 'capturing_moves_withdrawal'
        attributes
    clear_highlighted()
        clears highlight of every pawn and changes 'selected_pawn' back to None
    clear_where_was_pawn()
        clears 'where_was_pawn' attribute
    clear_able_to_capture()
        clears 'able_to_capture' attribute and clears 'if_capture' attribute
        of every Pawn
    """
    def __init__(self):
        self.board = Board()
        self.pawns = Pawns()
        self.printer = FanoronaPrinter(self)
        self.logic = FanoronaLogic(self)
        self.selected_pawn = None
        self.turn = WHITE
        self.possibilities = []
        self.capturing_moves_approach = []
        self.capturing_moves_withdrawal = []
        self.round = 1
        self.change = True
        self.where_was_pawn = []
        self.able_to_capture = []
        self.last_move = None

        self.problematic_cap = False
        self.approach_choices = []
        self.withdrowal_choices = []

    def highlight_clicked(self, clicked_pawn):
        """
        Changes attribute 'if_selected' of clicked Pawn
        """
        self.pawns.highlight_pawn(clicked_pawn)
        self.selected_pawn = clicked_pawn

    def move_selected_piece(self, new_row, new_col):
        """
        Changes location of the selected pawn to the
        new_row and new_column, note that it doesn't
        check if the move is valid
        """
        if self.selected_pawn is not None:
            self.selected_pawn.move(new_row, new_col)

    def remove_captured_and_count(self, captured: list):
        count = len(captured)

        for row, col in captured:
            self.pawns.remove_pawn(row, col)

        if self.selected_pawn.colour == WHITE:
            self.pawns.blacks -= count
        else:
            self.pawns.whites -= count

    def move_and_capture_by_approach(self, new_row, new_col):
        """
        this method should be called when we now that capture by
        approach is possible
        """
        self.update_last_move(new_row, new_col)
        # print(self.last_move)
        captured = self.logic.capture_by_approach(new_row, new_col)
        self.remove_captured_and_count(captured)
        self.selected_pawn.move(new_row, new_col)
        self.where_was_pawn.append((new_row, new_col))
        self.clear_able_to_capture()
        # print(self.where_was_pawn)

    def move_and_capture_by_withdrawal(self, new_row, new_col):
        """
        this method should be called when we now that capture by
        withdrawal is possible
        """
        self.update_last_move(new_row, new_col)
        # print(self.last_move)
        captured = self.logic.capture_by_withdrawal(new_row, new_col)
        self.remove_captured_and_count(captured)
        self.selected_pawn.move(new_row, new_col)
        self.where_was_pawn.append((new_row, new_col))
        self.clear_able_to_capture()
        # print(self.where_was_pawn)

    def empty_space_validator(self):
        new_poss = self.logic.empty_space_validator_list(self.possibilities)
        self.possibilities = new_poss

    def last_move_validator(self):
        self.possibilities = self.logic.last_move_validator_poss()

    def capturing_moves_validator(self):
        cp_mv_app_copy = deepcopy(self.capturing_moves_approach)
        cp_mv_with_copy = deepcopy(self.capturing_moves_withdrawal)
        for row, col in self.capturing_moves_approach:
            if (row, col) in self.where_was_pawn:
                cp_mv_app_copy.remove((row, col))
        for row, col in self.capturing_moves_withdrawal:
            if (row, col) in self.where_was_pawn:
                cp_mv_with_copy.remove((row, col))
        self.capturing_moves_approach = cp_mv_app_copy
        self.capturing_moves_withdrawal = cp_mv_with_copy

    def reset(self):
        """Resets the game, calls init again"""
        self.__init__()

    def next_round(self):
        """Initializes a new game"""
        self.round += 1

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def return_able_to_capture(self):
        pawns_able_to_capture = []
        for pawn in self.pawns.pawns:
            poss = self.logic.possibilities_of_pawn(pawn)
            poss2 = self.logic.empty_space_validator_list(poss)
            cap1 = self.logic.possible_captures_approach(pawn, poss2)
            cap2 = self.logic.possible_captures_withdrowal(pawn, poss2)
            if cap1 or cap2:
                pawns_able_to_capture.append(pawn)
        return pawns_able_to_capture

    def update_last_move(self, new_row, new_col):
        last_move = self.logic.get_last_move(
            self.selected_pawn, new_row, new_col)
        self.last_move = last_move

    def update_possibilities(self):
        if self.selected_pawn is None:
            self.possibilities.clear()
            return None
        selected = self.selected_pawn
        poss = self.logic.possibilities_of_pawn(selected)
        self.possibilities = poss
        self.empty_space_validator()
        self.last_move_validator()

    def update_possible_captures(self):
        if self.selected_pawn is None:
            return None
        self.update_possibilities()  # just in case
        captures_app = self.logic.possible_captures_approach(
            self.selected_pawn, self.possibilities)
        captures_with = self.logic.possible_captures_withdrowal(
            self.selected_pawn, self.possibilities)
        self.capturing_moves_approach = captures_app
        self.capturing_moves_withdrawal = captures_with
        self.capturing_moves_validator()

    def update_able_to_capture(self):
        pawns_able_to_capture = self.return_able_to_capture()
        self.able_to_capture.clear()
        for pawn in pawns_able_to_capture:
            if pawn.colour == self.turn:
                self.able_to_capture.append(pawn)
                pawn.if_capture = True

    def turn_approach(self, n_row, n_col, move_sound=False):
        self.register_poss_of_pawn()
        capt_mv_ap = self.capturing_moves_approach
        if self.problematic_cap is False:
            if (n_row, n_col) in capt_mv_ap:
                self.move_and_capture_by_approach(
                    n_row, n_col)
                self.clear_possibilities()
                self.clear_capturing_moves()
                if SOUND_EFFECTS == 1 and move_sound is not False:
                    move_sound.play(0)

                self.update_possibilities()
                self.update_possible_captures()
                cond1 = self.capturing_moves_approach
                cond2 = self.capturing_moves_withdrawal
                cond3 = self.round in [1, 2]
                self.change = False
                self.clear_able_to_capture()
                if (not cond1 and not cond2) or cond3:
                    self.end_of_turn_conf()

    def turn_paika(self, n_row, n_col, move_sound=False):
        # in this case there is no point saving position of pawn
        # since there will be no more moves and the end of the round
        # after paika move
        if self.problematic_cap is False:
            if (n_row, n_col) in self.possibilities:
                self.move_selected_piece(n_row, n_col)

                if SOUND_EFFECTS == 1 and move_sound is not False:
                    move_sound.play(0)

                self.clear_able_to_capture()

                self.end_of_turn_conf()

    def turn_withdrawal(self, n_row, n_col, move_sound=False):
        if self.problematic_cap is False:
            self.register_poss_of_pawn()
            capt_mv_w = self.capturing_moves_withdrawal
            if (n_row, n_col) in capt_mv_w:
                self.move_and_capture_by_withdrawal(
                    n_row, n_col)
                self.clear_possibilities()
                self.clear_capturing_moves()
                if SOUND_EFFECTS == 1 and move_sound is not False:
                    move_sound.play(0)

                self.update_possibilities()
                self.update_possible_captures()
                cond1 = self.capturing_moves_approach
                cond2 = self.capturing_moves_withdrawal
                cond3 = self.round in [1, 2]
                self.change = False
                self.clear_able_to_capture()
                if (not cond1 and not cond2) or cond3:
                    self.end_of_turn_conf()

    def turn_problematic_move(self, n_row, n_col, move_sound=False):
        where_to_move = self.problematic_cap[1]

        def movement_after_problematic(type_of_capture):
            # type_of_capture - "APPROACH" / "WITHDRAWAL"
            self.register_poss_of_pawn()
            self.pawns._change_colours_to_default()
            # print(self.where_was_pawn)
            if type_of_capture == "WITHDRAWAL":
                self.move_and_capture_by_withdrawal(
                    where_to_move[0], where_to_move[1])
            else:
                self.move_and_capture_by_approach(
                    where_to_move[0], where_to_move[1])
            self._sett_after_problematic_capture()
            if SOUND_EFFECTS == 1 and move_sound is not False:
                move_sound.play(0)
            self.clear_able_to_capture()

        for row, col in self.withdrowal_choices:
            if row == n_row and col == n_col:
                movement_after_problematic("WITHDRAWAL")

        for row, col in self.approach_choices:
            if row == n_row and col == n_col:
                movement_after_problematic("APPROACH")

    def pick_your_pawn(self, clicked_pawn):
        if self.turn == clicked_pawn.colour:
            self.update_able_to_capture()
            # we needed to add this since we are now
            # clearing able_to_capture with draw function
            # because of previous bug
            if self.change is True:
                cond1 = clicked_pawn in self.able_to_capture
                cond2 = not self.able_to_capture
                if cond1 or cond2:
                    self.highlight_clicked(
                        clicked_pawn)
            # clearing list of possibilites just in case
                    self.clear_capturing_moves()
                    self.clear_possibilities()
                    self.update_possibilities()
                    if ROWS != 3 or COLS != 3:
                        self.update_possible_captures()

    def indicate_problematic_capture(self, new_row, new_col):
        if self.problematic_cap is False:
            self.problematic_cap = True, (new_row, new_col)
            captured1 = self.logic.capture_by_approach(new_row, new_col)
            captured2 = self.logic.capture_by_withdrawal(new_row, new_col)

            for row, col in captured1:
                pawn1 = self.pawns.row_column_pawn(row, col)
                if pawn1.colour == WHITE:
                    pawn1.colour = WHITE2
                else:
                    pawn1.colour = BLACK2
                if (row, col) not in self.where_was_pawn:
                    self.approach_choices.append((row, col))

            for row, col in captured2:
                pawn1 = self.pawns.row_column_pawn(row, col)
                if pawn1.colour == WHITE:
                    pawn1.colour = WHITE2
                else:
                    pawn1.colour = BLACK2
                if (row, col) not in self.where_was_pawn:
                    self.withdrowal_choices.append((row, col))
            # clearing highlights of pawns that can capture
            self.clear_able_to_capture()

    def _sett_after_problematic_capture(self):
        self.approach_choices.clear()
        self.withdrowal_choices.clear()
        self.problematic_cap = False

        self.clear_possibilities()
        self.clear_capturing_moves()
        self.update_possibilities()
        self.update_possible_captures()

        self.change = False
        cond3 = self.round in [1, 2]
        cond1 = self.capturing_moves_approach
        cond2 = self.capturing_moves_withdrawal

        if cond3 or (not cond1 and not cond2):
            self.end_of_turn_conf()

    def register_poss_of_pawn(self):
        """Notes current position of pawn to 'where_was_pawn'"""
        row = self.selected_pawn.row
        col = self.selected_pawn.column

        if (row, col) not in self.where_was_pawn:
            self.where_was_pawn.append((row, col))

    def end_of_turn_conf(self):
        self._clear_after_round()
        self.next_round()
        self.change_turn()
        self.change = True
        self.last_move = None

    def clear_possibilities(self):
        """Clears 'possibiliites' (list) attribute"""
        self.possibilities.clear()

    def clear_capturing_moves(self):
        self.capturing_moves_approach.clear()
        self.capturing_moves_withdrawal.clear()

    def clear_highlighted(self):
        self.pawns.clear_highlights()
        self.selected_pawn = None

    def _clear_after_round(self):
        self.clear_highlighted()
        self.clear_possibilities()
        self.clear_capturing_moves()
        self.clear_where_was_pawn()

    def clear_where_was_pawn(self):
        self.where_was_pawn.clear()

    def clear_able_to_capture(self):
        self.pawns.clear_if_capture()
        self.able_to_capture.clear()


class FanoronaPrinter:
    """
    Class used for taking care of all the drawings of Fanorona game

    ....
    Attributes
    ----------
    fanorona:
        an instance of class Fanorona

    Methods:
    --------
    draw(window)
        takes as argument window (pygame.display)
        draws everything that should be on the screen
        draws board, draws, pawns, indicators, texts

        this method should be called in while game loop
    draw_round_indicator(window)
        draws small circle that informs whose turn is it
        and also shows a number of the round in the upper
        left corner
    draw_hints(window)
        draws hints about where selected_pawn can be moved
        into
        it shows the player possible captures/paika_moves
    draw_winner(window)
        draws information about who won on the screen
        should be called in case of winning
    draw_clue_about_changing_round(window)
        draws the text on the screen that informs the player
        that he can let his opponents start if he wants to
    """
    def __init__(self, fanorona: "Fanorona"):
        self.fanorona = fanorona

    def draw(self, window):
        """
        Draws board, turn indicator, possibilities on selected Pawn
        and a number of round depending on the constant
        """
        self.fanorona.board.draw_board(window)

        if self.fanorona.selected_pawn is None:
            if ROWS != 3 or COLS != 3:
                self.fanorona.clear_able_to_capture()
                self.fanorona.update_able_to_capture()
        else:
            self.fanorona.clear_able_to_capture()

        self.fanorona.pawns.draw(window, self.fanorona.board)

        self.draw_round_indicator(window)

        if self.fanorona.round == 1 and self.fanorona.selected_pawn is None:
            if ROWS != 3 or COLS != 3:
                self.draw_clue_about_changing_round(window)

        if self.fanorona.problematic_cap is False:
            self.draw_hints(window)

    def draw_round_indicator(self, window):
        colour = self.fanorona.turn
        pygame.draw.circle(window, colour, (15, 15), 10)

        if IF_DRAW_NUM_OF_ROUND == 1:
            text = "Round: " + str(self.fanorona.round)
            img_font = FONT_SMALL.render(text, True, WHITE)
            window.blit(img_font, (35, 8))

    def draw_hints(self, window):
        cond1 = not self.fanorona.capturing_moves_approach
        cond2 = not self.fanorona.capturing_moves_withdrawal

        help_circle_radius = int(self.fanorona.board._square_size * (0.2))
        if cond1 and cond2:
            if self.fanorona.possibilities:
                for row, col in self.fanorona.possibilities:
                    center = self.fanorona.board.centers_of_squares[
                        row-1][col-1]
                    pygame.draw.circle(
                        window, GREEN, center, help_circle_radius)

        if self.fanorona.capturing_moves_approach:
            for row, col in self.fanorona.capturing_moves_approach:
                center = self.fanorona.board.centers_of_squares[row-1][col-1]
                pygame.draw.circle(
                    window, RED2, center, help_circle_radius)

        if self.fanorona.capturing_moves_withdrawal:
            for row, col in self.fanorona.capturing_moves_withdrawal:
                center = self.fanorona.board.centers_of_squares[row-1][col-1]
                pygame.draw.circle(
                    window, ORANGE, center, help_circle_radius)
        capt_mv_app = self.fanorona.capturing_moves_approach
        capt_mv_with = self.fanorona.capturing_moves_withdrawal
        if capt_mv_app and capt_mv_with:
            for row, col in self.fanorona.capturing_moves_withdrawal:
                if (row, col) in self.fanorona.capturing_moves_approach:
                    center = self.fanorona.board.centers_of_squares[
                        row-1][col-1]
                    pygame.draw.circle(
                        window, PINK, center, help_circle_radius)

    def draw_winner(self, window):
        """
        Draws who the winner is, waits 4s, resets the game

        If there is no winner, raises NoWinnerError
        """
        colour_won = self.fanorona.logic.check_for_winner()
        if colour_won == WHITE:
            who_won_text = "White won!"
        else:
            who_won_text = "Black won!"
        img_font = FONT.render(who_won_text, True, colour_won)
        font_width, _ = FONT.size(who_won_text)
        width = window.get_width()
        x = (width // 2)-(font_width//2)
        window.blit(img_font, (x, 10))
        pygame.display.update()
        pygame.time.delay(4000)
        self.fanorona.reset()

    def draw_clue_about_changing_round(self, window):
        """
        Draws the text that informat about possibility of
        giving away your round
        """
        text = "You can give away your round by pressing 'F'..."
        img_font = FONT_SMALL.render(text, True, YELLOW)
        font_width, _ = FONT_SMALL.size(text)
        width = window.get_width()
        x = (width // 2)-(font_width//2)
        window.blit(img_font, (x, 25))


class FanoronaLogic:
    """
    Class used for taking care of majority of logic of Fanorona game

    ....
    Attributes
    ----------
    fanorona:
        an instance of class Fanorona

    Methods:
    --------
    capture_by_approach(new_row, new_col)
    capture_by_withdrawal(new_row, new_col)
        takes as arguemnt new_row and new_column and according to that and
        fanorona.selected_pawn returns list of pawns that selected pawn would
        capture by APPROACH/WITHDRAWAL by moving there;
        return e.g. [(1, 2), (2, 2), (3, 2)] and it means that if selected pawn
        moves on the place (new_row, new_col) is would capture pawns that are
        on (1, 2), (2, 2) and (3, 2)

        raises WrongUseOfCaptureByAppOrWithFunc exception if (new_row, new_col)
        isn't around selected_pawn (one place away)
    empty_space_validator_list(list_of_poss)
        takes as arguemnt list of possible movements and removes from it places
        that are already taken by some other pawn
    last_move_validator_poss()
        return copy of list fanorona.possibilities attribute without not
        allowed moved because of direction of last movement
    possibilities_of_pawn(pawn: "Pawn")
        takes as argument an instance of class Pawn and returns list of
        possible movement that it can be moved into; note that it returns
        possiblies as if it was on PLAIN BOARD, so all possible movement
        are just movements along the lines
    possible_captures_withdrowal(pawn: "Pawns", poss)
    possible_captures_approach(pawn: "Pawns", poss)
        takes as argument an instance of class Pawn and list of its possible
        movement and according to that returns list of possible moves that
        would capture by APPROCH/WITHDROWAL
        e.g. [(1, 2), (2, 1)]
    get_last_move(pawn: "Pawn", new_row, new_col)
        takes an instance of class Pawn and new_row and new_col that means the
        place that it will be moved into and according to that returns
        direction of movement e.g. 'N', 'SW'....

        returns string
    check_for_winner()
        returns colour of pawns (RGB) that won or None if nobody has won yet
    """
    def __init__(self, fanorona: "Fanorona"):
        self.fanorona = fanorona

    def capture_by_approach(self, new_row, new_col):
        """
        This method works knowing that pawn can be moved on places that are
        'around' it, just as in fanorona game; in other cases will be raised
        WrongUseOfCaptureByAppOrWithFunc Excepetion
        """
        captured = []
        if self.fanorona.selected_pawn is not None:

            row = self.fanorona.selected_pawn.row
            col = self.fanorona.selected_pawn.column

            colour = self.fanorona.selected_pawn.colour
            colour_to_remove = BLACK if colour == WHITE else WHITE

            if abs(row-new_row) > 1 or abs(col-new_col) > 1:
                raise WrongUseOfCaptureByAppOrWithFunc()

            def check_for_capture(condition, n_row, n_col):
                if condition:
                    if self.fanorona.pawns.is_place_empty(
                            n_row, n_col) == (False, colour_to_remove):
                        captured.append((n_row, n_col))

            if new_row == row and new_col > col:
                # capture on the right
                check_for_capture(new_col+1 <= COLS, new_row, new_col+1)

                copy_new_col = new_col + 2
                while self.fanorona.pawns.is_place_empty(
                        new_row, copy_new_col) == (False, colour_to_remove):
                    captured.append((new_row, copy_new_col))
                    copy_new_col += 1

            elif new_row == row and new_col < col:
                # capture on the left
                check_for_capture(new_col - 1 > 0, new_row, new_col-1)

                copy_new_col = new_col - 2
                while self.fanorona.pawns.is_place_empty(
                      new_row, copy_new_col) == (False, colour_to_remove):
                    captured.append((new_row, copy_new_col))
                    copy_new_col -= 1

            elif new_row < row and new_col == col:
                # capture on top
                check_for_capture(new_row - 1 > 0, new_row-1, new_col)

                copy_new_row = new_row - 2
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, new_col) == (False, colour_to_remove):
                    captured.append((copy_new_row, new_col))
                    copy_new_row -= 1

            elif new_row > row and new_col == col:
                # capture at the bottom
                check_for_capture(new_row+1 <= ROWS, new_row+1, new_col)

                copy_new_row = new_row + 2
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, new_col) == (False, colour_to_remove):
                    captured.append((copy_new_row, new_col))
                    copy_new_row += 1

            elif new_row < row and new_col > col:
                # capture '/' on the right
                check_for_capture(
                    new_row-1 > 0 and new_col+1 <= COLS, new_row-1, new_col+1)

                copy_new_row = new_row - 2
                copy_new_col = new_col + 2
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, copy_new_col) == (
                            False, colour_to_remove):
                    captured.append((copy_new_row, copy_new_col))
                    copy_new_row -= 1
                    copy_new_col += 1

            elif new_row > row and new_col < col:
                # capture '/' on the left
                check_for_capture(
                    new_row+1 <= ROWS and new_col-1 > 0, new_row+1, new_col-1)

                copy_new_row = new_row + 2
                copy_new_col = new_col - 2
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, copy_new_col) == (
                            False, colour_to_remove):
                    captured.append((copy_new_row, copy_new_col))
                    copy_new_row += 1
                    copy_new_col -= 1

            elif new_row < row and new_col < col:
                # capture '\' on the left
                check_for_capture(
                    new_row-1 > 0 and new_col-1 > 0, new_row-1, new_col-1)

                copy_new_row = new_row - 2
                copy_new_col = new_col - 2
                while self.fanorona.pawns.is_place_empty(
                      copy_new_row, copy_new_col) == (False, colour_to_remove):
                    captured.append((copy_new_row, copy_new_col))
                    copy_new_row -= 1
                    copy_new_col -= 1

            elif new_row > row and new_col > col:
                # capture '\' on the right
                check_for_capture(
                    new_row+1 <= ROWS and new_col+1 <= COLS,
                    new_row+1, new_col+1)

                copy_new_row = new_row + 2
                copy_new_col = new_col + 2
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, copy_new_col) == (
                            False, colour_to_remove):
                    captured.append((copy_new_row, copy_new_col))
                    copy_new_row += 1
                    copy_new_col += 1
        return captured

    def capture_by_withdrawal(self, new_row, new_col):
        """
        This method works knowing that pawn can be moved on places that are
        'around' it, just as in fanorona game; in other cases will be raised
        WrongUseOfCaptureByAppOrWithFunc Excepetion
        """
        captured = []
        if self.fanorona.selected_pawn is not None:
            row = self.fanorona.selected_pawn.row
            col = self.fanorona.selected_pawn.column

            colour = self.fanorona.selected_pawn.colour
            colour_to_remove = BLACK if colour == WHITE else WHITE

            def check_for_capture(condition, n_row, n_col):
                if condition:
                    if self.fanorona.pawns.is_place_empty(
                            n_row, n_col) == (False, colour_to_remove):
                        captured.append((n_row, n_col))

            if abs(row-new_row) > 1 or abs(col-new_col) > 1:
                raise WrongUseOfCaptureByAppOrWithFunc()

            if new_row < row and new_col == col:
                # capture at the bottom (withdrawal), pawn goes up
                check_for_capture(new_row+2 <= ROWS, new_row+2, new_col)

                copy_new_row = new_row + 3
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, new_col) == (False, colour_to_remove):
                    captured.append((copy_new_row, new_col))
                    copy_new_row += 1

            elif new_row > row and new_col == col:
                # capture at the top (withdrowal), pawn goes down
                check_for_capture(new_row-2 > 0, new_row-2, new_col)

                copy_new_row = new_row - 3
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, new_col) == (False, colour_to_remove):
                    captured.append((copy_new_row, new_col))
                    copy_new_row -= 1

            elif new_row == row and new_col > col:
                # capture on the left (withdrawal), pawn goes right
                check_for_capture(new_col - 2 > 0, new_row, new_col-2)

                copy_new_col = new_col - 3
                while self.fanorona.pawns.is_place_empty(
                        new_row, copy_new_col) == (False, colour_to_remove):
                    captured.append((new_row, copy_new_col))
                    copy_new_col -= 1

            elif new_row == row and new_col < col:
                # capture on the right (withdrawal), pawn goes left
                check_for_capture(new_col + 2 <= COLS, new_row, new_col+2)

                copy_new_col = new_col + 3
                while self.fanorona.pawns.is_place_empty(
                        new_row, copy_new_col) == (False, colour_to_remove):
                    captured.append((new_row, copy_new_col))
                    copy_new_col += 1

            elif new_row < row and new_col > col:
                # capture by going upper right (withdrawal)
                check_for_capture(
                    new_row + 2 <= ROWS and new_col - 2 > 0,
                    new_row+2, new_col-2)

                copy_new_row = new_row + 3
                copy_new_col = new_col - 3
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, copy_new_col) == (
                            False, colour_to_remove):
                    captured.append((copy_new_row, copy_new_col))
                    copy_new_row += 1
                    copy_new_col -= 1

            elif new_row > row and new_col < col:
                # capture by going lower left (withdrawal)
                check_for_capture(
                    new_row - 2 > 0 and new_col + 2 <= COLS,
                    new_row-2, new_col+2)

                copy_new_row = new_row - 3
                copy_new_col = new_col + 3
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, copy_new_col) == (
                            False, colour_to_remove):
                    captured.append((copy_new_row, copy_new_col))
                    copy_new_row -= 1
                    copy_new_col += 1

            elif new_row > row and new_col > col:
                # capture by going lower right (withdrawal)
                check_for_capture(
                    new_row - 2 > 0 and new_col - 2 > 0, new_row-2, new_col-2)

                copy_new_row = new_row - 3
                copy_new_col = new_col - 3
                while self.fanorona.pawns.is_place_empty(
                      copy_new_row, copy_new_col) == (False, colour_to_remove):
                    captured.append((copy_new_row, copy_new_col))
                    copy_new_row -= 1
                    copy_new_col -= 1

            elif new_row < row and new_col < col:
                # capture by going upper left (withdrawal)
                check_for_capture(
                    new_row + 2 <= ROWS and new_col + 2 <= COLS,
                    new_row+2, new_col+2)

                copy_new_row = new_row + 3
                copy_new_col = new_col + 3
                while self.fanorona.pawns.is_place_empty(
                        copy_new_row, copy_new_col) == (
                            False, colour_to_remove):
                    captured.append((copy_new_row, copy_new_col))
                    copy_new_row += 1
                    copy_new_col += 1
        return captured

    def empty_space_validator_list(self, list_of_poss):
        possibilities_without_taken = deepcopy(list_of_poss)
        for row, col in list_of_poss:
            if not self.fanorona.pawns.is_place_empty(row, col)[0]:
                possibilities_without_taken.remove((row, col))
        return possibilities_without_taken

    def last_move_validator_poss(self):
        new_poss = deepcopy(self.fanorona.possibilities)
        for row, col in self.fanorona.possibilities:
            direction = self.get_last_move(
                self.fanorona.selected_pawn, row, col)
            if direction == self.fanorona.last_move:
                new_poss.remove((row, col))
        return new_poss

    def possibilities_of_pawn(self, pawn: "Pawn"):
        possibilities_to_ret = []

        row_hi = pawn.row
        col_hi = pawn.column
        cond1 = pawn.row != 1 and pawn.row != ROWS
        cond2 = pawn.column != 1 and pawn.column != COLS

        def append_top_and_down_to_possibilites():
            # top
            possibilities_to_ret.append((row_hi-1, col_hi))
            # down
            possibilities_to_ret.append((row_hi+1, col_hi))

        def append_left_and_right_to_possibilites():
            # left
            possibilities_to_ret.append((row_hi, col_hi-1))
            # right
            possibilities_to_ret.append((row_hi, col_hi+1))

        if cond1 and cond2:
            append_top_and_down_to_possibilites()
            append_left_and_right_to_possibilites()

            # diagonally
            def append_diagonal_to_possibilites():
                # top left
                possibilities_to_ret.append((row_hi-1, col_hi-1))
                # down right
                possibilities_to_ret.append((row_hi+1, col_hi+1))
                # top right
                possibilities_to_ret.append((row_hi-1, col_hi+1))
                # down left
                possibilities_to_ret.append((row_hi+1, col_hi-1))

            if is_even(pawn.column):
                if is_even(pawn.row):
                    append_diagonal_to_possibilites()
            else:
                if not is_even(pawn.row):
                    append_diagonal_to_possibilites()

        elif pawn.row == ROWS:
            # top
            possibilities_to_ret.append((row_hi-1, col_hi))
            if not is_even(pawn.column):
                if pawn.column != COLS:
                    # top right
                    possibilities_to_ret.append((row_hi-1, col_hi+1))
                if pawn.column != 1:
                    # top left
                    possibilities_to_ret.append((row_hi-1, col_hi-1))
            if pawn.column != COLS:
                # right
                possibilities_to_ret.append((row_hi, col_hi+1))
            if pawn.column != 1:
                # left
                possibilities_to_ret.append((row_hi, col_hi-1))
        elif pawn.row == 1:
            # down
            possibilities_to_ret.append((row_hi+1, col_hi))
            if not is_even(pawn.column):
                if pawn.column != COLS:
                    # right down
                    possibilities_to_ret.append((row_hi+1, col_hi+1))
                if pawn.column != 1:
                    # left down
                    possibilities_to_ret.append((row_hi+1, col_hi-1))
            if pawn.column != COLS:
                # right
                possibilities_to_ret.append((row_hi, col_hi+1))
            if pawn.column != 1:
                # left
                possibilities_to_ret.append((row_hi, col_hi-1))
        elif pawn.column == 1:
            # right
            possibilities_to_ret.append((row_hi, col_hi+1))
            if not is_even(pawn.row):
                # top right
                possibilities_to_ret.append((row_hi-1, col_hi+1))
                # down right
                possibilities_to_ret.append((row_hi+1, col_hi+1))
            # add top and down (don't have to check if last and first column)
            append_top_and_down_to_possibilites()
        elif pawn.column == COLS:
            # left
            possibilities_to_ret.append((row_hi, col_hi-1))
            if not is_even(pawn.row):
                # top left
                possibilities_to_ret.append((row_hi-1, col_hi-1))
                # down left
                possibilities_to_ret.append((row_hi+1, col_hi-1))
            append_top_and_down_to_possibilites()
        return possibilities_to_ret

    def possible_captures_approach(self, pawn: "Pawn", poss):
        pawn_row = pawn.row
        pawn_col = pawn.column
        poss_captures = []

        def check_and_append_to_captures(
                if_empty, colour, p_row, p_col):
            if not if_empty and colour != pawn.colour:
                poss_captures.append((p_row, p_col))

        for row, col in poss:
            # CHECKING POSSIBLE CAPTURES BY APPROACH
            if col == pawn_col and row < pawn_row:
                # top
                if row-1 > 0:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row-1, col)
                    # APPROACH
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if col == pawn_col and row > pawn_row:
                # down
                if row+1 <= ROWS:
                    # APPROACH
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row+1, col)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row == pawn_row and col > pawn_col:
                # right
                if col+1 <= COLS:
                    # APPROACH
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row, col+1)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row == pawn_row and col < pawn_col:
                # left
                if col-1 > 0:
                    # APPROACH
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row, col-1)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row < pawn_row and col > pawn_col:
                # top right
                # APPROACH
                if row-1 > 0 and col+1 <= COLS:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row-1, col+1)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row > pawn_row and col < pawn_col:
                # down left
                # APPROACH
                if row+1 <= ROWS and col-1 > 0:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row+1, col-1)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row > pawn_row and col > pawn_col:
                # down right
                # APPROACH
                if row+1 <= ROWS and col+1 <= COLS:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row+1, col+1)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row < pawn_row and col < pawn_col:
                # top left
                # APPROACH
                if row-1 > 0 and col-1 > 0:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row-1, col-1)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
        return poss_captures

    def possible_captures_withdrowal(self, pawn: "Pawns", poss):
        pawn_row = pawn.row
        pawn_col = pawn.column
        poss_captures = []

        def check_and_append_to_captures(
                if_empty, colour, p_row, p_col):
            if not if_empty and colour != pawn.colour:
                poss_captures.append((p_row, p_col))

        for row, col in poss:
            # CHECKING POSSIBLE CAPTURES BY WITHDROWAL
            if col == pawn_col and row < pawn_row:
                # top
                # WITHDRAWAL
                if row+2 <= ROWS:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row+2, col)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if col == pawn_col and row > pawn_row:
                # down
                # WITHDRAWAL
                if row-2 > 0:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row-2, col)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row == pawn_row and col > pawn_col:
                # right
                # WITHDRAWAL
                if col-2 > 0:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row, col-2)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row == pawn_row and col < pawn_col:
                # left
                # WITHDRAWAL
                if col+2 <= COLS:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row, col+2)
                    check_and_append_to_captures(
                        if_empty, colour, row, col)
            if row < pawn_row and col > pawn_col:
                # top right
                # WITHDRAWAL
                if col-2 > 0 and row+2 <= ROWS:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row+2, col-2)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row > pawn_row and col < pawn_col:
                # down left
                # WITHDRAWAL
                if row-2 > 0 and col+2 <= COLS:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row-2, col+2)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row > pawn_row and col > pawn_col:
                # down right
                # WITHDRAWAL
                if row-2 > 0 and col-2 > 0:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row-2, col-2)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
            if row < pawn_row and col < pawn_col:
                # top left
                # WITHDRAWAL
                if row+2 <= ROWS and col+2 <= COLS:
                    if_empty, colour = self.fanorona.pawns.is_place_empty(
                        row+2, col+2)
                    check_and_append_to_captures(
                            if_empty, colour, row, col)
        return poss_captures

    def get_last_move(self, pawn: "Pawn", new_row, new_col):
        row = pawn.row
        col = pawn.column

        if row == new_row and col == new_col:
            return None
        elif row == new_row:
            if col < new_col:
                return "E"
            if col > new_col:
                return "W"
        elif col == new_col:
            if row < new_row:
                return "S"
            if row > new_row:
                return "N"
        else:
            if row > new_row and col > new_col:
                return "NW"
            if row < new_row and col < new_col:
                return "SE"
            if row < new_row and col > new_col:
                return "SW"
            if row > new_row and col < new_col:
                return "NE"

    def check_for_winner(self):
        """
        If there is a winner, return its rgb color,
        if there is not, return None
        """
        if ROWS == 3 and COLS == 3:
            # check vertical
            for i in range(1, 4):
                if self.fanorona.pawns._colour_of_pawn(1, i) is not None:
                    colour1 = self.fanorona.pawns._colour_of_pawn(1, i)
                    colour2 = self.fanorona.pawns._colour_of_pawn(2, i)
                    colour3 = self.fanorona.pawns._colour_of_pawn(3, i)
                    if colour1 == colour2 and colour2 == colour3:
                        return colour1
            # check horizontal
            for i in range(1, 4):
                if self.fanorona.pawns._colour_of_pawn(i, 1) is not None:
                    colour1 = self.fanorona.pawns._colour_of_pawn(i, 1)
                    colour2 = self.fanorona.pawns._colour_of_pawn(i, 2)
                    colour3 = self.fanorona.pawns._colour_of_pawn(i, 3)
                    if colour1 == colour2 and colour2 == colour3:
                        return colour1
            # check diagonal
            if self.fanorona.pawns._colour_of_pawn(1, 1) is not None:
                colour1 = self.fanorona.pawns._colour_of_pawn(1, 1)
                colour2 = self.fanorona.pawns._colour_of_pawn(2, 2)
                colour3 = self.fanorona.pawns._colour_of_pawn(3, 3)
                if colour1 == colour2 and colour2 == colour3:
                    return colour1
            if self.fanorona.pawns._colour_of_pawn(1, 3) is not None:
                colour1 = self.fanorona.pawns._colour_of_pawn(1, 3)
                colour2 = self.fanorona.pawns._colour_of_pawn(2, 2)
                colour3 = self.fanorona.pawns._colour_of_pawn(3, 1)
                if colour1 == colour2 and colour2 == colour3:
                    return colour1
        else:
            pawns = self.fanorona.pawns
            if pawns.blacks == 0:
                return WHITE
            elif pawns.whites == 0:
                return BLACK
            return None
