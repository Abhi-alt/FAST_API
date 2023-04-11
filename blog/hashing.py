from passlib.context import CryptContext

crypt_cnxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def password_hash(password: str):
        return crypt_cnxt.hash(password)