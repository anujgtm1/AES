from functools import reduce

def ff_add(*a):
    """
    >>> hex(ff_add(0x57,0x83))
    '0xd4'
    """
    return reduce(lambda x, y: x^y, a, 0)

def xtime(a):
    """
    >>> hex(xtime(0x57))
    '0xae'
    >>> hex(xtime(0xae))
    '0x47'
    >>> hex(xtime(0x47))
    '0x8e'
    >>> hex(xtime(0x8e))
    '0x7'
    """
    # print(bin(a), a >> 7)
    return (a << 1 if not a >> 7 else ((a << 1) ^ 0x1b)) & 0xff

def ff_multiply(a, b):
    """
    >>> hex(ff_multiply(0x57,0x13))
    '0xfe'
    """
    # for i in range(b):
    #     a = xtime(a)
    # return a
    p = 0
    for _ in range(8):
        if not a or not b:
            break
        if b & 0x01: 
            p ^= a
        b = b >> 1
        a = xtime(a)
    return p