"""Hill Cipher — encode/decode messages using matrix multiplication via C engine.

Uses mod-26 arithmetic. The key matrix must have det coprime to 26.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bindings'))

import ctypes
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_matrix_mul.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_mul.restype = ctypes.POINTER(_LAMatrix)


def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def matrix_mod_inverse_2x2(key):
    a, b = int(key[0, 0]), int(key[0, 1])
    c, d = int(key[1, 0]), int(key[1, 1])
    det = (a * d - b * c) % 26
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        raise ValueError(f"det={det} has no inverse mod 26")
    return CMatrix(2, 2, [
        float((d * det_inv) % 26), float(((-b) * det_inv) % 26),
        float(((-c) * det_inv) % 26), float((a * det_inv) % 26),
    ])


def text_to_numbers(text):
    return [ord(c.upper()) - ord('A') for c in text if c.isalpha()]


def numbers_to_text(nums):
    return ''.join(chr(n % 26 + ord('A')) for n in nums)


def hill_transform(text_nums, matrix, n):
    result = []
    for i in range(0, len(text_nums), n):
        block = CMatrix(n, 1, [float(x) for x in text_nums[i:i+n]])
        prod_ptr = _lib.la_matrix_mul(matrix.ptr, block.ptr)
        for r in range(n):
            val = _lib.la_matrix_get(prod_ptr, r, 0)
            result.append(int(round(val)) % 26)
        _lib.la_matrix_free(prod_ptr)
    return result


def encrypt(plaintext, key):
    nums = text_to_numbers(plaintext)
    n = key.rows
    while len(nums) % n != 0:
        nums.append(23)  # pad with 'X'
    return numbers_to_text(hill_transform(nums, key, n))


def decrypt(ciphertext, key):
    inv_key = matrix_mod_inverse_2x2(key)
    nums = text_to_numbers(ciphertext)
    return numbers_to_text(hill_transform(nums, inv_key, key.rows))


if __name__ == '__main__':
    key = CMatrix(2, 2, [3, 3, 2, 5])  # det = 9, gcd(9,26)=1

    message = "HELPME"
    print(f"Original:  {message}")

    encrypted = encrypt(message, key)
    print(f"Encrypted: {encrypted}")

    decrypted = decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")

    assert decrypted[:len(message)] == message, f"Round-trip failed: {decrypted}"
    print("\nRound-trip verified!")
