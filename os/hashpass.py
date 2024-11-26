import os
import hashlib

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    hashed = hashlib.sha512((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"

def check_password(stored_password, input_password):
    salt, hashed = stored_password.split('$')
    return hash_password(input_password, salt).split('$')[1] == hashed