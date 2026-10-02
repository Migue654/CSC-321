from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# key that I will use for ECB mode
key = get_random_bytes(16)

# opens the file that i want encrypt and will be read in binary
file = open("mustang.bmp", "rb")
encryption = original = None
result = b""
original = file.read()

# preserve the plaintext BMP header and only encrypt the rest
header = original[:54]
encryption = original[54:]


def ECB_encrypt(encryption, key=key):
    result = b""

    # Kind of a configuration that whatever encryption I do with "ciper" will be in the ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    if len(encryption) % 16 != 0:
        # this is the padding if it's not perfectly divisible by 16, I will add the by version of " " for the remaining bytes
        encryption += b" " * (16 - len(encryption) % 16)

    ## once padded then we will read the file in chunks of 16 bytes and encrypt through the while loop
    done = len(encryption)
    progress = 16
    # will encrypt the file 16 bytes at a time until the whole things is done
    while done >= progress:
        chunk = encryption[progress - 16 : progress]
        result += cipher.encrypt(chunk)
        progress += 16

    return result

iv = get_random_bytes(16)
def CBC_encrypt(encryption, key=key ,iv=iv ):
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

        # i guess it needs the header at the front so it can later decrypt the file
    return result


ecb_cipher = ECB_encrypt(encryption)
cbc_cipher = CBC_encrypt(encryption)

with open("cp-logo-ecb.bmp", "wb") as file:
    file.write(header + ecb_cipher)

with open("cp-logo-cbc.bmp", "wb") as file:
    file.write(header + cbc_cipher)
