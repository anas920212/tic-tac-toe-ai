import random

def insertLetter(letter, pos, board):
    board[pos] = letter

def spaceIsFree(pos, board):
    return board[pos] == ' '

def printBoard(board):
    print(f'\n {board[1]} | {board[2]} | {board[3]} \n-----------\n {board[4]} | {board[5]} | {board[6]} \n-----------\n {board[7]} | {board[8]} | {board[9]} \n')

def isWinner(bo, le):
    return ((bo[7]==le and bo[8]==le and bo[9]==le) or (bo[4]==le and bo[5]==le and bo[6]==le) or 
            (bo[1]==le and bo[2]==le and bo[3]==le) or (bo[1]==le and bo[4]==le and bo[7]==le) or 
            (bo[2]==le and bo[5]==le and bo[8]==le) or (bo[3]==le and bo[6]==le and bo[9]==le) or 
            (bo[1]==le and bo[5]==le and bo[9]==le) or (bo[3]==le and bo[5]==le and bo[7]==le))

def isBoardFull(board):
    return board.count(' ') <= 1

def minimax(board, depth, isMaximizing):
    if isWinner(board, 'O'): return 1
    if isWinner(board, 'X'): return -1
    if isBoardFull(board): return 0

    if isMaximizing:
        bestScore = -float('inf')
        for i in range(1, 10):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float('inf')
        for i in range(1, 10):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                bestScore = min(score, bestScore)
        return bestScore

def get_smart_move(board):
    bestScore = -float('inf')
    bestMove = 0
    for i in range(1, 10):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = i
    return bestMove

def compMove(board, win_streak):
    if win_streak < 2 and random.random() < 0.3:
        possibleMoves = [x for x, l in enumerate(board) if l == ' ' and x != 0]
        return random.choice(possibleMoves)
    else:
        return get_smart_move(board)

def check_win_combination(board):
    win_combinations = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),
        (1, 4, 7), (2, 5, 8), (3, 6, 9),
        (1, 5, 9), (3, 5, 7)
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != ' ':
            return combo
    return None