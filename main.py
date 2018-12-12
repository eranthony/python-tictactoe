"""Module docstring"""
from game.board import Board
from game.tictactoe import next_player, is_winning_move, move_win_stats


def _board_pos_idx(board): 
    """Returns a sort function for board locations."""
    if not isinstance(board, Board):
        raise TypeError("board must be a Board object.")

    return lambda pos: pos[0]*board.side_len() + pos[1]


def main():
    """Function docstring"""
    board = Board(3, None)

    win_stats = move_win_stats(board, 0, 2)

    for pos in sorted(win_stats.keys(), key=_board_pos_idx(board)):
        wins_sum = sum(win_stats[pos])
        win_percents = list(map(lambda wins: wins / wins_sum, win_stats[pos]))

        print("({},{}) -> {} -> {}".format(
            pos[0], pos[1], win_stats[pos], win_percents)) 

if __name__ == "__main__":
    main()
