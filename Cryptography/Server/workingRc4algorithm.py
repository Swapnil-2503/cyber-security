

def read_key_from_file(file_path):
    with open(file_path, 'r') as file:
        key = file.read().strip()
    return key

def rc4(key, message):
    global string_out
    S = list(range(256))
    j = 0
    out = []

    # Key Scheduling Algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudorandom Generation Algorithm (PRGA)
    i = j = 0
    for char in message:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(chr(ord(char) ^ K))
    strReturn = ''.join(out)
    return strReturn

# Example usage
key = read_key_from_file('rc4-key.txt')
message = "Hello, World!"

# Encrypt the message
encrypted_message = rc4(key, message)
print("Encrypted Message:", encrypted_message) ## send to client

# Decrypt the message (since RC4 is symmetric, we use the same function)
decrypted_message = rc4(key, encrypted_message)  ## decrypt from received message
print("Decrypted Message:", decrypted_message)
