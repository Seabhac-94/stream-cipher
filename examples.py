import os
from main import KeyStream, encrypt, transmit, modification, get_key, crack

key = KeyStream(10)
# for i in range(10):
#     print(key.get_key_byte())

# encrypt message
message = "Hello, World! This is a test for demonstration purposes.".encode()
cipher = encrypt(key, message)
print(message)
print(cipher)

# calling transmit to demonstrate bits lost in transmit
cipher = transmit(cipher, 5)

# decrypt message using KeyStream
key = KeyStream(10)
message = encrypt(key, cipher)
print(message)

# code to demonstrate ability to modify message cross transmission:

# this is alice
key = KeyStream(10)
message = "Send Bob:   10$".encode()
print(message)
cipher = encrypt(key, message)
print(cipher)

# This is bob
cipher = modification(cipher)

# This is the Bank
key = KeyStream(10)
message = encrypt(key, cipher)
print(message)


# demonstrating the issue of re-using keys

# Eve gives Alice 'fake' message
eves_message = "This is the most important secret etc.".encode()

# Alice unknowingly sends Bob 'fake' message
key = KeyStream(10)
message = eves_message
print(message)
cipher = encrypt(key,message)
print(cipher)

# Eve intercepts
eves_key_stream = get_key(eves_message, cipher)

# Bob receives message
key = KeyStream(10)
message = encrypt(key, cipher)
print(message)

# Alice sends another message
message = "Another message sent to Bob".encode()
key = KeyStream(10)
cipher = encrypt(key, message)
print(cipher)

# Bob receives
key = KeyStream(10)
message = encrypt(key, cipher)
print(message)

# Eve intercepts message
print("Eve decrypting message")
print(crack(eves_key_stream, cipher))