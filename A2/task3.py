from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

def eulers_totent(p,q):
    return(p-1)*(q-1)


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


def decryption(encrypt,d,n):
   #Private Key (d,n)
   # m = c^d mod n
   message = (encrypt**d) % n


   return message


def encryption(m, e, n):
    # Public key =(e,n)
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


def key_generation():
    e = 65537
    p =int(input("Input P for the Algo: "))
    q = int(input("Input Q for the Algo: "))
    message = input("Input Message: ")

    n = p * q

    phi_of_n = eulers_totent(p,q)
    d =private_d(e,phi_of_n)

    print(f"Public Key is: ({n},{e})")
    print(f"Private Key is: {d}")

    encrypt= encryption(message,e,n)
    print(f"Ecnrypted Message : {encrypt}")

    decrypt= decryption(encrypt,d,n)
    decrypted_bytes = decrypt.to_bytes((decrypt.bit_length() + 7) // 8,byteorder="big")
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



print(key_generation())
