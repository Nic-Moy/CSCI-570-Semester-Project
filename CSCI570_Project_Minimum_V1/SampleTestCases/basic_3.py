import sys
import time
#import psutil
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

def read_input(path="input0.txt"):
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
def basic_solution():
    pass


#//////////////////////  MAIN FUNCTION  //////////////////////////
sequence1, j_nums, sequence2, k_nums = read_input()
new_seq_1 = string_generator(sequence1, j_nums)
new_seq_2 = string_generator(sequence2, k_nums)
write_output(new_seq_1)
