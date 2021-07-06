from hashlib import sha512
from re import compile, findall, match

hash = lambda x: sha512(str(x).encode("utf-8")).hexdigest()


def encrypt_password(password: str) -> str:
    """Returns Password Hashed with sha512 algo"""
    return hash(password)


def check_password(stored: str, entered: str) -> bool:
    """Verfies Hashed Password with password in db"""
    return stored == entered


class Validator(object):
    name_pattern = compile("[A-Za-z]")
    id_pattern = compile("[a-z0-9@_$-]")
    pwd_pattern = compile("[A-za-z0-9@_]")

    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate name passed in to store"""
        if findall(Validator.name_pattern, name) == list(name):
            return True
        else:
            return False
    
    @staticmethod
    def validate_id(uid: str) -> bool:
        """Validate user id"""
        if not findall("[a-z]", uid):
            return False
        elif not findall("[0-9]", uid):
            return False
        elif not findall("[@_$-]", uid):
            return False
        elif findall(Validator.id_pattern, uid) != list(uid):
            return False
        return True
    
    @staticmethod
    def validate_pwd(pwd: str) -> bool:
        """Validate password passed"""
        if not findall("[A-Z]", pwd):
            return False
        elif not findall("[a-z]", pwd):
            return False
        elif not findall("[0-9]", pwd):
            return False
        elif not findall("[@_]", pwd):
            return False
        elif findall(Validator.pwd_pattern, pwd) != list(pwd):
            return False
        return True


if __name__ == "__main__":
    print(Validator.validate_name("Aniruddh")) # True
    print(Validator.validate_id("aniruddh@07")) # True
    print(Validator.validate_pwd("Aniruddh@07")) # True