import numpy as np

rows = 6
cols = 7


def score_table():
    evaluation_table = np.zeros((6, 7), dtype=int)

    for i in range(rows):
        for j in range(cols-3):
            evaluation_table[i, j:j+4] += 1

    for i in range(rows-3):
        for j in range(cols):
            evaluation_table[i:i+4, j] += 1

    for i in range(rows-3):
        for j in range(cols-3):
            for k in range(4):
                evaluation_table[i+k, j+k] += 1

    for i in range(rows-3):
        for j in range(6, 2, -1):
            for k in range(4):
                evaluation_table[i+k, j-k] += 1

    return evaluation_table


def longest_chain(board, maximizingPlayer) -> int:
    longest = 0
    player = 1 if maximizingPlayer else -1

    # Test rows
    for i in range(rows):
        for j in range(cols - 3):
            value = sum(board[i][j:j + 3])
            if value * player > 0:
                longest = max(longest, value)

    # Test columns on transpose array
    reversed_board = [list(i) for i in zip(*board)]
    for i in range(cols):
        for j in range(rows - 3):
            value = sum(reversed_board[i][j:j + 3])
            if value * player > 0:
                longest = max(longest, value)

    # Test diagonal
    for i in range(rows - 3):
        for j in range(cols - 3):
            value = 0
            for k in range(3):
                value += board[i + k][j + k]
                if value * player > 0:
                    longest = max(longest, value)

    reversed_board = np.fliplr(board)
    # Test reverse diagonal
    for i in range(rows - 3):
        for j in range(cols - 3):
            value = 0
            for k in range(3):
                value += reversed_board[i + k][j + k]
                if value * player > 0:
                    longest = max(longest, value)

    return longest


# def longest_chain(board, player):
#     longest = 0
#     for i in range(rows):
#         for j in range(cols):
#             if board[i][j] == player:
#                 longest = max(longest, find_chain(board, row, col, player))

def eval_score(board, player):
    score = longest_chain(board, player) * 10

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == player:
                score += abs(3-j)
            elif board[i][j] == player*-1:
                score -= abs(3-j)

    return score

# def eval_score(board, eval_table):
#     utility = 138
#     sum = 0

#     for i in range(6):
#         for j in range(7):
#             if board[i][j] == 1:
#                 sum += eval_table[i][j]
#             elif board[i][j] == -1:
#                 sum -= eval_table[i][j]

#     print(board)
#     print(f"Score: {utility + sum}")

#     return utility + sum


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
