import pytest
from src.game_board import GameBoard


def test_game_board_raises_ValueError():
    """Test GameBoard constructor validates arguments."""
    with pytest.raises(ValueError):
        GameBoard(0)
    with pytest.raises(ValueError):
        GameBoard(-1)

@pytest.mark.parametrize("side", [
    (1),
    (3),
    (10),
    (100)
])

def test_side(side):
    """Test GameBoard.side()."""
    b = GameBoard(side)
    assert b.side() == side

def test_get_raises_ValueError():
    """Test GameBoard.get() validates arguments."""
    b = GameBoard(3)
    with pytest.raises(ValueError):
        b.get(-1, 0)
    with pytest.raises(ValueError):
        b.get(3, 0)
    with pytest.raises(ValueError):
        b.get(0, -1)
    with pytest.raises(ValueError):
        b.get(0, 3)

@pytest.mark.parametrize("side, ival", [
    (1, None),
    (2, 0),
    (3, 3.14),
    (4, "X"),
])

def test_get(side, ival):
    """Test GameBoard.get()."""
    b = GameBoard(side, ival)
    for row in range(b.side()):
        for col in range(b.side()):
            assert b.get(row, col) == ival

def test_board_defaults():
    """Test GameBoard constructor uses default location value."""
    b = GameBoard(3)
    for row in range(b.side()):
        for col in range(b.side()):
            assert b.get(row, col) == None    

def test_set_raises_ValueError():
    """Test GameBoard.set() validates arguments."""
    b = GameBoard(3)
    with pytest.raises(ValueError):
        b.set(-1, 0, 0)
    with pytest.raises(ValueError):
        b.set(3, 0, 0)
    with pytest.raises(ValueError):
        b.set(0, -1, 0)
    with pytest.raises(ValueError):
        b.set(0, 3, 0)

def test_set_immutable():
    """Test GameBoard.set() preserves immutable board."""
    b1 = GameBoard(3, 0)
    b2 = b1
    for row in range(b2.side()):
        for col in range(b2.side()):
            b2 = b2.set(row, col, row*b2.side() + col)

    for row in range(b1.side()):
        for col in range(b1.side()):
            assert b1.get(row, col) == 0

def test_set():
    """Test GameBoard.set()."""
    b1 = GameBoard(3, 0)
    b2 = b1
    for row in range(b2.side()):
        for col in range(b2.side()):
            b2 = b2.set(row, col, row*b2.side() + col)

    for row in range(b2.side()):
        for col in range(b2.side()):
            assert b2.get(row, col) == row*b2.side() + col

def _board_3x3_Indexes():
    """Returns 3x3 board initialized to location index values."""
    b = GameBoard(3)

    for row in range(b.side()):
        for col in range(b.side()):
            idx = row*b.side() + col
            b = b.set(row, col, idx)

    return b

def _board_3x3_OddEven():
    """Returns 3x3 board initialzed to Odd|Even strings based on index
    values."""
    b = GameBoard(3)

    for row in range(b.side()):
        for col in range(b.side()):
            idx = row*b.side() + col
            b = b.set(row, col, "Even" if (idx % 2) == 0 else "Odd")

    return b

def test_get_row_raises_ValueError():
    """Test GameBoard.get_row() validates arguments."""
    b = GameBoard(3)
    with pytest.raises(ValueError):
        b.get_row(-1)
    with pytest.raises(ValueError):
        b.get_row(3)

@pytest.mark.parametrize("board, rows", [
    (_board_3x3_Indexes(), [[0, 1, 2], 
                            [3, 4, 5], 
                            [6, 7, 8]]),
    (_board_3x3_OddEven(), [["Even", "Odd", "Even"], 
                            ["Odd", "Even", "Odd"], 
                            ["Even", "Odd", "Even"]])
])

def test_get_row(board, rows):
    """Test GameBoard.get_row()."""
    b = board
    for idx in range(len(rows)):
        assert b.get_row(idx) == rows[idx]

def test_get_col_raises_ValueError():
    """Test GameBoard.get_col() validates arguments."""
    b = GameBoard(3)
    with pytest.raises(ValueError):
        b.get_col(-1)
    with pytest.raises(ValueError):
        b.get_col(3)

@pytest.mark.parametrize("board, cols", [
    (_board_3x3_Indexes(), [[0, 3, 6], 
                            [1, 4, 7], 
                            [2, 5, 8]]),
    (_board_3x3_OddEven(), [["Even", "Odd", "Even"], 
                            ["Odd", "Even", "Odd"], 
                            ["Even", "Odd", "Even"]])
])

def test_get_col(board, cols):
    """Test GameBoard.get_col()."""
    b = board
    for idx in range(len(cols)):
        assert b.get_col(idx) == cols[idx]

@pytest.mark.parametrize("board, ldiag", [
    (_board_3x3_Indexes(), [0, 4, 8]),
    (_board_3x3_OddEven(), ["Even", "Even", "Even"])
])

def test_get_ldiag(board, ldiag):
    """Test GameBoard.get_ldiag()."""
    b = board
    assert b.get_ldiag() == ldiag

@pytest.mark.parametrize("board, rdiag", [
    (_board_3x3_Indexes(), [2, 4, 6]),
    (_board_3x3_OddEven(), ["Even", "Even", "Even"])
])

def test_get_rdiag(board, rdiag):
    """Test GameBoard.get_rdiag()."""
    b = board
    assert b.get_rdiag() == rdiag

@pytest.mark.parametrize("board, val, matches", [
    (GameBoard(1), None, [(0,0)]),
    (_board_3x3_Indexes(), 1, [(0,1)]),
    (_board_3x3_Indexes(), 5, [(1,2)]),
    (_board_3x3_Indexes(), 6, [(2,0)]),
    (_board_3x3_OddEven(), "Odd", [(0,1),(1,0),(1,2),(2,1)]),
    (_board_3x3_OddEven(), "Even", [(0,0),(0,2),(1,1),(2,0),(2,2)])
])

def test_matching_pos(board, val, matches):
    """Test GameBoard.matching_pos()."""
    assert board.matching_pos(val) == matches
