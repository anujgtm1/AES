from utils import s_box, r_con, combine_byte, mix_matrix, get_rounds, sub_byte

def subWord(a):
    """
    >>> hex(subWord(0x00102030))
    '0x63cab704'
    >>> hex(subWord(0x40506070))
    '0x953d051'
    >>> hex(subWord(0x8090a0b0))
    '0xcd60e0e7'
    >>> hex(subWord(0xc0d0e0f0))
    '0xba70e18c'
    """
    res = 0
    for i in range(24, -1, -8):
        byte = (a >> i) & 0xff
        res = (res << 8) + sub_byte(byte)
        # print(hex(i), hex(j), hex(sub_byte), hex(res))
    return res

def rotWord(a, i):
    """
    >>> hex(rotWord(0x09cf4f3c, 1))
    '0xcf4f3c09'
    >>> hex(rotWord(0x2a6c7605, 1))
    '0x6c76052a'
    >>> hex(rotWord(0x2a6c7605, 2))
    '0x76052a6c'
    """
    high_byte = a >> (32 - 8*i)
    return (((a << 8*i ) & 0xffffff00) | high_byte)

def key_expansion(key):
    N_k = len(key) // 4
    rounds = get_rounds(N_k)

    expanded_key = []
    for i in range(N_k):
        expanded_key.append(combine_byte(key[i*4: (i+1)*4]))

    for i in range(N_k, 4*(rounds)):
        W_prev = expanded_key[-1]
        W_i_N = expanded_key[i - N_k]
        if i % N_k == 0:
            sub = subWord(rotWord(W_prev, 1))
            r_word = r_con[i // N_k]
            key = W_i_N ^ sub ^ r_word
        elif N_k > 6 and i % N_k == 4:
            sub = subWord(W_prev)
            key = W_i_N ^ sub
        else:
            key = W_i_N ^ W_prev
        expanded_key.append(key)
    return expanded_key

if __name__ == '__main__':
    assert hex(subWord(0x00102030)) == '0x63cab704'