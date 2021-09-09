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
