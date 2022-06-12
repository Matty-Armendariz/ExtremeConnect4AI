# Matty Armendariz
# CSCI 599 
# Max connect 4 Project

import numpy as np
import random 
import sys
import math
import colorama
from colorama import Fore, Back, Style 
colorama.init(autoreset = True)

#java maxconnect4 interactive [input_file] [computer-next/human-next] [depth]
# python3 maxconnect4.py interactive input_file next-Player depth
#print(len(sys.argv))

EMPTY = 0
SEQUENCE_LENGTH = 4

mode = sys.argv[1]
inputFile = sys.argv[2]
nextPlayer = sys.argv[3]
depth = int(sys.argv[4])

ROWS = 6
COLUMNS = 7

# making the board from the input file
filename = inputFile
f = open(filename, "r")
Lines = f.readlines()
matrix = np.zeros((ROWS,COLUMNS))
tempMatrix = np.zeros((ROWS,COLUMNS))

#print(matrix)


row = 0
for line in Lines[:-1]:
    for col in range(COLUMNS):
        # Storing the appropriate values in the matrix
        #print(str(row) + ", " + str(col))
        tempMatrix[row][col] = int(line[col])
    row += 1

whosTurn = int(Lines[-1])

tempMatrix = np.flip(tempMatrix, 0)

for x in range(ROWS):
    for y in range(COLUMNS):
        matrix[x][y] = tempMatrix[x][y]


# all of the functions needed to run the program

# This is just to place the the piece in the right cell
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Checks to see if the proposed move is valid
def is_valid_move(board, col):
    # matrix is flipped so it is more intuative
    # print(str(ROWS-1) + " " + str(col))
    if board[ROWS-1][col] == 0:
        return True
    else:
        return False

# finds the next open row within a column
def get_next_open_cell(board, col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_sequence(sequence, piece, oppPiece):
    score = 0
    opp_piece = oppPiece
    # if piece == PLAYER_PIECE:
    #     opp_piece = AI_PIECE
    # piece 

    if sequence.count(piece) == 4:
        score += 100
    elif sequence.count(piece) == 3 and sequence.count(EMPTY) == 1:
        score += 5
    elif sequence.count(piece) == 2 and sequence.count(EMPTY) == 2:
        score += 2

    if sequence.count(opp_piece) == 3 and sequence.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    currPiece = piece
    if currPiece == 1:
        oppPiece = 2
    if currPiece == 2:
        oppPiece = 1

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMNS//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMNS-3):
            sequence = row_array[c:c+SEQUENCE_LENGTH]
            score += evaluate_sequence(sequence, piece, oppPiece)

    ## Score Vertical
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            sequence = col_array[r:r+SEQUENCE_LENGTH]
            score += evaluate_sequence(sequence, piece, oppPiece)

    ## Score posiive sloped diagonal
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            sequence = [board[r+i][c+i] for i in range(SEQUENCE_LENGTH)]
            score += evaluate_sequence(sequence, piece, oppPiece)

    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            sequence = [board[r+3-i][c+i] for i in range(SEQUENCE_LENGTH)]
            score += evaluate_sequence(sequence, piece, oppPiece)

    return score

# This is where the minimax as well as the alpha beta prning happens
def minimax(board, depth, alpha, beta, maximizingPlayer, playerNum,oppNum):
    # print("What")
    # getting the valie locations for the board
    validLocations = get_validLocations(board)
    gameOver = is_game_over(board)
    # first check if you are at the end of the depth or all moves have taken place
    if depth == 0 or gameOver:
        # check who won the game
        if gameOver:
            if winning_move(board, playerNum):
                return (None, math.inf)
            elif winning_move(board, oppNum):
                return (None, -math.inf)
        # this is if you have hit max depth of the function it will return the score 
        else:
            return (None, score_position(board, playerNum))
    # this is for the player that calls the function
    if maximizingPlayer:
        # setting the value to -inf to start off 
        value = -math.inf
        column = random.choice(validLocations)

        for col in validLocations:
            row = get_next_open_cell(board, col)
            # make the board a copy or else it will mess with the actual value of the board
            tempBoard = board.copy()
            drop_piece(tempBoard, row, col, playerNum)
            # recursively calling minimax to find the best outcome
            newScore = minimax(tempBoard, depth-1, alpha, beta, False, playerNum, oppNum)[1]
            # if the score is better than the value it will be set to the new value
            if newScore > value:
                value = newScore
                column = col
            # The alpha is changed to the max of the itself and the new value
            alpha = max(alpha, value)
            # this is wher the pruning for the max player happens
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        # very large number 
        value = math.inf
        column = random.choice(validLocations)
        #iterating though all of the valid locations
        for col in validLocations:
            row = get_next_open_cell(board, col)
            tempBoard = board.copy()
            drop_piece(tempBoard, row, col, oppNum)
            # recursive call of the minimax but passing it off to the max player
            newScore = minimax(tempBoard, depth-1, alpha, beta, True, playerNum, oppNum)[1]
            # changing the score dependent on the result
            if newScore < value:
                value = newScore
                column = col
            # this is where the pruning for the minimizing player happens
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# getting all of the possible locations you can move to
def get_validLocations(board):
    validLocations = []
    # just parses through the columns and makes sure you can move there 
    for col in range(COLUMNS):
        if is_valid_move(board, col):
            validLocations.append(col)

    return validLocations

# don't need this now that I have the pretty one
# def print_board(board):
#     print(np.flip(board, 0))

# printing out the board in an appealing way
def draw_board(board):
    count = 0
    for x in reversed(board):
        print("| ", end="")
        for y in range(COLUMNS):
            if int(x[y]) == 0:
                print(Fore.BLACK + Back.BLACK + str(int(x[y])), end=" | " )
            if int(x[y]) == 1:
                print(Fore.RED + str(int(x[y])), end=" | " )
            if int(x[y]) == 2:
                print(Fore.GREEN + str(int(x[y])), end=" | " )
            # print(str(int(x[y])) + " | " , end="")
        print()

        # #count = count + 1
        # if count >= COLUMNS:
        #     break
    print(" ---------------------------")

def draw_to_file(board, file, nextTurn):
    f = open(file, "w")
    for x in reversed(board):
        rowString = ""
        for y in range(COLUMNS):
            rowString = rowString + str(int(x[y]))

        f.write(rowString)
        f.write("\n")
    f.write(str(nextTurn))
    f.close()

def adding_points(board, piece):

    totalPoints = 0
    # Check horizontal locations for win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                totalPoints += 1
                break

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                totalPoints += 1
                break

    # Check positively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                totalPoints += 1
                break

    # Check negatively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                totalPoints += 1
                break

    return totalPoints

def display_score(board):
    
    # Red is always 1
    RedScore = 0
    # Green is always 2
    GreenScore = 0

    # SCORING RED
    RedScore += adding_points(board, 1)
    # SCORING GREEN
    GreenScore += adding_points(board, 2)

    print("         Score: " + str(RedScore) +"-"+str(GreenScore))
    print("         (red first)")

def is_game_over(board):
    validLocations = get_validLocations(board)
    if len(validLocations) == 0:
        return True
    else:
        return False

def display_winner(board):
    
    # Red is always 1
    RedScore = 0
    # Green is always 2
    GreenScore = 0

    # SCORING RED
    RedScore += adding_points(board, 1)
    # SCORING GREEN
    GreenScore += adding_points(board, 2)

    if RedScore > GreenScore:
        print("Red Player Has won!")
    if RedScore < GreenScore:
        print("Green Player Has won!")
    if RedScore == GreenScore:
        print("It was a tie!")
    print("Score: " + str(RedScore) +"-"+str(GreenScore))
    print("(red first)")

def is_game_over(board):
    validLocations = get_validLocations(board)
    if len(validLocations) == 0:
        return True
    else:
        return False

if mode == "interactive":

    PLAYER = 0
    AI = 1

    if nextPlayer == "computer-next":
        turn = AI
        if whosTurn == 1:
            AI_PIECE = 1
            PLAYER_PIECE = 2
        else:
            AI_PIECE = 2
            PLAYER_PIECE = 1
    
    if nextPlayer == "human-next":
        turn = PLAYER
        if whosTurn == 1:
            AI_PIECE = 2
            PLAYER_PIECE = 1
        if whosTurn == 2:
            AI_PIECE = 1
            PLAYER_PIECE = 2


    # If computer-next, goto 2, else goto 5.
    # Print the current board state and score. If the board is full, exit.
    # Choose and make the next move.
    # Save the current board state in a file called computer.txt (in same format as input file).
    # Print the current board state and score. If the board is full, exit.
    # Ask the human user to make a move (make sure that the move is valid, otherwise repeat request to the user).
    # Save the current board state in a file called human.txt (in same format as input file).
    # Goto 2.

    # # This is where the actual game takes place
    # if nextPlayer == "computer-next":
    #     turn = AI
    # else:
    #     turn = PLAYER

    game_over = False

    while not game_over:

        if turn == AI:
            
            print("Computer's Turn")
            draw_board(matrix)
            #display_score(matrix)

            col, minimax_score = minimax(matrix, depth, -math.inf, math.inf, True, AI_PIECE, PLAYER_PIECE)
            # print("Col = " + str(col))
            if is_valid_move(matrix, col):
                row = get_next_open_cell(matrix, col)
                drop_piece(matrix, row, col, AI_PIECE)

            turn += 1
            turn = turn % 2
            draw_to_file(matrix, "computer.txt", turn )

        # break in case the computer is the last to make a move
        game_over = is_game_over(matrix)
        if game_over == True:
            break

        if turn == PLAYER:
            print()
            print("Human Turn")
            # drawing the current board
            draw_board(matrix)
            display_score(matrix)
            print()

            # Player's turn
            validMove = False

            # remember, the player will think it is indexed at 1
            while validMove == False:
                print("Player, please choose your next move")
                playerCol = input("Please Choose Column: ")
                playerCol = int(playerCol)
                playerCol = playerCol-1
                validMove = is_valid_move(matrix, playerCol)
            
            # if it is a valid move 
            row = get_next_open_cell(matrix, playerCol)
            drop_piece(matrix, row, playerCol, PLAYER_PIECE)

            # if winning_move(matrix, PLAYER_PIECE):
            #     print("Human Won!")
            #     game_over = True

            turn += 1
            turn = turn % 2

            draw_to_file(matrix,"human.txt",turn)

    # if you reach here that means you have finished the game
    print()
    display_winner(matrix)
    draw_board(matrix)

if mode == "one-move":

    if inputFile == "red_next.txt":
        PIECE = 1
        OPP_PIECE = 2
        nt = 2
    elif inputFile == "green_next.txt":
        PIECE = 2
        OPP_PIECE = 1
        nt = 1
    else: 
        if whosTurn == 1:
            PIECE = 1
            OPP_PIECE = 2
            nt = 2
        else:
            PIECE = 2
            OPP_PIECE = 1
            nt = 1

    print("Current Board")
    draw_board(matrix)
    print(".")
    print(".")
    print(".")
    print("Board After Move")
    col, minimax_score = minimax(matrix, depth, -math.inf, math.inf, True, PIECE, OPP_PIECE)
    # print("Col = " + str(col))
    if is_valid_move(matrix, col):
        row = get_next_open_cell(matrix, col)
        drop_piece(matrix, row, col, PIECE)

    draw_board(matrix)

    draw_to_file(matrix, nextPlayer, nt )