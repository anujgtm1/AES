from key_expansion import subWord, rotWord
from utils import combine_byte, separate_bytes, mix_matrix, get_rounds, sub_byte, shift_row, create_state_block, print_state_block, convert_block_to_stream, block_to_text
from ff_algorithm import ff_multiply, ff_add
from cipher import addRoundKey
import logger

def inv_subBytes(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] = sub_byte(state[i][j], inverse=True)


def inv_shiftRows(state):
    for i in range(len(state)):
        state[i] = shift_row(state[i], 4 - i)


def inv_mixColumns(state):
    for i in range(4):
        a0 = state[0][i]
        a1 = state[1][i]
        a2 = state[2][i]
        a3 = state[3][i]
        b0 = ff_add(ff_multiply(a0, 0x0e),ff_multiply(a1, 0x0b), ff_multiply(a2, 0x0d), ff_multiply(a3, 0x09))
        b1 = ff_add(ff_multiply(a0, 0x09), ff_multiply(a1, 0x0e), ff_multiply(a2, 0x0b), ff_multiply(a3, 0x0d))
        b2 = ff_add(ff_multiply(a0, 0x0d), ff_multiply(a1, 0x09), ff_multiply(a2, 0x0e), ff_multiply(a3, 0x0b))
        b3 = ff_add(ff_multiply(a0, 0x0b), ff_multiply(a1, 0x0d), ff_multiply(a2, 0x09), ff_multiply(a3, 0x0e))
        state[0][i] = b0
        state[1][i] = b1
        state[2][i] = b2
        state[3][i] = b3


def inv_cipher(data, key, N_k):

    r = 0
    rounds = get_rounds(N_k)

    data = create_state_block(data)
    logger.input(r, data)

    key_sch = key[-4:]
    logger.k_sch(r, key_sch)

    addRoundKey(data, key_sch)

    for r in range(rounds-2, 0, -1):
        logger.start(rounds-r-1, data)

        inv_shiftRows(data)
        logger.shift_row(rounds-r-1, data)

        inv_subBytes(data)
        logger.sub_byte(rounds-r-1, data)

        key_sch = key[4*(r):4*(r+1)]
        logger.k_sch(rounds-r-1, key_sch)

        addRoundKey(data, key_sch)
        logger.ik_add(rounds-r-1, data)

        inv_mixColumns(data)
    logger.start(rounds-r, data)

    inv_subBytes(data)
    logger.sub_byte(rounds-r, data)

    inv_shiftRows(data)
    logger.shift_row(rounds-r, data)

    key_sch = key[0:4]
    logger.k_sch(rounds-r, key_sch)

    addRoundKey(data, key_sch)
    logger.output(rounds-r, data)

    return convert_block_to_stream(data)