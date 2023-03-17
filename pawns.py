from pawn import Pawn
from constants import ROWS, COLS, WHITE, BLACK
from constants import WHITE2, BLACK2


class Pawns:
    """
    Class used for representing the pawns

    ...
    Attributes
    ----------
    pawns: list
        a list of instances of class Pawn

        the default value is empty list []
    whites: int
        a number of white pawns
    blacks: int
        a number of black pawns

    Methods
    -------
    draw(window, board)
        draws each Pawn in 'pawns' attribute
    _starting_positions()
        adds to 'pawns' attribute instances of class Pawn that are
        placed on the right place according to the size of the board;
        also keeps attributes 'blacks', 'whites' up-to-date
    clear_highlights()
        sets attribute 'if_selected' of each pawn in 'pawns' to False
    clear_if_capture()
        sets attribute 'if_capture' of each pawn in 'pawns' to False
    is_place_empty(row, col)
        takes a number of rows and a number of columns of some place;
        returns (True, None) if place is empty
        return (False, colour of pawn in this place) if place is taken
    remove_pawn(row, col)
        take a number of rows and columns of some place and removes the pawn
        that is placed there; if there is no pawn at this place, nothing
        is done
    row_column_pawn(row, col)
        takes a number of rows and columns of some place and returns an
        instance of class Pawn that is placed there or returns None if
        the place is empty
    _colour_of_pawn(row, col)
        takes a number of rows and columns and returns colour of Pawn
        that is placed there or no if the place is empty
    _change_colours_to_default()
        changes colour of every Pawn in 'pawns' to default (BLACK/WHITE)
    highlight_pawn(pawn)
        calls clear_highlights() method of this class (clears highlight of each
        Pawn in 'pawns') and sets attribute 'if_selected' of passed Pawn
        to True

        this method is used for highlighting only clicked pawn
    """
    def __init__(self, pawns=None):
        # default value of self.pawns is []
        self.pawns = pawns if pawns else []
        self.whites = 0
        self.blacks = 0
        # when self.pawns is empty, new pawns are created
        # and placed at starting positions
        if not self.pawns:
            self._starting_positions()

    def draw(self, window, board):
        """
        Draws each Pawn that is in the 'pawns'

        'pawns' - attribute that store instances of Pawn in a list
        """
        for pawn in self.pawns:
            pawn.draw(window, board)

    def _starting_positions(self):
        """
        Adding pawn to list self.pawns depending on the
        width and height of the board;

        Sets added pawns at the starting points;
        """
        # board 3x3 have characteristic starting postions
        list_of_pawns = []
        if ROWS == COLS and ROWS == 3:
            # WHITES
            for i in range(1, 3):
                pawn = Pawn(3, i, WHITE)
                list_of_pawns.append(pawn)
            pawn2 = Pawn(2, 1, WHITE)
            list_of_pawns.append(pawn2)

            # BLACKS
            for i in range(2, 4):
                pawn = Pawn(1, i, BLACK)
                list_of_pawns.append(pawn)
            pawn2 = Pawn(2, 3, BLACK)
            list_of_pawns.append(pawn2)
            self.blacks = 3
            self.whites = 3
        else:
            # rows at the top with black pawns
            # (above the middle row)
            for i in range(1, (ROWS//2)+1):
                for j in range(1, COLS+1):
                    pawn = Pawn(i, j, BLACK)
                    self.blacks += 1
                    list_of_pawns.append(pawn)
            # rows at the bottom with white pawns
            # (below the middle row)
            for i in range((ROWS//2)+2, ROWS+1):
                for j in range(1, COLS+1):
                    pawn = Pawn(i, j, WHITE)
                    self.whites += 1
                    list_of_pawns.append(pawn)
            # filling the line between them
            # (middle row)
            num_of_center_row = ROWS//2+1
            for i in range(0, (COLS//2), 2):
                pawn = Pawn(num_of_center_row, i+1, BLACK)
                self.blacks += 1
                list_of_pawns.append(pawn)
                pawn2 = Pawn(num_of_center_row, i+2, WHITE)
                self.whites += 1
                list_of_pawns.append(pawn2)
            for i in range((COLS//2)+2, COLS, 2):
                pawn = Pawn(num_of_center_row, i+1, WHITE)
                self.whites += 1
                list_of_pawns.append(pawn)
                pawn2 = Pawn(num_of_center_row, i, BLACK)
                self.blacks += 1
                list_of_pawns.append(pawn2)
        self.pawns = list_of_pawns

    def clear_highlights(self):
        """
        Changes attribute 'if_selected' of each pawn
        in attribute 'pawns' to False
        """
        for pawn in self.pawns:
            pawn.if_selected = False

    def clear_if_capture(self):
        """
        Changes attribute 'if_capture' of each pawn
        in attribute 'pawns' to False
        """
        for pawn in self.pawns:
            pawn.if_capture = False

    def is_place_empty(self, row, col):
        """
        Checks whether or not place with passed number of rows
        and number of columns is empty;
        If a place is empty, returns tuple (True, None)

        If a place is taken, returns (False, colour of pawn in this place)

        If a place is certainly wrong (negativ values) returns None
        """
        for pawn in self.pawns:
            if pawn.row == row and pawn.column == col:
                return False, pawn.colour
        if row >= 1 and col >= 1:
            return True, None
        return None

    def remove_pawn(self, row, col):
        """
        Takes a number of rows and columns and removes the pawn
        that is placed there
        """
        for pawn in self.pawns:
            if pawn.row == row and pawn.column == col:
                self.pawns.remove(pawn)

    def row_column_pawn(self, row, col):
        """
        Takes a number of rows and columns and returns an instance of
        Pawn that is placed there; if this place is empty, returns None
        """
        for pawn in self.pawns:
            if pawn.row == row and pawn.column == col:
                return pawn
        return None

    def _colour_of_pawn(self, row, col):
        """
        Returns colour of the pawn at the place with row, col
        (row - a number of rows, col - a number of columns) or None
        """
        for pawn in self.pawns:
            if pawn.row == row and pawn.column == col:
                return pawn.colour
        return None

    def _change_colours_to_default(self):
        """
        Changes colour of pawns to default (BLACK/WHITE)
        """
        for pawn in self.pawns:
            if pawn.colour == WHITE2:
                pawn.colour = WHITE
            elif pawn.colour == BLACK2:
                pawn.colour = BLACK

    def highlight_pawn(self, pawn):
        """
        Changes attribute 'if_selected' of clicked Pawn
        """
        self.clear_highlights()
        pawn.if_selected = not pawn.if_selected
