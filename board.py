import pygame
from constants import WHITE, RED
from constants import ROWS, COLS, LINE_WIDTH, PADDING


class Board:
    """
    Class used for representing the board

    ...
    Attributes
    ----------
    rows: int
        a number of rows
    columns: int
        a number of columns
    center_of_squares: list
        two-dim list containing center point of each square (box for pawn)
    rectangles_boxes: list
        two-dim list containing instances of class Rect on the board
    _square_size: int
        size of the square that is calculated based on the width and the height
        of passed window (pygame.display)

    Methods
    -------
    draw_board(window)
        draws the square boxes depending on the size of passed window
        (pygame.display) and lines of the board
    row_col_from_center_of_square(passed_center)
        takes as an argument a tuple with two numbers which represents
        the center of the square box and returns its number of column and row

        if there is no such square with passed_center, returns None
    """
    def __init__(self):
        self.rows = ROWS
        self.columns = COLS
        self.centers_of_squares = None
        self.rectangles_boxes = []
        self._square_size = None

    def draw_board(self, window):
        """Draws the board on the passed window (pygame.display)"""
        # takes the size of the window
        width = window.get_width()
        height = window.get_height()

        # calculating some appropriate size of square
        square_size_depending_on_height = int(
            (height-(PADDING*2)) // (((ROWS-1)*2)+1))
        square_size_depending_on_width = int(
            (width-(PADDING*2)) // (((COLS-1)*2)+1))
        square_size = min(
            square_size_depending_on_height, square_size_depending_on_width)
        self._square_size = square_size

        middle_points_of_squares = []
        rectangles_boxes = []

        # centering the board depending on the free space
        # at the top and at the bottom
        height_of_board = ((ROWS * square_size) + ((ROWS-1)*square_size))
        y = (height - height_of_board)//2
        for _ in range(ROWS):
            # centering the board depending on the free space
            # on the left and right
            width_of_board = ((COLS * square_size) + ((COLS-1) * square_size))
            x = (width - width_of_board)//2
            middle_points_in_row = []
            rectangles_row = []
            for _ in range(COLS):
                rectangle = pygame.Rect(x, y, square_size, square_size)
                rectangles_row.append(rectangle)
                pygame.draw.rect(window, RED, rectangle)
                center = rectangle.center
                middle_points_in_row.append(center)
                x += 2 * square_size
            y += 2 * square_size
            # draw horizontal line
            # middle_point_of_left is the center of left square in a row
            # middle_point_of_right is the center of right square in a row
            middle_point_of_left = middle_points_in_row[0]
            middle_point_of_right = middle_points_in_row[-1]
            pygame.draw.line(
                window, WHITE, middle_point_of_left,
                middle_point_of_right, LINE_WIDTH)

            middle_points_of_squares.append(middle_points_in_row)
            rectangles_boxes.append(rectangles_row)

        # assigning lists to attributes of the class
        self.centers_of_squares = middle_points_of_squares
        self.rectangles_boxes = rectangles_boxes

        # draw vertical lines
        for i in range(COLS):
            middle_point_of_upper = middle_points_of_squares[0][i]
            middle_point_of_lower = middle_points_of_squares[-1][i]
            pygame.draw.line(
                window, WHITE, middle_point_of_upper,
                middle_point_of_lower, LINE_WIDTH)

        # draw '\' lines
        for i in range(0, ROWS-2, 2):  # it doesnt take the last row
            for j in range(0, COLS-2, 2):
                point_one = middle_points_of_squares[i][j]
                point_two = middle_points_of_squares[i+2][j+2]
                pygame.draw.line(
                    window, WHITE, point_one, point_two, LINE_WIDTH)

        # draw '/' lines
        for i in range(0, ROWS-2, 2):
            for j in range(2, COLS, 2):
                point_one = middle_points_of_squares[i][j]
                point_two = middle_points_of_squares[i+2][j-2]
                pygame.draw.line(
                    window, WHITE, point_one, point_two, LINE_WIDTH)

    def row_col_from_center_of_square(self, passed_center):
        """Takes center of square, returns its number of row, column or None"""
        for i, centers_row in enumerate(self.centers_of_squares):
            for j, center in enumerate(centers_row):
                if center == passed_center:
                    return i+1, j+1
        return None
