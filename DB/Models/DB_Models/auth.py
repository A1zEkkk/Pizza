from DB.Models import Base

from datetime import datetime

from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String)

    login: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)

    refresh_tokens: Mapped[list['RefreshToken']] = relationship(
        back_populates='user',
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, login='{self.login}', role='{self.role}', password='{self.password}')>"

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE"),  # каскадное удаление на уровне БД
        nullable=False,
        index=True
    )

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    jti: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped[User] = relationship(back_populates='refresh_tokens')