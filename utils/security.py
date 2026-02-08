import random
import string
import hashlib

def generate_account_number():
    return "DZ" + "".join(random.choices(string.digits, k=10))

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash
