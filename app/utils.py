from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(pwd: str):
    return pwd_context.hash(pwd)

def verify_password(current_password, stored_password) -> bool:
    return pwd_context.verify(current_password, stored_password)