from game_board import GameBoard


def next_player(cur_player, total_player):
    """Returns the number of the next player given the current
    player's number and the total number of players.

    Multiple players can play Tic Tac Toe. Players are numbered from 
    0 to total_player-1. The order of players is sequential.

    Args:
        cur_player (int): Number of the current player.
        total_player (int): Total number of players.

    Raises:
        ValueError: current_player must be between 0 and total_player-1.
        ValueError: total_player must be greater than 0.
    """
    if total_player <= 0:
        raise ValueError("total_player must be greater than 0.")
    if cur_player < 0 or cur_player >= total_player:
        raise ValueError("cur_player must be between 0 and total_player-1.")

    if cur_player == total_player - 1:
        return 0
    else:
        return cur_player + 1


def is_winning_move(board, row, col):
    """Returns True if the value in the given location is a winning
    move based on Tic Tac Toe rules. Returns false otherwise.

    Args:
        board (GameBoard): Game board with location values.
        row (int): Row location.
        col (int): Column location.

    Raises:
        TypeError: board must be a GameBoard object.
        ValueError: game board row must be between 0 and side-1.
        ValueError: game board column must be between 0 and side-1.
    """
    if not isinstance(board, GameBoard):
        raise TypeError("board must be a GameBoard object.")

    val = board.get(row, col)

    is_ldiag = row == col
    is_rdiag = row == board.side() - col - 1

    if all(map(lambda v: v == val, board.get_row(row))):
        return True
    if all(map(lambda v: v == val, board.get_col(col))):
        return True
    if is_ldiag and all(map(lambda v: v == val, board.get_ldiag())):
        return True
    if is_rdiag and all(map(lambda v: v == val, board.get_rdiag())):
        return True

    return False
