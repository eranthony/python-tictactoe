import pytest
from src.tictactoe_rules import next_player, is_winning_move
from src.game_board import GameBoard


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
    board = GameBoard(3)
    with pytest.raises(ValueError):
        is_winning_move(board, -1, 0)
    with pytest.raises(ValueError):
        is_winning_move(board, 3, 0)
    with pytest.raises(ValueError):
        is_winning_move(board, 0, -1)
    with pytest.raises(ValueError):
        is_winning_move(board, 0, 3)
        
def _create_board(side, vals):
    """Return game board from given values."""
    b = GameBoard(side)

    for row in range(side):
        for col in range(side):
            idx = row*side + col
            b = b.set(row, col, vals[idx])

    return b

@pytest.mark.parametrize("board, row, col, result", [
    (_create_board(3, [0, 0, 0, 1, 1, 1, 0, 0, 0]), 1, 0, True),
    (_create_board(3, [0, 1, 0, 1, 1, 1, 0, 1, 0]), 0, 0, False),
    (_create_board(3, [0, 1, 0, 0, 0, 0, 0, 1, 0]), 0, 0, True),
    (_create_board(3, [0, 1, 0, 0, 0, 0, 0, 1, 0]), 0, 1, False),
    (_create_board(3, [0, 0, 1, 1, 0, 1, 1, 0, 0]), 2, 2, True),
    (_create_board(3, [1, 0, 0, 1, 0, 1, 0, 0, 1]), 1, 1, True)
])

def test_is_winning_move(board, row, col, result):
    assert is_winning_move(board, row, col) == result