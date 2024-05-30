import hashlib

def HashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()