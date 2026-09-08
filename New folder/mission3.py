import time
import hmac
import hashlib
import struct
import base64
import json
import urllib.request


def generate_totp(email):
    secret = (email + "HENNGECHALLENGE004").encode("ascii")

    counter = int(time.time()) // 30
    counter_bytes = struct.pack(">Q", counter)

    hmac_result = hmac.new(
        secret,
        counter_bytes,
        hashlib.sha512
    ).digest()

    offset = hmac_result[-1] & 0x0f

    binary_code = (
        ((hmac_result[offset] & 0x7f) << 24)
        | ((hmac_result[offset + 1] & 0xff) << 16)
        | ((hmac_result[offset + 2] & 0xff) << 8)
        | (hmac_result[offset + 3] & 0xff)
    )

    return str(binary_code % 10**10).zfill(10)


def main():
    email = "saransh.g2911@gmail.com"
    gist_url = "https://gist.github.com/SaranshGupta-sg/bc51dad423d68f5352d7a93adc03d8e2"

    totp = generate_totp(email)

    data = {
        "github_url": gist_url,
        "contact_email": email,
        "solution_language": "python"
    }

    json_data = json.dumps(data).encode("utf-8")

    credentials = f"{email}:{totp}".encode("utf-8")
    authorization = base64.b64encode(credentials).decode("ascii")

    request = urllib.request.Request(
        "https://api.challenge.hennge.com/challenges/backend-recursion/004",
        data=json_data,
        headers={
            "Authorization": f"Basic {authorization}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        print(response.status)
        print(response.read().decode())


if __name__ == "__main__":
    main()