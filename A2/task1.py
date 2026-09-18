from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

#Diffie- Hellman Key Exchange
def calculation(base,x,mod):
    # y = (base ** x) % mod

    # print (f"({base} ^ {x}) % {mod}")
    # print(f"{y}")
    return  (base ** x) % mod

def create_key(shared_secret):
    sha = SHA256.new(str(shared_secret).encode())
    return sha.digest()[:16]


def encrypt(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(message, AES.block_size))


def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)


iv =b'1234567890123456'
def diffie_Hellman_key_exhange() :

    bobs_num = int(input("Enter Bobs Secret: "))
    bobs_mes = input("Enter Message: ").encode()


    alice_num = int(input("Enter Alice's Secret: "))
    alice_mess = input("Enter Alice's Message: ").encode()
    mod = 0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371

    base = 0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5
    calc_value_bob = calculation(base,bobs_num,mod)
    print (f"this is bobs key : {calc_value_bob}" )

    calc_value_alice = calculation(base,alice_num,mod)
    print(f"this is alices key: {calc_value_alice}" )

    bobs_shared = calculation(calc_value_alice,bobs_num,mod)
    print(f"this is bobs shared calc: {bobs_shared}" )

    alice_shared = calculation(calc_value_bob,alice_num,mod)
    print(f"this is alices shared calc: {alice_shared}" )




    if (alice_shared == bobs_shared):
        print("Keys matched ")
        key = create_key(alice_shared)
        print(f"AES Key : {key.hex()}")

        # Alice to Bob
        ciphertext = encrypt(bobs_mes, key, iv)

        print(f"Bob sends: {bobs_mes.decode()}")
        print(f"Ciphertext: {ciphertext.hex()}")

        decrypted1 = decrypt(ciphertext, key, iv)

        print(f"Alice decrypts: {decrypted1.decode()}")


        # Bob to Alice
        ciphertext2 = encrypt(alice_mess, key, iv)

        print(f"Alice sends: {alice_mess.decode()}")
        print(f"Ciphertext: {ciphertext2.hex()}")

        decrypted2 = decrypt(ciphertext2, key, iv)

        print(f"Bob decrypts: {decrypted2.decode()}")

    else:
        print("Key does not match")



print(diffie_Hellman_key_exhange())
