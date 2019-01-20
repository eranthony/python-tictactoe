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

def matching_positions(board, val):
    """Returns list of board locations that match the given value.

    Args:
        board: Board to search for matching values
        val: Board value to match.

    Returns:
        A list of (row,column) tuples for all board locations with
        the given value. Returns an empty list if the value is not
        present in the board.

    Raises:
        TypeError: board must be a Board object.
    """
    if not isinstance(board, Board):
        raise TypeError("board must be a Board object.")

    return [(row, col) 
            for row in range(board.side_len())
            for col in range(board.side_len()) 
            if board.get(row, col) == val]

def is_symmetric(board, symmetry_fn):
    """Returns true if the board is symmetric based on the symmetry function.

    Raises:
        TypeError: board must be a Board object.
        TypeError: symmetry_fn must be callable.
    """
    if not isinstance(board, Board):
        raise TypeError("board must be a Board object.")
    if not callable(symmetry_fn):
        raise TypeError("symmetry_fn must be callable.")

    side = board.side_len()

    for row in range(side):
        for col in range(side):
            (sym_row, sym_col) = symmetry_fn((row, col))
            if board.get(row, col) != board.get(sym_row, sym_col):
                return False

    return True

def _collate_positions(board, positions):
    """Returns simple collated position list.

    Ex: [1, 2, 3] -> [[1], [2], [3]]
    
    Raises:
        TypeError: board must be a Board object.
    """
    if not isinstance(board, Board):
        raise TypeError("board must be a Board object.")

    return [[pos] for pos in positions]

def _collate_symmetric_positions(board, positions):
    """Returns collated position list based on board symmetry.

    Positions are collated together if the equivalent based on board symmetry.

    Raises:
        TypeError: board must be a Board object.
    """
    if not isinstance(board, Board):
        raise TypeError("board must be a Board object.")

    collated_positions = []

    side = board.side_len()
    symmetry_fns = [
        lambda pos: (pos[0], side - pos[1] - 1),            # left/right
        lambda pos: (side - pos[0] - 1, pos[1]),            # up/down
        lambda pos: (pos[1], pos[0]),                       # left diag
        lambda pos: (side - pos[1] - 1, side - pos[0] - 1), # right diag
        lambda pos: (pos[1], side - pos[0] - 1),            # rotate 90
        lambda pos: (side - pos[0] - 1, side - pos[1] - 1), # rotate 180
        lambda pos: (side - pos[1] - 1, pos[0])             # rotate 270
    ]

    while len(positions) > 0:
        cur_pos = positions.pop()

        symmetric_positions = [cur_pos]

        for symmetry_fn in symmetry_fns:
            if is_symmetric(board, symmetry_fn):
                sym_pos = symmetry_fn(cur_pos)

                if sym_pos in positions:
                    positions.remove(sym_pos)
                    symmetric_positions.append(sym_pos)

        collated_positions.append(symmetric_positions)

    return collated_positions


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
    return _move_win_stats(board, cur_player, total_player, _collate_positions)


def move_win_stats_fast(board, cur_player, total_player):
    """Returns the statistics of the current player winning for each
    open move on the board assuming the rules of Tic Tac Toe.

    This is a fast algorithm that utilizes board symmetry to avoid
    replaying moves that are symmetric to already played moves.

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
    return _move_win_stats(board, cur_player, total_player, _collate_symmetric_positions)


def _move_win_stats(board, cur_player, total_player, collate_fn):
    """Returns the statistics of the current player winning for each
    open move on the board assuming the rules of Tic Tac Toe.
    """
    if not isinstance(board, Board):
        raise TypeError("board must be a Board object.")

    win_stats = {}

    open_positions = matching_positions(board, None)
    if len(open_positions) == 0:
        return win_stats

    collated_positions = collate_fn(board, open_positions)

    for positions in collated_positions:
        move_pos = positions.pop()
        move_row = move_pos[0]
        move_col = move_pos[1]
        new_board = board.set(move_row, move_col, cur_player)

        win_stats[move_pos] = [0 for i in range(total_player)]

        if is_winning_move(new_board, move_row, move_col):
            win_stats[move_pos][cur_player] = 1
        else:
            new_player = next_player(cur_player, total_player)
            move_stats = _move_win_stats(new_board, new_player, total_player, collate_fn)
            for stats in move_stats.values():
                for idx, stat in enumerate(stats):
                    win_stats[move_pos][idx] += stat

        for pos in positions:
            win_stats[pos] = win_stats[move_pos].copy()

    return win_stats
