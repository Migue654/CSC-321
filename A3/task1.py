from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
import string

# sha256_hash(input_string):
#  FUNCTION sha256_hash(input_string):
#     Convert input_string to bytes
#     Calculate SHA256 hash of the bytes
#     Return the hash as a hexadecimal string
#  END FUNCTIONYou may use a different
# way to truncate a hash...in this way I am bit shifting but you may find another way.

def sha256_hash(string):
    byte_string = string.encode()
    hashed = SHA256.new(byte_string)

    return hashed.hexdigest


# truncate_hash(hash_string, bits):
#  FUNCTION truncate_hash(hash_string, bits):
#     Take the first (bits / 4) characters of hash_string
#     Convert this substring to an integer (base 16)
#     Create a bitmask of 'bits' number of 1s
#     Perform bitwise AND between the integer and the bitmask
#     Return the result
#  END FUNCTION
#    )

def truncate_hash(hash_string,bits):
    truncated = hash_string[0 : bits // 4]

    int_convert = int(truncated, 16)

    mask = (1 << bits) - 1

    return int_convert & mask

# hamming_distance(s1, s2):
#  FUNCTION hamming_distance(s1, s2):
#     Initialize count to 0
#     FOR each pair of characters (c1, c2) in (s1, s2):
#         IF c1 != c2:
#             Increment count
#     RETURN count
#  END FUNCTIONYou may use a different approach rather than hamming

def hamming_distance (s1,s2):
    count = 0
    for (c1,c2) in (s1,s2):
        if c1 != c2:
            count+=1

    return count


# ind_hamming_distance_1():
#  FUNCTION find_hamming_distance_1():
#     Generate a random string 'base' of 10 ASCII letters
#     FOR each index i in base:
#         Create 'modified' by flipping the i-th bit of base
#         IF hamming_distance(base, modified) == 1:
#             RETURN base, modified
#     RETURN None, None
#  END FUNCTION


def finding_hamming_distance_1():
    letter = string.ascii_letters
    base = "".join(random.choices(letter, k=10))

    for i in range(len(base) * 8):
        modified = bytearray(base.encode())

        byte_index = i // 8
        bit_index = i % 8

        modified[byte_index] ^= 1 << bit_index

        modified = modified.decode()

        if hamming_distance(base, modified) == 1:
            return base, modified

    return None, None

# find_collision(bits, max_attempts):
#  FUNCTION find_collision(bits, max_attempts):
#     Initialize empty dictionary 'seen'
#     Record start time
#     FOR attempts from 1 to max_attempts:
#         Generate random string 's' of 10 ASCII letters
#         Calculate truncated hash 'h' of 's'
#         IF h exists in seen:
#             Calculate end time
#             RETURN seen[h], s, attempts, elapsed time
#         ELSE:
#             Add s to seen with key h
#     RETURN None, None, max_attempts, elapsed time
#  END FUNCTION

def find_collision(bits,max_attempts):
    seen ={}

    for i in range(0,max_attempts):
        s = string.ascii_letters
        base = "".join(random.choices(s, k=10))
        hash= truncate_hash(base,bits)
        if hash in seen:
            # Calculate end time
            return 1
        else:
            seen= {"letter": base , "key":hash }
    return None,None, max_attempts, #elapsed time
