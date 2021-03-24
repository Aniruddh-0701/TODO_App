from hashlib import sha512

hash = lambda x: sha512(str(x).encode("utf-8")).hexdigest()


def encrypt_password(password):
    return hash(password)


def check_password(stored, entered):
    return stored == entered
