from jose import jwt, JWTError

secret = "601b229579585b4d011cd74e37714898e7a53a55c5d2fb40530769b2b5c7a2bc43716194ee3c41223a1837c5edb199090653930a8e8a2301eb0a49a39748fcb1"
# secret = bytearray.fromhex(secret)
print(len(secret))

payload = {"sub": "some@email.com", "username": "obj111212", "role": "user"}

token = jwt.encode(payload, secret, algorithm=jwt.ALGORITHMS.HS512)  # type: ignore

print(token)

try:
    decoded = jwt.decode(token, secret, algorithms=[jwt.ALGORITHMS.HS512])  # type: ignore
    print(decoded)
except JWTError as err:
    print("ERR", err)
