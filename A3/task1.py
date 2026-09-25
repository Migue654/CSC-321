from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
import string
import time

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

    return hashed.hexdigest()


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
    for (c1,c2) in zip(s1,s2):
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
    start_time = time.perf_counter()

    for i in range(0,max_attempts):
        s = string.ascii_letters
        base = "".join(random.choices(s, k=10))
        hash_string = sha256_hash(base)
        hash_value = truncate_hash(hash_string, bits)
        if hash_value in seen:
            # Calculate end time
            end_time = time.perf_counter()
            elapsed_time = end_time-start_time
            return seen[hash_value],s,i,elapsed_time
        else:
            seen[hash_value] = base

    end_time = time.perf_counter()
    elapsed_time = end_time-start_time
    return None,None, max_attempts, elapsed_time

# task_1a():
#  FUNCTION task_1a():
#     Print "Task 1a: SHA256 hashes of arbitrary inputs"
#     FOR each input in ["Hello, World!", "Python", "Cryptography"]:
#         Calculate SHA256 hash of input
#         Print input and its hash
#  END FUNCTION

def task_1a():
    print("Task1a: SHA256 Hashes of arbitrary inputs")

    for i in ["Hello, World!","Python", "Cryptography"]:
        byte_string=i.encode()
        sha = sha256_hash(i)
        print (i,sha)


# task_1b():
#  FUNCTION task_1b():
#     Print "Task 1b: Strings with Hamming distance of 1"
#     FOR i from 1 to 3:
#         Find two strings s1, s2 with Hamming distance 1
#         Calculate SHA256 hashes h1, h2 of s1, s2
#         Print s1, s2, h1, h2
#  END FUNCTION

def task_1b():
    print("Task 1b: Strings with Hamming Distance of 1")
    for i in range(3):
       st1 , st2 = finding_hamming_distance_1()
       h1 = sha256_hash(st1)
       h2= sha256_hash(st2)
       print (f"{st1} ->  {h1} \n {st2} -> {h2}")


# task_1c():
#  FUNCTION task_1c():
#     Print "Task 1c: Finding collisions for truncated hashes"
#     Initialize empty lists for bits, time, and inputs
#     FOR bits from 8 to 50, step 2:
#         Find collision for 'bits' number of bits
#         IF collision found:
#             Add result to table
#             Append bits, time, and inputs to respective lists
#         ELSE:
#             Print timeout message
#     Print results table
#     Plot graphs:
#         1. Digest Size vs Collision Time
#         2. Digest Size vs Number of Inputs
#     Save graphs as 'collision_analysis.png'
#  END FUNCTION

def task_1c():
    print("Task 1c: Finding collisions for truncated hashes")
    bits=[]
    time=[]
    inputs=[]
    for i in range(8, 50, 2):
        result = find_collision(i, 1000000)


        if result[0] is not None:
            base1, base2, num_inputs, elapsed_time = result
            bits.append(i)
            time.append(elapsed_time)
            inputs.append(num_inputs)

            print(i, base1, base2, num_inputs, elapsed_time)

        else:
            print(f"Timeout for {i} bits")
    print(bits,time,inputs)

def task1_main():
 task_1a()
 task_1b()
 task_1c()

print(task1_main())
