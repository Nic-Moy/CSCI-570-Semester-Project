import sys
import time
import psutil
from resource import *

#////////////////////// GLOBAL VARIABLES  //////////////////////////
letter_to_idx = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

values_table = [
    [0, 110, 48, 94],  # row 0 = A
    [110, 0, 118, 48],  # row 1 = C
    [48, 118, 0, 110],  # row 2 = G
    [94, 48, 110, 0]]  # row 3 = T

gap_penalty = 30


#//////////////////////  INPUT FUNCTIONS  //////////////////////////

def read_input(path="input1.txt"):
    with open(path) as file:
        lines = []
        for x in file:
            lines.append(x.strip())

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


def write_output(new_sequence, path="output0.txt", ):
    with open(path, 'w') as file:
        file.write(new_sequence)



#//////////////////////  DP FUNCTION  //////////////////////////
def basic_solution(sequence1, sequence2):
    m = len(sequence1)
    n = len(sequence2)
    opt = [[0]*(n+1) for _ in range(m+1)]

    #Initialize column 0 and row 0
    for x in range(1, m+1):
        opt[x][0] = x * gap_penalty
    for y in range(1, n+1):
        opt[0][y] = y * gap_penalty


    for i in range(1,m+1):
        for j in range(1,n+1):
            offset1 = letter_to_idx[sequence1[i-1]]
            offset2 = letter_to_idx[sequence2[j-1]]

            opt[i][j] = min(opt[i-1][j-1] + values_table[offset1][offset2],
                            opt[i-1][j] + gap_penalty,
                            opt[i][j-1] + gap_penalty)

    i, j = m, n
    align_X, align_Y = [], []
    while i > 0 or j > 0:
        # diag?
        if i > 0 and j > 0:
            a = letter_to_idx[sequence1[i - 1]]
            b = letter_to_idx[sequence2[j - 1]]
            if opt[i][j] == opt[i - 1][j - 1] + values_table[a][b]:
                align_X.append(sequence1[i - 1])
                align_Y.append(sequence2[j - 1])
                i, j = i - 1, j - 1
                continue
        # gap in X (left)
        if j > 0 and opt[i][j] == opt[i][j - 1] + gap_penalty:
            align_X.append('_')
            align_Y.append(sequence2[j - 1])
            j -= 1
            continue
        # gap in Y (up)
        if i > 0 and opt[i][j] == opt[i - 1][j] + gap_penalty:
            align_X.append(sequence1[i - 1])
            align_Y.append('_')
            i -= 1
            continue
    aligned_X = ''.join(reversed(align_X))
    aligned_Y = ''.join(reversed(align_Y))
    return opt[m][n], aligned_X, aligned_Y


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 basic_3.py <input_file> <output_file>")
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    sequence1, j_nums, sequence2, k_nums = read_input(input_path)
    new_seq_1 = string_generator(sequence1, j_nums)
    new_seq_2 = string_generator(sequence2, k_nums)

    start_time = time.time()
    cost, aligned_X, aligned_Y = basic_solution(new_seq_1, new_seq_2)
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000
    memory_kb = process_memory()

    with open(output_path, 'w') as file:
        file.write(f"{cost}\n")
        file.write(f"{aligned_X}\n")
        file.write(f"{aligned_Y}\n")
        file.write(f"{time_taken_ms}\n")
        file.write(f"{memory_kb}\n")

if __name__ == "__main__":
    main()
