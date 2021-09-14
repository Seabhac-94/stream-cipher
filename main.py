import random

class KeyStream:
    def __init__(self, key=1):
        self.next = key

    def rand(self):
        self.next = (1103515245*self.next + 12345) % 2**31
        return self.next

    def get_key_byte(self):
        return self.rand() % 256


def encrypt(key, message):
    return bytes([message[i] ^ key.get_key_byte() for i in range(len(message))])


# function to demonstrate bits lost in transmit
def transmit(cipher, likely):
    b = []
    for c in cipher:
        if random.randrange(0, likely) == 0:
            c = c ^ 2**random.randrange(0, 8)
        b.append(c)
    return bytes(b)


# used to demonstrate ability to modify message cross transmission
def modification(cipher):
    mod = [0]*len(cipher)
    mod[10] = ord(' ') ^ ord('1')
    mod[11] = ord(' ') ^ ord('0')
    mod[12] = ord('1') ^ ord('0')
    return bytes([mod[i] ^ cipher[i] for i in range(len(cipher))])


def get_key(message, cipher):
    return bytes([message[i] ^ cipher[i] for i in range(len(cipher))])


def crack(key_stream, cipher):
    length = min(len(key_stream), len(cipher))
    return bytes([key_stream[i] ^ cipher[i] for i in range(length)])


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