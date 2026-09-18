from Crypto.Hash import SHA256

#Diffie- Hellman Key Exchange
def calculation(base,x,mod):
    # y = (base ** x) % mod

    # print (f"({base} ^ {x}) % {mod}")
    # print(f"{y}")
    return  (base ** x) % mod



def diffie_Hellman_key_exhange() :

    bobs_num = int(input("Enter Bobs Secret: "))
    alice_num = int(input("Enter Alice's Secret: "))

    mod = 37
    base = 5

    calc_value_bob = calculation(base,bobs_num,mod)
    print (f"this is bobs key : {calc_value_bob}" )

    calc_value_alice = calculation(base,alice_num,mod)
    print(f"this is alices key: {calc_value_alice}" )

    bobs_shared = calculation(calc_value_alice,bobs_num,mod)
    print(f"this is bobs shared calc: {bobs_shared}" )

    alice_shared = calculation(calc_value_bob,alice_num,mod)
    print(f"this is alices shared calc: {alice_shared}" )

    sha=SHA256.new(str(alice_shared).encode())



    if (alice_shared == bobs_shared):

        return 1

    # return bobs_shared

print(diffie_Hellman_key_exhange())
