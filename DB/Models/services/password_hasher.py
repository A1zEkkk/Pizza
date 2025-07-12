from passlib.context import CryptContext


class PasswordService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        print(f"Хеширование пароля: {password}")
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        print(f"Верификация пароля: {plain_password} его хэш: {hashed_password}")
        return self.pwd_context.verify(plain_password, hashed_password)
