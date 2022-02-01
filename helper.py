import numpy as np


def score_table():
    rows = 6
    cols = 7
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

    print(evaluation_table)
    return evaluation_table
