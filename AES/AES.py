from utils import read_plaintext_to_stream, convert_stream_to_plaintext
from cipher import cipher
from inv_cipher import inv_cipher
from key_expansion import key_expansion
import logger


def encrypt_decrypt(plaintext, key, decrypt=False):
    logger.plaintext(plaintext)
    logger.key(key)
    data = read_plaintext_to_stream(plaintext)
    key = read_plaintext_to_stream(key)

    N_k = len(key) // 4
    key = key_expansion(key)
    if not decrypt:
        logger.encrypt()
        result = cipher(data, key, N_k)
    else:
        logger.decrypt()
        result = inv_cipher(data, key, N_k)
    return result

def encrypt(plaintext, key):
    return encrypt_decrypt(plaintext, key)

def decrypt(plaintext, key):
    return encrypt_decrypt(plaintext, key, decrypt=True)


if __name__ == '__main__':
    data = [
        ("00112233445566778899aabbccddeeff", "000102030405060708090a0b0c0d0e0f"),
        ("00112233445566778899aabbccddeeff", "000102030405060708090a0b0c0d0e0f1011121314151617"),
        ("00112233445566778899aabbccddeeff", "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
    ]
    for plaintext, key in data:
        encrypted = encrypt(plaintext, key)
        print("")
        decrypt(convert_stream_to_plaintext(encrypted), key)
        print("\n")