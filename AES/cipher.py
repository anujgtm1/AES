from key_expansion import subWord, rotWord
from utils import combine_byte, separate_bytes, mix_matrix, get_rounds, sub_byte, shift_row, create_state_block, print_state_block, convert_block_to_stream, block_to_text
from ff_algorithm import ff_multiply, ff_add
import logger

def subBytes(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] = sub_byte(state[i][j])


def shiftRows(state):
    for i in range(len(state)):
        state[i] = shift_row(state[i], i)


def mixColumns(state):
    for i in range(4):
        a0 = state[0][i]
        a1 = state[1][i]
        a2 = state[2][i]
        a3 = state[3][i]
        b0 = ff_add(ff_multiply(a0, 2),ff_multiply(a1, 3), a2, a3)
        b1 = ff_add(a0, ff_multiply(a1, 2), ff_multiply(a2, 3), a3)
        b2 = ff_add(a0, a1, ff_multiply(a2, 2), ff_multiply(a3, 3))
        b3 = ff_add(ff_multiply(a0, 3), a1, a2, ff_multiply(a3, 2))
        state[0][i] = b0
        state[1][i] = b1
        state[2][i] = b2
        state[3][i] = b3


def addRoundKey(state, round_key):
    for i in range(len(state)):
        r_key = separate_bytes(round_key[i])
        for j in range(len(state[0])):
            state[j][i] = ff_add(state[j][i], r_key[j])
            # print(hex(d), hex(r_key[j]), hex(state[j][i]))
    # test = []
    # for i in range(4):
    #     test.append([])
    #     for j in range(4):
    #         test[-1].append(hex(state[i][j]))
    # print(test)


def cipher(data, key, N_k):

    r = 0
    rounds = get_rounds(N_k)

    data = create_state_block(data)
    logger.input(r, data)

    key_sch = key[0:4]
    logger.k_sch(r, key_sch)

    addRoundKey(data, key_sch)
    for r in range(1, rounds-1):
        logger.start(r, data)

        subBytes(data)
        logger.sub_byte(r, data)

        shiftRows(data)
        logger.shift_row(r, data)

        mixColumns(data)
        logger.mix_column(r, data)

        key_sch = key[4*r:4*(r+1)]
        logger.k_sch(r, key_sch)

        addRoundKey(data, key_sch)
    r += 1
    logger.start(r, data)

    subBytes(data)
    logger.sub_byte(r, data)

    shiftRows(data)
    logger.shift_row(r, data)

    key_sch = key[-4:]
    logger.k_sch(r, key_sch)

    addRoundKey(data, key_sch)
    logger.output(r, data)

    return convert_block_to_stream(data)

