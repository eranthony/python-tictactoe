"""Module docstring"""

class Board(object):
    """Class used to represent a square game board with a value at each 
    location.
    
    The board is immutable and may contain heterogeneous values. Board
    locations are referenced by row and column values, which range from 
    0 to the length of the side minus 1.

    Attributes:
        None
    """

    def __init__(self, side, ival=None):
        """Initializes a game board of the given side length and 
        initial location values.

        Args:
            side (int): Length of board on one side. Must be greater 
                than 0.
            ival: Initial value for all board locations. Defaults to
                None.

        Raises:
            ValueError: game board side must be greater than 0.
        """
        if side <= 0:
            raise ValueError("game board side must be greater than 0.")
        
        self._side = side
        self._vals = [ival for i in range(side*side)]


    def _validate_row(self, row):
        """Raises ValueError if row location value is invalid.
        
        Args:
            row (int): Row location.
        """
        if row < 0 or row >= self._side:
            raise ValueError("game board row must be between 0 and side-1.")


    def _validate_col(self, col):
        """Raises ValueError if column location value is invalid.
                
        Args:
            col (int): Column location.
        """
        if col < 0 or col >= self._side:
            raise ValueError("game board column must be between 0 and side-1.")


    def _idx(self, row, col):
        """Returns list index for given row and column location.
        
        Args:
            row (int): Row location.
            col (int): Column location.
        """
        return row*self._side + col


    def side_len(self):
        """Returns length of board's side."""
        return self._side


    def get(self, row, col):
        """Returns board value at given row and column location.

        Args:
            row (int): Row location.
            col (int): Column location.

        Raises:
            ValueError: game board row must be between 0 and side-1.
            ValueError: game board column must be between 0 and side-1.
        """
        self._validate_row(row)
        self._validate_col(col)
        return self._vals[self._idx(row, col)]


    def get_row(self, row):
        """Returns list of board values for the given row location.

        Args:
            row (int): Row location.

        Raises:
            ValueError: game board row must be between 0 and side-1.
        """
        self._validate_row(row)
        return [self.get(row, col) for col in range(self._side)]


    def get_col(self, col):
        """Returns list of board values for the given column location.

        Args:
            col (int): Column location.

        Raises:
            ValueError: game board column must be between 0 and side-1.
        """
        self._validate_col(col)
        return [self.get(row, col) for row in range(self._side)]


    def get_ldiag(self):
        """Returns list of board values along the diagonal from location
        (0,0) to (side-1,side-1)."""
        return [self.get(idx, idx) for idx in range(self._side)]


    def get_rdiag(self):
        """Returns list of board values along the diagonal from location
        (0,side-1) to (side-1,0)."""
        side = self._side
        return [self.get(idx, side-idx-1) for idx in range(side)]


    def matching_pos(self, val):
        """Returns list of board locations that match the given value.

        Args:
            val: Board value to match.

        Returns:
            A list of (row,column) tuples for all board locations with
            the given value. Returns an empty list of the value is not
            present in the board.
        """
        return [(row, col) 
                for row in range(self._side)
                for col in range(self._side) 
                if self.get(row, col) == val]


    def set(self, row, col, val):
        """Returns a new board that is a copy of the existing board
        with the given location set to a new value.

        Args:
            row (int): Row location for new value.
            col (int): Column location for new value.
            val: Value to set at the given location.

        Raises:
            ValueError: game board row must be between 0 and side-1.
            ValueError: game board column must be between 0 and side-1.
        """
        self._validate_row(row)
        self._validate_col(col)

        new_board = Board(self._side)

        for r in range(self._side):
            for c in range(self._side): 
                idx = self._idx(r, c)

                if r == row and c == col:
                    new_board._vals[idx] = val
                else:
                    new_board._vals[idx] = self._vals[idx]
        
        return new_board
