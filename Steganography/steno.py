import numpy as np
from PIL import Image
import copy
from io import BytesIO
import struct, hashlib


# helpers
def seed_from_password(password):
    hash = hashlib.sha256(password.encode("utf-8")).digest()
    seed = hash[0 : 8]
    return int.from_bytes(seed, "big")

def capacity_bytes(height, width, channels=3):
    return (height * width * channels) // 8

def bytes_to_bits(data):
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_bytes(bits):
    if len(bits) % 8:
        bits = bits + [0] * (8 - len(bits) % 8)
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i : i + 8]:
            byte = (byte << 1) | b
        out.append(byte)
    return bytes(out)

def frame_payload(type, payload_bytes):
    magic = b"STEG"
    if type == "text":
        tbyte = b"\x00"
    else:
        tbyte = b"\x01"
    length = struct.pack(">I", len(payload_bytes))
    return magic + tbyte + length + payload_bytes


# task 1 embed
def embed(cover_path, out_path, type, payload_bytes, password):
    image = Image.open(cover_path).convert("RGB")
    arr = np.array(image)
    height = arr.shape[0]
    width = arr.shape[1]
    total_channels = height * width * arr.shape[2]

    framed = frame_payload(type, payload_bytes)
    bits = bytes_to_bits(framed)

    if len(bits) > total_channels:
        raise Exception("payload too large for this cover")

    seed = seed_from_password(password)
    perm = np.random.default_rng(seed).permutation(total_channels - 1)
    out = copy.deepcopy(arr)

    for i in range(len(bits)):
        channel_pos = perm[i]
        pixel = channel_pos // 3
        ch = channel_pos % 3
        y = pixel // width
        x = pixel % width

        out[y, x, ch] = (out[y, x, ch] & 0xFE) | bits[i]

    Image.fromarray(out).save(out_path)

# text payload
embed("apple_logo_cover.png", "stego_text.png", "text", b"this is a secret", "password")

# image payload
bio = BytesIO()
Image.open("laptop_secret.png").convert("RGBA").save(bio, "PNG")
image_bytes = bio.getvalue()
embed("apple_logo_cover.png", "stego_laptop.png", "image", image_bytes, "password")


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
        bits.append(arr[y, x, ch] & 1)


        if len(bits) == 72:
            header = bits_to_bytes(bits)
            if header[0 : 4] != b"STEG":
                return (None, None)

            type = "text" if header[4] == 0 else "image"
            length = int.from_bytes(header[5 : 9], "big")
            total_bits_needed = (9 + length) * 8
            header_seen = True

        if header_seen and len(bits) >= total_bits_needed:
            break
    payload_bytes = bits_to_bytes(bits[72 : 72 + length*8])
    if type == "text":
        return ("text", str(payload_bytes, "utf-8"))
    else:
        return ("image", payload_bytes)


print(extract("stego_text.png", "password"))
print(extract("stego_text.png", "wrong_password"))

# image
type, secret_image = extract("stego_laptop.png", "password")
Image.open(BytesIO(secret_image)).save("recovered_image.png")

# image: wrong password
print(extract("stego_laptop.png", "wrong_password"))
