from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad


def eulers_totent(p, q):
    return (p - 1) * (q - 1)


def private_d(a, m):

    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

    g, x, _ = egcd(a, m)

    if g != 1:
        raise Exception("Modular inverse does not exist")
    else:
        return x % m


def decryption(encrypt, d, n):
    # Private Key (d,n)
    # m = c^d mod n
    message = (encrypt**d) % n
    return message


def encryption(m, e, n):
    # Public key = (e,n)
    # c = m^e % n
    if isinstance(m, str):
        m = int.from_bytes(m.encode("utf-8"), byteorder="big")
    return (m**e) % n


def Mallary_attack(n):
    # Mallory chooses c' = 1
    c_prime = 1
    print(f"Mallory modified ciphertext: {c_prime}")
    return c_prime


def derive_key(s):
    s_bytes = s.to_bytes((s.bit_length() + 7) // 8, byteorder="big")
    return SHA256.new(s_bytes).digest()


# --------------------
# Task 3(part 2): Malleability example - tampering with an encrypted amount
# TA Comment on Needing this
# -------------------


def malleability_amount_attack(e, n, d):
    print("\n--- Malleability Attack: Amount Tampering ---")

    # Alice wants to authorize a transfer of, say, 100 (cents)
    amount = 100
    c = encryption(amount, e, n)
    print(f"Original encrypted amount (100): {c}")

    # Mallory intercepts c and multiplies it by 2^e mod n
    # This works because RSA is multiplicatively homomorphic:
    # (m * k)^e = m^e * k^e mod n
    factor = 2
    factor_encrypted = (factor**e) % n
    c_prime = (c * factor_encrypted) % n
    print(f"Mallory's tampered ciphertext (c * 2^e mod n): {c_prime}")

    # Bank decrypts c' as usual, with no idea it was modified
    recovered_amount = decryption(c_prime, d, n)
    print(f"Bank decrypts tampered ciphertext to: {recovered_amount}")
    print(f"Expected doubled amount: {amount * factor}")
    print(f"Attack succeeded: {recovered_amount == amount * factor}")


# -------------------------------------------------------
# Task 3.(part 3): Signature malleability - forging s3 for m3 = m1 * m2
# Added this from the TA Comment
# -------------------------------------------------------


def sign(m, d, n):
    # Sign(m, d) = m^d mod n
    return (m**d) % n


def verify(m, s, e, n):
    # valid if s^e mod n == m
    return (s**e) % n == m


def signature_forgery_attack(d, e, n):
    print("\n--- Signature Malleability Attack ---")

    m1 = 12345
    m2 = 6789

    s1 = sign(m1, d, n)
    s2 = sign(m2, d, n)
    print(f"Signature on m1={m1}: {s1}")
    print(f"Signature on m2={m2}: {s2}")

    # Mallory, without knowing d, forges a signature on m3 = m1 * m2 mod n
    m3 = (m1 * m2) % n
    s3 = (s1 * s2) % n
    print(f"Forged m3 = m1*m2 mod n = {m3}")
    print(f"Forged signature s3 = s1*s2 mod n = {s3}")

    # Verify the forged signature using only the public key (e, n)
    valid = verify(m3, s3, e, n)
    print(f"Forged signature verifies as valid: {valid}")


def key_generation():
    e = 65537
    p = int(input("Input P for the Algo: "))
    q = int(input("Input Q for the Algo: "))
    message = input("Input Message: ")

    n = p * q

    phi_of_n = eulers_totent(p, q)
    d = private_d(e, phi_of_n)

    print(f"Public Key is: ({n},{e})")
    print(f"Private Key is: {d}")

    encrypt = encryption(message, e, n)
    print(f"Ecnrypted Message : {encrypt}")

    decrypt = decryption(encrypt, d, n)
    decrypted_bytes = decrypt.to_bytes((decrypt.bit_length() + 7) // 8, byteorder="big")
    message = decrypted_bytes.decode("utf-8")
    print(f"decrypted Message : {message}")

    # ------------------------------------------------------------------------------------------------------------
    print("\n--- Mallory Attack ---")

    # Mallory sends c' = 1 to Alice
    c_prime = Mallary_attack(n)

    # Alice decrypts c' using her private key
    s = decryption(c_prime, d, n)
    print(f"Alice decrypts modified ciphertext to: {s}")

    # Mallory already knows that s = 1
    mallory_s = 1

    # Both derive the same AES key
    alice_key = derive_key(s)
    mallory_key = derive_key(mallory_s)

    print(f"Alice key:   {alice_key.hex()}")
    print(f"Mallory key: {mallory_key.hex()}")
    print(f"Keys match: {alice_key == mallory_key}")

    iv = b"1234567890123456"

    cipher = AES.new(alice_key, AES.MODE_CBC, iv)
    c0 = cipher.encrypt(pad(b"Hi Bob!", AES.block_size))
    print(f"AES ciphertext: {c0.hex()}")

    # Mallory decrypts using the key she knows
    cipher = AES.new(mallory_key, AES.MODE_CBC, iv)
    recovered = unpad(cipher.decrypt(c0), AES.block_size)
    print(f"Mallory recovered message: {recovered.decode('utf-8')}")

    # ---------------------------------
    # Task 3.2 parts 2 and 3 ( TA Comment )
    # ---------------------------------
    malleability_amount_attack(e, n, d)
    signature_forgery_attack(d, e, n)


key_generation()
