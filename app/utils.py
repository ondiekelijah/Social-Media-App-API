from passlib.context import CryptContext

# tell passlib what hashing algorithm to use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)