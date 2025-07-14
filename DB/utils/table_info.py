import jwt
from datetime import datetime, timedelta, timezone

async def add_row(session, Model, **kwargs):
    db_token = Model(**kwargs)
    session.add(db_token)
    await session.commit()
    await session.refresh(db_token)
    return db_token

def fetch_time_interval(minutes, tzinfo=None):
    expire = (datetime.now(timezone.utc) + timedelta(minutes=minutes)).replace(
        tzinfo=tzinfo)  # Время протухания токена
    issued_at = datetime.now(timezone.utc).replace(tzinfo=tzinfo)
    return expire, issued_at

def create_token(payload, secret_key, algorithm):
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token