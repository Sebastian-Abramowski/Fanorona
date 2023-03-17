from pygame import draw
from board import Board
from constants import ORANGE, PINK
from constants import ROWS, COLS


class Pawn:
    """
    Class used for representing the pawn

    ...
    Attributes
    ----------
    row: int
        a number of row
    column: int
        a number of column
    colour: tuple e.g. (0, 0, 0)
        a colour of the pawn (rgb)
    if_selected: bool
        True is Pawn is selected, False when it's not
    if_capture: bool
        True if capturing by the pawn is possible, False
        when it's not

    Methods
    -------
    draw(window, board, row=None, col=None)
        draws the Pawn and its highlighting when if_selected is
        True, you can pass row, col if you don't want to draw where
        current position of the Pawn is
    move(row, col)
        moves the Pawn, changes its 'row' and 'column' attributes
    _take_the_center_of_pawn(board, row=None, col=None)
        returns the tuple which represent where Pawn should be drawn
        (the center of the circle) depending on its row and column
    __str__()
        returns string information about the Pawn
    """
    def __init__(self, n_row, n_column, colour, selected=False):
        """
        Creates an instance of Pawn, arguments required:
        n_row - a number of row
        n_column - a number of colum
        colour - rgb colour of Pawn
        selected - bool if Pawn is selected, default value is False
        """
        self.row = n_row
        self.column = n_column
        self.colour = colour
        self.if_selected = selected
        self.if_capture = False

    def draw(self, window, board: "Board",
             row=None, col=None):
        """
        Draws the Pawn on the board and draws highlighting
        if the Pawn 'if_selected' attribute is True

        Can also take row, col where it should be drawn, by
        default it's current row, col of the Pawn
        """
        square_size = board._square_size
        circle_radius = int(0.8*square_size/2)
        circle_radius_HIGHLIGHT = int(0.9*square_size/2)
        if row is None and col is None:
            row = self.row
            col = self.column
        center = self._take_the_center_of_pawn(board, row, col)
        if self.if_capture:
            if ROWS != 3 or COLS != 3:
                draw.circle(window, PINK, center, circle_radius_HIGHLIGHT)
        if self.if_selected:
            draw.circle(window, ORANGE, center, circle_radius_HIGHLIGHT)
        draw.circle(window, self.colour, center, circle_radius)

    def move(self, row, col):
        """Moves pawn to the the place depending on passed row, col"""
        self.row = row
        self.column = col

    def _take_the_center_of_pawn(self, board: "Board", row=None, col=None):
        """
        When only board is passed, returns the center of this Pawn
        When also row, column is passed, returns the center of the
        place (square box) depending on row, column

        Returns a tuple e.g. (125, 325)
        """
        if row is None and col is None:
            row = self.row
            col = self.column
        return board.centers_of_squares[row-1][col-1]

    def __str__(self):
        """
        String representation, returns string with information
        about attributes of this class
        """

        text_to_return = f"Row: {self.row}, Column: {self.column}, "\
                         f"colour: {self.colour}, selected: {self.if_selected}"
        return text_to_return
