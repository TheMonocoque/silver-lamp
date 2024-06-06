#!/usr/bin/env python
# Example notes from online

from nacl.public import PrivateKey, Box
from nacl.hash import sha256
from nacl.encoding import Base64Encoder

# Generate Bob's private key, which must be kept secret
skbob = PrivateKey.generate()

# Create key into saveable string that can be stored in vault
b64skbob = skbob.encode(encoder=Base64Encoder)
rtnskbob = Base64Encoder.decode(b64skbob)
skbob = PrivateKey(rtnskbob)
print(f"RAW   : {skbob}")
print(f"BASE64: {b64skbob}")
print(f"DECODE: {rtnskbob}")
print("SHA2  : %s" % sha256(rtnskbob).decode('utf-8'))

# Bob's public key can be given to anyone wishing to send
#   Bob an encrypted message
pkbob = skbob.public_key

# Alice does the same and then Alice and Bob exchange public keys
skalice = PrivateKey.generate()
pkalice = skalice.public_key

# Bob wishes to send Alice an encrypted message so Bob must make a Box with
#   his private key and Alice's public key
bob_box = Box(skbob, pkalice)

# This is our message to send, it must be a bytestring as Box will treat it
#   as just a binary blob of data.
message = b"Kill all humans, robots unite"
print(f"MESSAGE-SHA  : {sha256(message).decode()}")

# Encrypt our message, it will be exactly 40 bytes longer than the
#   original message as it stores authentication information and the
#   nonce alongside it.
encrypted = bob_box.encrypt(message)

# Alice creates a second box with her private key to decrypt the message
alice_box = Box(skalice, pkbob)

# Decrypt our message, an exception will be raised if the encryption was
#   tampered with or there was otherwise an error.
plaintext = alice_box.decrypt(encrypted)
print(f"DECRYPTED-SHA: {sha256(plaintext).decode()}")
print(plaintext.decode('utf-8'))
