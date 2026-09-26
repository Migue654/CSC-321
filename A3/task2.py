from nltk.corpus import words
from bcrypt import checkpw, hashpw
import time

#wordfunction = words.words()

def password_cracking():
    #with open("shadow.pdf", "rb") as file:
     #   data = file.read()
      #  print(words.words(data))


      allwords = words.words()

      start = time.time()

      for word in allwords:
            if checkpw(bytes(word, "utf-8"), b'$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq'):
                  end = time.time()
                  print(f"true, time: {end-start}")






password_cracking()
