from lib.encryption.fernet import FernetCipher

if __name__ == "__main__":
    cipher = FernetCipher()
    cipher.generate_key()