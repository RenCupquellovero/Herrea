import bcrypt

pw = input("Password: ").encode()
hashed = bcrypt.hashpw(pw, bcrypt.gensalt()).decode()
print("\nBcrypt hash:")
print(hashed)
