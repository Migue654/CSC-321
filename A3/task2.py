from nltk.corpus import words
from bcrypt import checkpw, hashpw
import time

def password_cracking():

    allwords = words.words()

    hashes = [

      b"$2b$13$6ypcazOOkUT/a7EwMuIjH.qbdqmHPDAC9B5c37RT9gEw18BX6FOay"]
    for hash in hashes:
        start = time.time()
        for word in allwords:
            if checkpw(bytes(word, "utf-8"), hash):
                end = time.time()
                print(f"word: {word} time: {end-start}")
                break


password_cracking()
