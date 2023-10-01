def get_opponent(who_am_i):
    if who_am_i == 'X':                          # Determine and return the opponent's symbol based on the current player's symbol
        return 'O'
    elif who_am_i == 'O':
        return 'X'
    else:
        raise Exception("Unknown player: " + who_am_i)          # Raise an exception for an unknown player


def get_all_legal_moves(board):
    legal_moves = []                              # Initialize a list to store legal (empty) moves on the board
    for x, row in enumerate(board):
        for y, val in enumerate(row):
            if val is None:                       # Check if the board square is empty (None)
                legal_moves.append((x, y))        # Append the coordinates of the empty square to the list
    return legal_moves                            # Return the list of legal moves
