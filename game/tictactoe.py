"""Module docstring"""
from .board import Board


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
        board (Board): Game board with location values.
        row (int): Row location.
        col (int): Column location.

    Raises:
        TypeError: board must be a Board object.
        ValueError: game board row must be between 0 and side-1.
        ValueError: game board column must be between 0 and side-1.
    """
    if not isinstance(board, Board):
        raise TypeError("board must be a Board object.")

    val = board.get(row, col)

    is_ldiag = row == col
    is_rdiag = row == board.side_len() - col - 1

    if all(map(lambda v: v == val, board.get_row(row))):
        return True
    if all(map(lambda v: v == val, board.get_col(col))):
        return True
    if is_ldiag and all(map(lambda v: v == val, board.get_ldiag())):
        return True
    if is_rdiag and all(map(lambda v: v == val, board.get_rdiag())):
        return True

    return False

def move_win_stats(board, cur_player, total_player):
    """Returns the statistics of the current player winning for each
    open move on the board assuming the rules of Tic Tac Toe.

    This is a brute force algorithm that plays all possible moves
    regardless of prior results or board symmetry. 

    Args:
        board (Board): Current game board. Open positions must have
            the value of None.
        cur_player (int): Current player number.
        total_player (int): Total number of players.

    Returns:
        A dictionary of lists. The keys are (row,col) tuples for open
        positions. The values are lists of integers. The values
        represent the number of times each player won where the 
        player numbers are used to index the lists. An empty 
        dictionary is returned if there are no open moves.

        For example: { (0,1):[5, 3], (1,1):[10, 2] } shows statistics
        for the current player playing locations (0,1) and (1,1). In
        the first case the first player won 5 times and second player 
        won 3 times. The in the latter case win ratio was 10 to 2.

    Raises:
        TypeError: board must be a Board object.
    """
    win_stats = {}

    # Brute force algorithm plays all open board positions. If a move 
    # is a win, then record the win for the current player. Otherwise 
    # play the move and record the collated stats for all successive 
    # moves.

    open_pos = board.matching_pos(None)

    for pos in open_pos:
        move_row = pos[0]
        move_col = pos[1]
        new_board = board.set(move_row, move_col, cur_player)

        win_stats[pos] = [0 for i in range(total_player)]

        if is_winning_move(new_board, move_row, move_col):
            win_stats[pos][cur_player] = 1
        else:
            new_player = next_player(cur_player, total_player)
            move_stats = move_win_stats(new_board, new_player, total_player)
            for stats in iter(move_stats.values()):
                for idx, stat in enumerate(stats):
                    win_stats[pos][idx] += stat

    return win_stats


def has_left_right_symmetry(board):
    """Returns true if the board has left-right symmetry."""
    side = board.side_len()
    max_idx = side / 2

    for row in range(side):
        for idx in range(max_idx):
            if board.get(row, idx) != board.get(row, side - idx - 1):
                return False
    
    return True

def has_up_down_symmetry(board):
    """Returns true if the board has up-down symmetry."""
    side = board.side_len()
    max_idx = side / 2

    for col in range(side):
        for idx in range(max_idx):
            if board.get(idx, col) != board.get(side - idx - 1, col):
                return False
    
    return True
