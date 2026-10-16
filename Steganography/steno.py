from Crypto.Hash import SHA256
import numpy as np
from PIL import Image
import copy


# helpers

def seed_from_password(password):
    hash = SHA256.new(bytes(password, "utf-8"))
    seed = hash.digest()[0 : 64]
    return int.from_bytes(seed, "big")


def capacity_bytes(height, width, channels=3):
    return (height * width * channels) // 8

def bytes_to_bits(data):
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

# not sure if completely right
def bits_to_bytes(bits):
    padding_needed = len(bits) % 8
    if padding_needed != 0:
        for i in range (0, padding_needed):
            bits.append(0)
    out = []
    byte = []
    for i in range(0, len(bits), 8):
        group = bits[i : i + 8]
        out.append(group.reverse())

    return out


def frame_payload(type, payload_bytes):
    magic = b"STEG"
    if type == "text":
        tbyte = 0x00
    else:
        tbyte = 0x01


    length = len(payload_bytes).to_bytes(4)

    return magic + bytes(tbyte) + length + payload_bytes


# task 1 embed
# not done yet
def embed(cover_path, out_path, type, payload_bytes, password):
    image = Image.open(cover_path).convert("RGB")
    arr = np.array(image)
    height = arr.shape[0]
    width = arr.shape[1]
    total_channels = height * width * arr.shape[2]

    framed = frame_payload(type, payload_bytes)
    bits = bytes_to_bits(framed)

    if len(bits) > total_channels:
        # raise error
        return "error"

    seed = seed_from_password(password)

    perm = np.random.default_rng(seed).permutation(total_channels - 1)

    out = copy.deepcopy(arr)

    for i in range(len(bits)):
        channel_pos = perm[i]
        pixel = channel_pos // 3
        ch = channel_pos % 3
        y = pixel // width
        x = pixel % width

        old_y = out[0]
        old_x = out[1]
        old_ch = out[2]

        # out[y, x, ch] = (  (out[0] | out[1] | out[2]) & 0xFE) | bits[i]
        # out[0] = ((old_y | old_x | old_ch) & 0xFE) | bits[i]
        out[0] = (old_y & 0xFE) | bits[i]
        out[1] = (old_x & 0xFE) | bits[i]
        out[2] = (old_ch & 0xFE) | bits[i]

        print(out)

    Image.fromarray(out).save(out_path)


#embed("apple_logo_cover.png", "stego_text.png", "text", b"this is a secret", "password")



def extract(stego_path, password):
    image = Image.open(stego_path).convert("RGB")
    arr = np.array(image)
    height = arr.shape[0]
    width = arr.shape[1]
    channels = arr.shape[2]
    total_channels = height * width * channels

    seed = seed_from_password(password)

    perm = np.random.default_rng(seed).permutation(total_channels - 1)

    bits = []
    header_seen = False
    for i in range(total_channels):
        channel_pos = perm[i]
        pixel = channel_pos // 3
        ch = channel_pos % 3
        y = pixel // width
        x = pixel % width
        bits.append((y | x | ch) & 1)

        if len(bits) == 72:
            header = bits_to_bytes(bits)
            if header[0 : 4] != "STEG":
                return (None, None)

        type = "text" if header[4] == 0 else "image"
        length = header[5 : 10]
        total_bits_needed = (9 + length) * 8
        header_seen = True

        if header_seen and len(bits) >= total_bits_needed:
            break
    payload_bytes = bits_to_bytes(bits[72 : 72 + length*8])
    if type == "text":
        return ("text", str(payload_bytes, "utf-8"))
    else:
        return ("image", payload_bytes)


extract("stego_text.png", "password")
