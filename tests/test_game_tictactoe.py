"""Module docstring"""
import pytest
from game.tictactoe import next_player, is_winning_move, matching_positions, is_symmetric
from game.board import Board


def test_next_player_raises_ValueError():
    """Tests next_player() validates arguments."""
    with pytest.raises(ValueError):
        next_player(-1, 2)
    with pytest.raises(ValueError):
        next_player(2, 2)
    with pytest.raises(ValueError):
        next_player(3, 2)
    with pytest.raises(ValueError):
        next_player(0, -1)
    with pytest.raises(ValueError):
        next_player(0, 0)

@pytest.mark.parametrize("cur_player, total_player, result", [
    (0, 3, 1),
    (1, 3, 2),
    (2, 3, 0)
])

def test_next_player(cur_player, total_player, result):
    """Tests next_player()."""
    assert next_player(cur_player, total_player) == result


def test_is_winning_move_raises_TypeError():
    """Tests is_winning_move() validates arguments."""
    with pytest.raises(TypeError):
        is_winning_move(None, 0, 0)
    with pytest.raises(TypeError):
        is_winning_move(int, 0, 0)
    with pytest.raises(TypeError):
        is_winning_move(str, 0, 0)

def test_is_winning_move_raises_ValueError():
    """Tests is_winning_move() validates arguments."""
    board = Board(3)
    with pytest.raises(ValueError):
        is_winning_move(board, -1, 0)
    with pytest.raises(ValueError):
        is_winning_move(board, 3, 0)
    with pytest.raises(ValueError):
        is_winning_move(board, 0, -1)
    with pytest.raises(ValueError):
        is_winning_move(board, 0, 3)
        
@pytest.mark.parametrize("board, row, col, result", [
    (Board(3, [0, 0, 0, 1, 1, 1, 0, 0, 0]), 1, 0, True),
    (Board(3, [0, 1, 0, 1, 1, 1, 0, 1, 0]), 0, 0, False),
    (Board(3, [0, 1, 0, 0, 0, 0, 0, 1, 0]), 0, 0, True),
    (Board(3, [0, 1, 0, 0, 0, 0, 0, 1, 0]), 0, 1, False),
    (Board(3, [0, 0, 1, 1, 0, 1, 1, 0, 0]), 2, 2, True),
    (Board(3, [1, 0, 0, 1, 0, 1, 0, 0, 1]), 1, 1, True)
])

def test_is_winning_move(board, row, col, result):
    """Tests is_winning_board()."""
    assert is_winning_move(board, row, col) == result


def test_matching_positions_raises_TypeError():
    """Tests matching_positions() validates arguments."""
    with pytest.raises(TypeError):
        matching_positions(None, 0)

def _board_3x3_Indexes():
    """Returns 3x3 board initialized to location index values."""
    return Board(3, [0, 1, 2, 3, 4, 5, 6, 7, 8])

def _board_3x3_OddEven():
    """Returns 3x3 board initialzed to Odd|Even strings based on index
    values."""
    return Board(3, ["Even", "Odd", "Even", "Odd", "Even", "Odd", "Even", "Odd", "Even"])

@pytest.mark.parametrize("board, val, matches", [
    (Board(1), None, [(0,0)]),
    (_board_3x3_Indexes(), 1, [(0,1)]),
    (_board_3x3_Indexes(), 5, [(1,2)]),
    (_board_3x3_Indexes(), 6, [(2,0)]),
    (_board_3x3_OddEven(), "Odd", [(0,1), (1,0), (1,2), (2,1)]),
    (_board_3x3_OddEven(), "Even", [(0,0), (0,2), (1,1), (2,0), (2,2)])
])

def test_matching_positions(board, val, matches):
    """Test matching_positions()."""
    assert matching_positions(board, val) == matches


def _is_match(board1, board2):
    """Returns True if the boards have the same size and values. 
    Otherwise, returns False."""
    if board1.side_len() != board2.side_len():
        return False

    for row in range(board1.side_len()):
        for col in range(board2.side_len()):
            if board1.get(row, col) != board2.get(row, col):
                return False
    
    return True

def test_is_symmetric_raises_TypeError():
    """Tests is_symmetric raises TypeError."""
    with pytest.raises(TypeError):
        is_symmetric(None, lambda pos: pos)
    with pytest.raises(TypeError):
        is_symmetric(Board(3), None)


@pytest.mark.parametrize("board, symmetry_fn, result", [
    (Board(3, [0, 0, 0, 1, 1, 1, 2, 2, 2]), lambda pos: (pos[0], 3 - pos[1] - 1), True),
    (Board(3, [0, 1, 2, 0, 1, 2, 0, 1, 2]), lambda pos: (pos[0], 3 - pos[1] - 1), False),
    (Board(3, [0, 1, 2, 1, 0, 1, 2, 1, 0]), lambda pos: (pos[0], 3 - pos[1] - 1), False),
    (Board(3, [2, 1, 0, 3, 0, 1, 0, 3, 2]), lambda pos: (pos[0], 3 - pos[1] - 1), False),
    (Board(3, [0, 0, 0, 1, 1, 1, 2, 2, 2]), lambda pos: (3 - pos[0] - 1, pos[1]), False),
    (Board(3, [0, 1, 2, 0, 1, 2, 0, 1, 2]), lambda pos: (3 - pos[0] - 1, pos[1]), True),
    (Board(3, [0, 1, 2, 1, 0, 1, 2, 1, 0]), lambda pos: (3 - pos[0] - 1, pos[1]), False),
    (Board(3, [2, 1, 0, 3, 0, 1, 0, 3, 2]), lambda pos: (3 - pos[0] - 1, pos[1]), False),
    (Board(3, [0, 0, 0, 1, 1, 1, 2, 2, 2]), lambda pos: (pos[1], pos[0]), False),
    (Board(3, [0, 1, 2, 0, 1, 2, 0, 1, 2]), lambda pos: (pos[1], pos[0]), False),
    (Board(3, [0, 1, 2, 1, 0, 3, 2, 3, 0]), lambda pos: (pos[1], pos[0]), True),
    (Board(3, [2, 1, 0, 3, 0, 1, 0, 3, 2]), lambda pos: (pos[1], pos[0]), False),
    (Board(3, [0, 0, 0, 1, 1, 1, 2, 2, 2]), lambda pos: (3 - pos[1] - 1, 3 - pos[0] - 1), False),
    (Board(3, [0, 1, 2, 0, 1, 2, 0, 1, 2]), lambda pos: (3 - pos[1] - 1, 3 - pos[0] - 1), False),
    (Board(3, [0, 1, 2, 1, 0, 3, 2, 3, 0]), lambda pos: (3 - pos[1] - 1, 3 - pos[0] - 1), False),
    (Board(3, [2, 1, 0, 3, 0, 1, 0, 3, 2]), lambda pos: (3 - pos[1] - 1, 3 - pos[0] - 1), True),
])

def test_is_symmetric(board, symmetry_fn, result):
    """Tests is_symmetric."""
    assert is_symmetric(board, symmetry_fn) == result
