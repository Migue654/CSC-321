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
   #decrypted_bytes = message.to_bytes((message.bit_length() + 7) // 8,byteorder="big")
   #message = decrypted_bytes.decode("utf-8")

   return message


def encryption(m, e, n):
    # Public key =(e,n)
    # c = m^e % n

    if isinstance(m, str):
        m = int.from_bytes(m.encode("utf-8"), byteorder="big")

    return (m**e) % n


def Mallary_attack(c, e, n, d):
    x = 3

    r_encrypted = encryption(x, e, n)

    c_prime = (c * r_encrypted) % n

    s_prime = decryption(c_prime, d, n)

    print(f"Mallory modified ciphertext: {c_prime}")
    print(f"Alice decrypts modified ciphertext to: {s_prime}")


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

    print("Mallary Chooses 3 as her number to attack ")
    Mallary_attack(encrypt, e, n, d)


print(key_generation())
print("\n\n\n  --------------------------------Mallary Attack Starts here----------------------------------------------")
