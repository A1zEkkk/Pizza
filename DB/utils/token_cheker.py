from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone


async def token_checker(token: str, session: AsyncSession, model) -> bool:
    """
    Проверяет, валиден ли токен
    """
    stmt = select(model).where(model.token == token)
    result = await session.execute(stmt)
    db_token = result.scalar_one_or_none()

    if db_token is None:
        return False

    if db_token.is_revoked:
        return False

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    return db_token.expires_at > now


