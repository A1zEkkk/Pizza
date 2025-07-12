import asyncio
from DB.Models.repository.repository import AuthDBService

async def main():
    service = AuthDBService()

    # Попробуем создать нового пользователя
    print("\n📌 Создание нового пользователя:")
    result_create = await service.create_user(
        login="test_user",
        password="secure_password",
        role="user"
    )
    print(result_create)

    # Пробуем войти с тем же логином и паролем
    print("\n📌 Аутентификация пользователя:")
    result_auth = await service.authenticate_user(
        login="test_user",
        password="secure_password"
    )
    print(result_auth)

if __name__ == "__main__":
    asyncio.run(main())
