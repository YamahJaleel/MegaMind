import copy
import utils

def new_board():              ## Function to create a new game board ##
    board = [
             [None, None, None],
             [None, None, None],
             [None, None, None]
            ]
    return board 

def render(board):            ## Function to render and display the game board ##
    rows = []
    for y in range(0, 3):                 # Iterate through the rows (vertical) of the game board
        row = []                          # Initialize an empty list to store rows of the game board
        for x in range(0, 3):             # Iterate through the columns (horizontal) of the game board
            row.append(board[x][y])       # Append each square to the current row
        rows.append(row)                  # Append the completed row to the rows list

    row_num = 0                           # Initialize a variable to keep track of the row number for labeling
    print('  0 1 2 ')                     # Display column labels for reference
    print('  ------')                     # Display a horizontal line separator
    for row in rows:                      # Iterate through the rows of the game board
        output_row = ''                   # Initialize an empty string for the current row
        for sq in row:                    # Iterate through the squares in the current row
            if sq is None:
                output_row += ' '         # Add a space for empty squares
            else:
                output_row += sq          # Add the player's symbol for occupied squares
        print("%d|%s|" % (row_num, ' '.join(output_row)))         # Display the row number, the current row, and vertical separators
        row_num += 1                      # Increment the row number for the next iteration
    print('  ------')                     # Display a horizontal line separator to complete the board rendering

def make_move(player, board, move_co_ords):              ## Function to make a move on the game board ##
    if board[move_co_ords[0]][move_co_ords[1]] is not None:             # Check if the target square on the game board is already occupied
        raise Exception("Illegal move!")                                # Raise an exception for an illegal move

    board[move_co_ords[0]][move_co_ords[1]] = player                    # Set the target square on the game board to the current player's symbol

    
def is_board_full(board):                                               # Function to check if the game board is full
    for col in board:                                                   # Iterate through the columns and squares of the game board
        for sq in col:
            if sq is None:
                return False                                            # If an empty square is found, the board is not full
    return True                                                         # If no empty squares are found, the board is full

def get_all_line_co_ords():                             ## Function to get all possible line coordinates (columns, rows, diagonals) ##
    cols = []                                                           # Initialize an empty list to store line coordinates (columns, rows, and diagonals)
    for x in range(0, 3):                                               # Generate coordinates for columns (vertical lines)
        col = []                                                        # Initialize an empty list for each column
        for y in range(0, 3):                                           
            col.append((x, y))                                          # Append each coordinate (x, y) to the current column
        cols.append(col)                                                # Append the completed column to the list of line coordinates

    rows = []                                                           # The same process is repeated for rows (horizontal lines) and diagonals
    for y in range(0, 3):
        row = []
        for x in range(0, 3):
            row.append((x, y))
        rows.append(row)

    diagonals = [
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]
    return cols + rows + diagonals


def get_winner(board):                                             ## Function to determine the winner of the game ##
    all_line_co_ords = get_all_line_co_ords()                                # Get all possible line coordinates (columns, rows, diagonals)

    for line in all_line_co_ords:                                             # Iterate through each line (column, row, or diagonal)
        line_values = [board[x][y] for (x, y) in line]                        # Get the values (player symbols) at each coordinate in the line
        if len(set(line_values)) == 1 and line_values[0] is not None:         # Check if all values in the line are the same and not None
            return line_values[0]                                             # Return the winning player's symbol

    return None                                                               # If no winner is found in any line, return None indicating no winner

def get_move(board, current_player_id):                            ## Function to get the next move for a player using the minimax AI algorithm ##
    return minimax_ai(board, current_player_id)                                 

def minimax_ai(board, who_am_i):                                   ## Minimax AI algorithm for making optimal moves ##
    best_move = None                                                          # Initialize variables to keep track of the best move and its score
    best_score = None                                                         

    for move in utils.get_all_legal_moves(board):                              # Iterate through all legal moves on the current game board
        _board = copy.deepcopy(board)                                          # Create a copy of the board to simulate the move
        make_move(who_am_i, _board, move)                                      # Simulate the move

        opp = utils.get_opponent(who_am_i)                                     # Determine the opponent's symbol
        score = _minimax_score(_board, opp, who_am_i)                          # Get the score for the simulated move
        if best_score is None or score > best_score:                           # Update the best move and its score if a better move is found
            best_move = move
            best_score = score

    return best_move                                                           # Return the best move found by the minimax AI algorithm

def _minimax_score(board, player_to_move, player_to_optimize):      ## Helper function to calculate the minimax score for a given board state ##
    winner = get_winner(board)                                                        # Check if there is a winner on the current board state
    if winner is not None:                                                            # If there is a winner, return a score based on whether it's the optimizing player
        if winner == player_to_optimize:
            return 10                                                                 # The optimizing player wins
        else:
            return -10                                                                # The opponent wins
    elif is_board_full(board):
        return 0                                                                      # If the board is full and there's no winner, return a neutral score (draw)

    legal_moves = utils.get_all_legal_moves(board)                                    # Get all legal moves for the current player

    scores = []                                                                       # Initialize a list to store scores for each potential move
    for move in legal_moves:
        _board = copy.deepcopy(board)                                                 # Create a copy of the board to simulate the move
        make_move(player_to_move, _board, move)                                       # Simulate the move

        opp = utils.get_opponent(player_to_move)                                      # Determine the opponent's symbol
        opp_best_response_score = _minimax_score(_board, opp, player_to_optimize)     # Recursively calculate the opponent's best response score
        scores.append(opp_best_response_score)                                        # Add the opponent's best response score to the list

    if player_to_move == player_to_optimize:                                          # If it's the optimizing player's turn, return the maximum score from the opponent's moves
        return max(scores)
    else:                                                                             # If it's the opponent's turn, return the minimum score from the opponent's moves
        return min(scores)                          


def play(player1_f, player2_f):                                 ## Function to play the game between two players or a player and the AI ##

    players = [                                                             # Define the players as symbols ('X' and 'O') and their respective functions
        ('X', player1_f),                                                   # Player 1 with symbol 'X'
        ('O', player2_f),                                                   # Player 2 or AI with symbol 'O'
    ]

    turn_number = 0                                                          # Initialize the turn counter
    board = new_board()                                                      # Initialize the game board

    while True:

        current_player_id, current_player_f = players[turn_number % 2]       # Determine the current player's symbol and function
        
        render(board)                                                        # Display the current game board

        if (turn_number % 2 ) == 0 :
            xy = (input ("Enter your moves in this format ---> X,Y\n                                ---> "))
            move_co_ords = list(map(int, xy.split(",")))                    # Parse the player's move from user input
        else :
            move_co_ords = get_move(board, current_player_id)               # Get the AI's or player's move

        make_move(current_player_id, board, move_co_ords)                   # Make the current player's move on the board

        winner = get_winner(board)                                          # Check if there's a winner
        if winner is not None:
            render(board)                                                   # Display the final game board
            if (winner == players[0][0]) :
                print("%s HAS WON !!!" % player1_f)                         # Player 1 wins
            else :
                print("MegaMind HAS WON !!!")                               # MegaMind wins
            break

        if is_board_full(board):
            render(board)                                                   # Display the final game board
            print("IT'S A DRAW !!!")                                        # The game ends in a draw
            break

        turn_number += 1                                                    # Increment the turn counter

play("PLAYER 1", "PLAYER 2")                    # Start the game with two players
