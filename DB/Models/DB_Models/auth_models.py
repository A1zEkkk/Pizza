from DB.Models import Base

from datetime import datetime

from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String)

    login: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)

    #Связь с токенами
    access_tokens: Mapped[list["AccessToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    refresh_tokens: Mapped[list['RefreshToken']] = relationship(back_populates='user', cascade="all, delete-orphan")


class AccessToken(Base):
    __tablename__ = "access_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    #Время истечения действия токена
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    #Время выдачи токена
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    #Флаг ручного отзыва токена
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Определяет отношение "многие к одному" обратно к модели User.
    # 'back_populates' связывает эту сторону отношения с атрибутом 'access_tokens' в модели Users.
    user: Mapped[Users] = relationship(back_populates='access_tokens')  # для AccessToken

    def __repr__(self):
        return (
            f"<AccessToken(id={self.id}, user_id={self.user_id}, "
            f"expires_at={self.expires_at.strftime('%Y-%m-%d %H:%M:%S')}, "
            f"revoked={self.is_revoked})>"
        )


    #Метод проверки токена
    @property
    def is_expired(self) -> bool:
        return self.expires_at < datetime.now()


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)

    #Время истечения жизни рефреш токена
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    #Время выдачи рефреш токена
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    # Флаг для ручного отзыва.
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # JTI (JWT ID): Уникальный идентификатор из полезной нагрузки JWT.
    # Критически важен для чёрных списков токенов и реализации refresh-токенов "одноразового использования".
    jti: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    # Флаг 'used': Для стратегии refresh-токена "одноразового использования".
    # Когда refresh-токен используется для выдачи нового access-токена, этот флаг устанавливается в True,
    # и выдаётся *новый* refresh-токен. Это значительно повышает безопасность против атак повторного воспроизведения.
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Определяет отношение "многие к одному" обратно к модели User.
    user: Mapped[Users] = relationship(back_populates='refresh_tokens')

    def __repr__(self):
        return (
            f"<RefreshToken(id={self.id}, user_id={self.user_id}, "
            f"expires_at={self.expires_at.strftime('%Y-%m-%d %H:%M:%S')}, "  # Форматируем для более чистого вывода
            f"revoked={self.is_revoked}, used={self.used})>"
        )

    #Проверка токена
    @property
    def is_expired(self) -> bool:
        return self.expires_at < datetime.now()