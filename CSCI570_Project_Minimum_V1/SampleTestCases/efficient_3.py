# efficient_3.py

import sys
import time
from resource import *
import psutil

#////////////////////// GLOBAL VARIABLES  //////////////////////////
gap_penalty = 30
letter_to_idx = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
values_table = [
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]
]

#//////////////////////  INPUT FUNCTIONS  //////////////////////////
# same as basic
def read_input(path):
    with open(path) as file:
        lines = [x.strip() for x in file]
        sequence1 = lines[0]
        index = 1
        j_nums = []
        while lines[index].isdigit():
            j_nums.append(int(lines[index]))
            index += 1
        sequence2 = lines[index]
        k_nums = []
        index += 1
        while index < len(lines) and lines[index].isdigit():
            k_nums.append(int(lines[index]))
            index += 1
    return sequence1, j_nums, sequence2, k_nums

def string_generator(sequence, nums):
    new_sequence = sequence
    for i in nums:
        temp1 = new_sequence[:i + 1]
        temp2 = new_sequence[i + 1:]
        new_sequence = temp1 + new_sequence + temp2
    return new_sequence

#//////////////////////  FUNCTIONS  //////////////////////////

# we need this to get the costs for L and R
def cost_only(X, Y):
    # init the first row of the DP table
    #  cost of aligning empty X with prefixes of Y
    m, n = len(X), len(Y)
    prev = [j * gap_penalty for j in range(n + 1)]
    curr = [0] * (n + 1)

    # first column: cost of aligning X[R] with empty Y
    for i in range(1, m + 1):
        curr[0] = i * gap_penalty
        for j in range(1, n + 1):
            a = letter_to_idx[X[i - 1]]
            b = letter_to_idx[Y[j - 1]]
            # Compute minimum cost of:
            # 1. match/mismatch
            # 2. gap in X
            # 3. gap in Y
            curr[j] = min(
                prev[j - 1] + values_table[a][b],
                prev[j] + gap_penalty,
                curr[j - 1] + gap_penalty
            )
        prev, curr = curr, prev
    return prev

# we avoid calculating the entire m*n table
# we use the divide and conquer and our helper functions
def efficient(X, Y):
    # base cases are straight forward
    if len(X) == 0:
        return '_' * len(Y), Y
    elif len(Y) == 0:
        return X, '_' * len(X)
    elif len(X) == 1 or len(Y) == 1:
        return basic_solution(X, Y)[1:]  # ignore cost, we just care about alignment
    else:
        mid = len(X) // 2
        # Compute cost of aligning R with Y - forward pass
        L = cost_only(X[:mid], Y)
        # compute cost of aligning L with Y - backlward pass
        # we use backwards strings so that we do not need to redo logic
        # our idea was that we use backwards because we need to align it with Y[n]
        R = cost_only(X[mid:][::-1], Y[::-1])
        total = [L[i] + R[len(Y) - i] for i in range(len(Y) + 1)]
        split = total.index(min(total))

        #divide and conquer baby

        left_X, left_Y = efficient(X[:mid], Y[:split])
        right_X, right_Y = efficient(X[mid:], Y[split:])
        return left_X + right_X, left_Y + right_Y


### samew as before 
def basic_solution(X, Y):
    m, n = len(X), len(Y)
    opt = [[0]*(n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        opt[i][0] = i * gap_penalty
    for j in range(1, n+1):
        opt[0][j] = j * gap_penalty

    for i in range(1, m+1):
        for j in range(1, n+1):
            a = letter_to_idx[X[i - 1]]
            b = letter_to_idx[Y[j - 1]]
            opt[i][j] = min(
                opt[i - 1][j - 1] + values_table[a][b],
                opt[i - 1][j] + gap_penalty,
                opt[i][j - 1] + gap_penalty
            )

    i, j = m, n
    align_X, align_Y = [], []
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            a = letter_to_idx[X[i - 1]]
            b = letter_to_idx[Y[j - 1]]
            if opt[i][j] == opt[i - 1][j - 1] + values_table[a][b]:
                align_X.append(X[i - 1])
                align_Y.append(Y[j - 1])
                i -= 1
                j -= 1
                continue
        if j > 0 and opt[i][j] == opt[i][j - 1] + gap_penalty:
            align_X.append('_')
            align_Y.append(Y[j - 1])
            j -= 1
            continue
        if i > 0 and opt[i][j] == opt[i - 1][j] + gap_penalty:
            align_X.append(X[i - 1])
            align_Y.append('_')
            i -= 1
            continue
    return opt[m][n], ''.join(reversed(align_X)), ''.join(reversed(align_Y))

# helper function to compute the cost
# in basic it was inbuilt into the dp
# but because we use different methodology here it was easier to create aa helper function
def alignment_cost(X, Y):
    cost = 0
    for a, b in zip(X, Y):
        if a == '_' or b == '_':
            cost += gap_penalty
        else:
            i = letter_to_idx[a]
            j = letter_to_idx[b]
            cost += values_table[i][j]
    return cost


##### same as before
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 efficient_3.py <input_file> <output_file>")
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    seq1, j_nums, seq2, k_nums = read_input(input_path)
    full_seq1 = string_generator(seq1, j_nums)
    full_seq2 = string_generator(seq2, k_nums)

    start_time = time.time()
    aligned_X, aligned_Y = efficient(full_seq1, full_seq2)
    end_time = time.time()
    total_cost = alignment_cost(aligned_X, aligned_Y)
    total_time = (end_time - start_time) * 1000
    memory_kb = process_memory()

    with open(output_path, 'w') as f:
        f.write(f"{total_cost}\n")
        f.write(f"{aligned_X}\n")
        f.write(f"{aligned_Y}\n")
        f.write(f"{total_time:.3f}\n")
        f.write(f"{memory_kb:.3f}\n")

if __name__ == "__main__":
    main()
