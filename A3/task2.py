from nltk.corpus import words
from bcrypt import checkpw, hashpw
import time

def password_cracking():

    allwords = words.words()

    hashes = [
        b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq",
        b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.q2PW6mqALUl2/uFvV9OFNPmHGNPa6YC",
        b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.6B7jUcPdnqJz4tIUwKBu8lNMs5NdT9q",
        b"$2b$09$M9xNRFBDn0pUkPKIVCSBzuwNDDNTMWlvn7lezPr8IwVUsJbys3YZm",
        b"$2b$09$M9xNRFBDn0pUkPKIVCSBzuPD2bsU1q8yZPlgSdQXIBILSMCbdE4Im",
    ]
    for hash in hashes:
        start = time.time()
        for word in allwords:
            if checkpw(bytes(word, "utf-8"), hash):
                end = time.time()
                print(f"word: {word} time: {end-start}")
                break


password_cracking()
