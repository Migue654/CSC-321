from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = get_random_bytes(16)
iv = get_random_bytes(16)


def CBC_encrypt(encryption, key=key, iv=iv):
    prev = iv
    cipher = AES.new(key, AES.MODE_ECB)

    if len(encryption) % 16 != 0:
        # this is the padding if it's not perfectly divisible by 16,
        # I will add the byte version of " " for the remaining bytes to fill in the rest
        encryption += b" " * (16 - len(encryption) % 16)

    # once padded  i initialize necessary variables
    done = len(encryption)
    progress = 16
    result = b""
    mixed = bytearray(16)
    while done >= progress:
        chunk = encryption[progress - 16 : progress]

        # this is what makes the CBC different from ECB, so it XOR's
        for i in range(16):
            mixed[i] = chunk[i] ^ prev[i]

            # continue the "CBC" standard thingy by making the next "prev" to XOR with the block we JUST encrypted
        prev = cipher.encrypt(bytes(mixed))
        result += prev
        mixed = bytearray(16)

        progress += 16

    return result


PREPEND = "userid=456;userdata="
APPEND = ";session-id=31337"

def submit(user_str):
    # Encode characters the user is not supposed to inject directly.
    safe_user_str = user_str.replace(";", "%3B").replace("=", "%3D")
    plaintext = PREPEND + safe_user_str + APPEND

    # Pad the appended plaintext using PKCS#7 padding
    # "utf-8" basically tells python that it is/going to be turned into bytes
    padded_plaintext = pad(plaintext.encode("utf-8"), AES.block_size)

    # Use my CBC encryption code instead of the library's CBC mode.
    return CBC_encrypt(padded_plaintext)


def verify(ciphertext):
    # Get the cipher to CBC mode that I will use later
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Using the CBC Library to decrypt the encrypted text
    decrypted = cipher.decrypt(ciphertext)


    plaintext = unpad(decrypted, AES.block_size).decode("utf-8", errors="ignore")
    return ";admin=true;" in plaintext


def cbc_bitflip_attack():
    # PREPEND is 20 bytes long, so 12 filler bytes push our chosen text

    # to the start of the next block.
    attack_input = "A" * 12 + "XadminYtrueZAAAA"
    ciphertext = bytearray(submit(attack_input))

    target_block = b"XadminYtrueZAAAA"
    desired_block = b";admin=true;AAAA"
    block_to_modify = 16

    for i in range(len(target_block)):
        ciphertext[block_to_modify + i] ^= target_block[i] ^ desired_block[i]

    return bytes(ciphertext)


if __name__ == "__main__":
    user_str = input("Enter the arbitrary string thingy: ")
    ciphertext = submit(user_str)
    print("Encrypted string:", ciphertext)
    print("verify(submit(user input)):", verify(ciphertext))

    forged_ciphertext = cbc_bitflip_attack()
    print("verify(modified ciphertext):", verify(forged_ciphertext))
