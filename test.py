import asyncio
import asyncpg
import platform
import logging # Добавляем импорт модуля logging

# --- Настройка логирования asyncpg ---
# Получаем логгер для asyncpg
asyncpg_logger = logging.getLogger('asyncpg')
# Устанавливаем уровень логирования на DEBUG для максимальной детализации
asyncpg_logger.setLevel(logging.DEBUG)
# Создаем обработчик для вывода логов в консоль
handler = logging.StreamHandler()
# Задаем формат вывода логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Добавляем обработчик к логгеру asyncpg
asyncpg_logger.addHandler(handler)
# ------------------------------------

# --- Ваш существующий код test_db_connection.py или main.py начинается здесь ---

# Если это test_db_connection.py:
# if platform.system() == "Windows":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_connection():
    """
    Попытка прямого подключения к PostgreSQL с использованием asyncpg.
    """
    conn = None
    try:
        print("Попытка подключения к базе данных...")
        await asyncio.sleep(1) # Задержка в 1 секунду

        conn = await asyncpg.connect(
            user='postgres',
            password='postgres',
            host='127.0.0.1',
            port=5432,
            database='Pizza'
        )
        print("Подключение к базе данных успешно установлено!")

        result = await conn.fetchval("SELECT 1 + 1;")
        print(f"Результат простого запроса (1+1): {result}")

    except asyncpg.exceptions.PostgresError as e:
        print(f"Ошибка PostgreSQL: {e}")
    except ConnectionRefusedError as e:
        print(f"Ошибка подключения: Соединение отклонено. Возможно, БД не запущена или порт неверный. Детали: {e}")
    except OSError as e:
        print(f"Ошибка ОС (WinError 64?): Проблема с сетевым именем. Детали: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    finally:
        if conn:
            print("Закрытие соединения с базой данных.")
            await conn.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
