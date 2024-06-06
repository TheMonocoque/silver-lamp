from nacl.public import PrivateKey, SealedBox
from nacl.hash import sha256

#-- Example from loading b64 from vault
# from nacl.encoding import Base64Encoder
# savedkey = 'BASE64 PRIVATE KEY FROM VAULT'
# byte_skbob = Base64Encoder().decode(savedkey)
# skbob = PrivateKey(byte_skbob)
# pkbob = skbob.public_key
# print(f"PrivateKey: {skbob.encode(encoder=Base64Encoder).decode('utf-8')}")
# print(f"PublicKey : {pkbob.encode(encoder=Base64Encoder).decode('utf-8')}")

# Generate Bob's private key, as we've done in the Box example
skbob = PrivateKey.generate()
pkbob = skbob.public_key

# Alice wishes to send a encrypted message to Bob,
# but prefers the message to be untraceable
sealed_box = SealedBox(pkbob)

# This is Alice's message
message = b"Kill all kittens"
print(f"M(sha2): {sha256(message).decode()}")

# Encrypt the message, it will carry the ephemeral key public part
# to let Bob decrypt it
encrypted = sealed_box.encrypt(message)

unseal_box = SealedBox(skbob)
# decrypt the received message
plaintext = unseal_box.decrypt(encrypted)
print(f"D(sha2): {sha256(plaintext).decode()}")
print(plaintext.decode('utf-8'))

