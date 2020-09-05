from utils import block_to_text, separate_bytes

def plaintext(p):
    generic("PLAINTEXT:", p)

def key(k):
    generic("KEY:", k)

def generic(prefix, data):
    print("{0:20}{1}".format(prefix, data))

def round_based(round, log_type, data):
    prefix = "round[{0:2}].{1}".format(round, log_type)
    generic(prefix, block_to_text(data))

def input(round, data):
    round_based(round, "input", data)

def k_sch(round, data):
    key = []
    for i in data:
        key.append("{:0>8}".format(hex(i).split('0x')[1]))
    prefix = "round[{0:2}].{1}".format(round, "k_sch")
    generic(prefix, ''.join(key))

def start(round, data):
    round_based(round, "start", data)

def sub_byte(round, data):
    round_based(round, "s_box", data)

def shift_row(round, data):
    round_based(round, "s_row", data)

def mix_column(round, data):
    round_based(round, "m_col", data)

def output(round, data):
    round_based(round, "output", data)

def ik_add(round, data):
    round_based(round, "ik_add", data)

def encrypt():
    print("CIPHER (ENCRYPT):")

def decrypt():
    print("CIPHER (DECRYPT):")