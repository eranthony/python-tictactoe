"""Module docstring"""
import pytest
from game.board import Board

def test_game_board_raises_ValueError():
    """Test Board constructor validates arguments."""
    with pytest.raises(ValueError):
        Board(0)
    with pytest.raises(ValueError):
        Board(-1)

@pytest.mark.parametrize("side", [
    (1),
    (3),
    (10),
    (100)
])

def test_side(side):
    """Test Board.side_len()."""
    b = Board(side)
    assert b.side_len() == side

def test_get_raises_ValueError():
    """Test Board.get() validates arguments."""
    b = Board(3)
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
    """Test Board.get()."""
    b = Board(side, ival)
    for row in range(b.side_len()):
        for col in range(b.side_len()):
            assert b.get(row, col) == ival

def test_board_defaults():
    """Test Board constructor uses default location value."""
    b = Board(3)
    for row in range(b.side_len()):
        for col in range(b.side_len()):
            assert b.get(row, col) == None    

def test_set_raises_ValueError():
    """Test Board.set() validates arguments."""
    b = Board(3)
    with pytest.raises(ValueError):
        b.set(-1, 0, 0)
    with pytest.raises(ValueError):
        b.set(3, 0, 0)
    with pytest.raises(ValueError):
        b.set(0, -1, 0)
    with pytest.raises(ValueError):
        b.set(0, 3, 0)

def test_set_immutable():
    """Test Board.set() preserves immutable board."""
    b1 = Board(3, 0)
    b2 = b1
    for row in range(b2.side_len()):
        for col in range(b2.side_len()):
            b2 = b2.set(row, col, row*b2.side_len() + col)

    for row in range(b1.side_len()):
        for col in range(b1.side_len()):
            assert b1.get(row, col) == 0

def test_set():
    """Test Board.set()."""
    b1 = Board(3, 0)
    b2 = b1
    for row in range(b2.side_len()):
        for col in range(b2.side_len()):
            b2 = b2.set(row, col, row*b2.side_len() + col)

    for row in range(b2.side_len()):
        for col in range(b2.side_len()):
            assert b2.get(row, col) == row*b2.side_len() + col

def _board_3x3_Indexes():
    """Returns 3x3 board initialized to location index values."""
    b = Board(3)

    for row in range(b.side_len()):
        for col in range(b.side_len()):
            idx = row*b.side_len() + col
            b = b.set(row, col, idx)

    return b

def _board_3x3_OddEven():
    """Returns 3x3 board initialzed to Odd|Even strings based on index
    values."""
    b = Board(3)

    for row in range(b.side_len()):
        for col in range(b.side_len()):
            idx = row*b.side_len() + col
            b = b.set(row, col, "Even" if (idx % 2) == 0 else "Odd")

    return b

def test_get_row_raises_ValueError():
    """Test Board.get_row() validates arguments."""
    b = Board(3)
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
    """Test Board.get_row()."""
    b = board
    for idx in range(len(rows)):
        assert b.get_row(idx) == rows[idx]

def test_get_col_raises_ValueError():
    """Test Board.get_col() validates arguments."""
    b = Board(3)
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
    """Test Board.get_col()."""
    b = board
    for idx in range(len(cols)):
        assert b.get_col(idx) == cols[idx]

@pytest.mark.parametrize("board, ldiag", [
    (_board_3x3_Indexes(), [0, 4, 8]),
    (_board_3x3_OddEven(), ["Even", "Even", "Even"])
])

def test_get_ldiag(board, ldiag):
    """Test Board.get_ldiag()."""
    b = board
    assert b.get_ldiag() == ldiag

@pytest.mark.parametrize("board, rdiag", [
    (_board_3x3_Indexes(), [2, 4, 6]),
    (_board_3x3_OddEven(), ["Even", "Even", "Even"])
])

def test_get_rdiag(board, rdiag):
    """Test Board.get_rdiag()."""
    b = board
    assert b.get_rdiag() == rdiag

@pytest.mark.parametrize("board, val, matches", [
    (Board(1), None, [(0,0)]),
    (_board_3x3_Indexes(), 1, [(0,1)]),
    (_board_3x3_Indexes(), 5, [(1,2)]),
    (_board_3x3_Indexes(), 6, [(2,0)]),
    (_board_3x3_OddEven(), "Odd", [(0,1),(1,0),(1,2),(2,1)]),
    (_board_3x3_OddEven(), "Even", [(0,0),(0,2),(1,1),(2,0),(2,2)])
])

def test_matching_pos(board, val, matches):
    """Test Board.matching_pos()."""
    assert board.matching_pos(val) == matches
