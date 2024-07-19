def rc4(message, key):
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
    return ''.join(out)

if __name__ == "__main__":
    plaintext = "hello i am here"  # Example plaintext
    key = "12345"                 # Example key

    ciphertext = rc4(plaintext, key)
    print(f"Ciphertext: {ciphertext}")

    decrypted_text = rc4(ciphertext, key)
    print(f"Decrypted text: {decrypted_text}")

