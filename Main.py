import copy
import utils

def new_board(): 
    board = [
             [None, None, None],
             [None, None, None],
             [None, None, None]
            ]
    return board 

def render(board):
    rows = []
    for y in range(0, 3):
        row = []
        for x in range(0, 3):
            row.append(board[x][y])
        rows.append(row)

    row_num = 0
    print('  0 1 2 ')
    print('  ------')
    for row in rows:
        output_row = ''
        for sq in row:
            if sq is None:
                output_row += ' '
            else:
                output_row += sq
        print("%d|%s|" % (row_num, ' '.join(output_row)))
        row_num += 1
    print('  ------')

def make_move(player, board, move_co_ords):
    if board[move_co_ords[0]][move_co_ords[1]] is not None:
        raise Exception("Illegal move!")

    board[move_co_ords[0]][move_co_ords[1]] = player

    
def is_board_full(board):
    for col in board:
        for sq in col:
            if sq is None:
                return False
    return True

def get_all_line_co_ords():
    cols = []
    for x in range(0, 3):
        col = []
        for y in range(0, 3):
            col.append((x, y))
        cols.append(col)

    rows = []
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


def get_winner(board):
    all_line_co_ords = get_all_line_co_ords()

    for line in all_line_co_ords:
        line_values = [board[x][y] for (x, y) in line]
        if len(set(line_values)) == 1 and line_values[0] is not None:
            return line_values[0]

    return None

def get_move(board, current_player_id):
    return minimax_ai(board, current_player_id)

def minimax_ai(board, who_am_i):
    best_move = None
    best_score = None

    for move in utils.get_all_legal_moves(board):
        _board = copy.deepcopy(board)
        make_move(who_am_i, _board, move)

        opp = utils.get_opponent(who_am_i)
        score = _minimax_score(_board, opp, who_am_i)
        if best_score is None or score > best_score:
            best_move = move
            best_score = score

    return best_move

def _minimax_score(board, player_to_move, player_to_optimize):
    winner = get_winner(board)
    if winner is not None:
        if winner == player_to_optimize:
            return 10
        else:
            return -10
    elif is_board_full(board):
        return 0

    legal_moves = utils.get_all_legal_moves(board)

    scores = []
    for move in legal_moves:
        _board = copy.deepcopy(board)
        make_move(player_to_move, _board, move)

        opp = utils.get_opponent(player_to_move)
        opp_best_response_score = _minimax_score(_board, opp, player_to_optimize)
        scores.append(opp_best_response_score)

    if player_to_move == player_to_optimize:
        return max(scores)
    else:
        return min(scores)


def play(player1_f, player2_f):

    players = [
        ('X', player1_f),
        ('O', player2_f),
    ]

    turn_number = 0
    board = new_board()

    while True:

        current_player_id, current_player_f = players[turn_number % 2]
        
        render(board)

        #x = int(input("What is your moves x coordinates --> "))
        #y = int(input("What is your moves y coordinates --> "))
        #move_co_ords = (x,y)

        if (turn_number % 2 ) == 0 :
            xy = (input ("What is your moves x and y coordinates ---> X,Y\n                                       ---> "))
            move_co_ords = list(map(int, xy.split(","))) 
        else :
            move_co_ords = get_move(board, current_player_id)

        make_move(current_player_id, board, move_co_ords)

        winner = get_winner(board)
        if winner is not None:
            render(board)
            if (winner == players[0][0]) :
                print("%s HAS WON !!!" % player1_f)
            else :
                print("AI HAS WON !!!") 
            break

        if is_board_full(board):
            render(board)
            print("IT'S A DRAW !!!")
            break

        turn_number += 1

play("PLAYER 1", "PLAYER 2")
