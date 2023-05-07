import secrets

# Generate a random 32-byte key
key = secrets.token_hex(32)

# Print the key
print(key)