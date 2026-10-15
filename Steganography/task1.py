from Crypto.Hash import SHA256
import numpy as np
from PIL import Image

from itertools import permutations



#helpers

def seed_from_password(password):
    hash = SHA256(bytes(password, "utf-8"))
    return hash[0 : 8]


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
    magic = "STEG"
    if type == "text":
        tbyte = 0x00
    else:
        tbyte = 0x01


    length = len(payload_bytes).to_bytes(4)

    return magic + tbyte + length + payload_bytes


#task 1 embed
#not done yet
def embed(cover_path, out_path, type, payload_bytes, password):
    image = Image.open(cover_path).convert("RGB")
    arr = np.array(image).shape
    total_channels = arr[0] * arr[1] * arr[2]

    # framed = frame_payload(type, payload_bytes)
    # bits = bytes_to_bits(framed)

    # if len(bits) > total_channels:
    #     #raise error
    #     return "error"

    list = [range(0, total_channels)]

    perm = permutations[list[0]]


embed("apple_logo_cover.png", None, None, None, None)
