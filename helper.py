import numpy as np

rows = 6
cols = 7

test_table = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [-1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0]
])


def longest_chain(board, maximizingPlayer) -> int:
    longest = 0
    player = 1 if maximizingPlayer else -1

    # Test rows
    for i in range(rows):
        for j in range(cols - 3):
            value = sum(board[i][j:j + 4])
            if value * player > 0:
                longest = max(longest, value)

    # Test cols
    for i in range(rows-3):
        for j in range(cols):
            window = board[i:i + 4, j]
            value = sum(window)
            if value * player > 0:
                longest = max(longest, value)

    # Test diagonal
    for i in range(rows - 3):
        for j in range(cols - 3):
            value = 0
            for k in range(4):
                value += board[i + k][j + k]
                if value * player > 0:
                    longest = max(longest, value)

    reversed_board = np.fliplr(board)
    # Test reverse diagonal
    for i in range(rows - 3):
        for j in range(cols - 3):
            value = 0
            for k in range(4):
                value += reversed_board[i + k][j + k]
                if value * player > 0:
                    longest = max(longest, value)

    return longest


def eval_score(board, player):
    score = longest_chain(board, player) * 10

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == player:
                score -= abs(3-j)
            # elif board[i][j] == player*(-1):
            #     score += abs(3-j)

    return score


def is_win_state(board) -> bool:
    # Test rows
    for i in range(rows):
        for j in range(cols - 3):
            value = sum(board[i][j:j + 4])
            if abs(value) == 4:
                return True

    # Test columns on transpose array
    reversed_board = [list(i) for i in zip(*board)]
    for i in range(cols):
        for j in range(rows - 3):
            value = sum(reversed_board[i][j:j + 4])
            if abs(value) == 4:
                return True

    # Test diagonal
    for i in range(rows - 3):
        for j in range(cols - 3):
            value = 0
            for k in range(4):
                value += board[i + k][j + k]
                if abs(value) == 4:
                    return True

    reversed_board = np.fliplr(board)
    # Test reverse diagonal
    for i in range(rows - 3):
        for j in range(cols - 3):
            value = 0
            for k in range(4):
                value += reversed_board[i + k][j + k]
                if abs(value) == 4:
                    return True

    return False


def available_moves(board):
    moves = []
    for col in range(cols):
        if board[0][col] == 0:
            moves.append(col)

    return moves
