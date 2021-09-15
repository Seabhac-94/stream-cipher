import random
from main import KeyStream, encrypt, transmit, modification, get_key, crack, brute_force

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


# Using a brute force on stream cipher

# This is Alice
secret_key = random.randrange(0, 2**20)
print(secret_key)
key = KeyStream(secret_key)
header = "Message: "
message = header + "My secret message to Bob"
message = message.encode()
print(message)
cipher = encrypt(key, message)
print(cipher)

# This is Bob
key = KeyStream(secret_key)
message = encrypt(key, cipher)
print(message)

# This is Eve
bf_key = brute_force(header.encode(), cipher)
print("Brute force key: ", bf_key)
key = KeyStream(bf_key)
message = encrypt(key, cipher)
print(message)
