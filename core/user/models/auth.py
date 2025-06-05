import datetime
from datetime import timezone
from typing import Union
from sqlalchemy.future import select
from core.database import get_async_session
from core.database.sql_models.user.auth import AuthTokenSqlModel


class AuthTokenRepo:

    @classmethod
    async def create(cls, user_id: int, value: str):
        async with get_async_session() as session:
            new_token = AuthTokenSqlModel(
                user_id=user_id,
                token=value,
                expiration_date=datetime.datetime.utcnow() + datetime.timedelta(days=30)
            )
            session.add(new_token)
            await session.commit()

    @classmethod
    async def get_by_value(cls, value: str) -> Union['AuthTokenModel', None]:
        async with get_async_session() as session:
            token_in_db = await session.scalars(
                select(AuthTokenSqlModel).where(AuthTokenSqlModel.token == value)
            )
            token = token_in_db.first()
            return AuthTokenModel.from_db_instance(token) if token else None


class AuthTokenModel:
    def __init__(self, db_instance: AuthTokenSqlModel):
        self._db_instance = db_instance

    @classmethod
    def from_db_instance(cls, db_instance: AuthTokenSqlModel):
        return cls(db_instance)

    @property
    def user_id(self) -> int:
        return self._db_instance.user_id

    @property
    def token(self) -> str:
        return self._db_instance.token

    @property
    def expiration_date(self) -> datetime.date:
        return self._db_instance.expiration_date

    @property
    def is_expired(self) -> bool:
        return datetime.datetime.utcnow() >= self.expiration_date

    async def delete(self):
        async with get_async_session() as session:
            token_in_session: AuthTokenSqlModel = await session.get(AuthTokenSqlModel, self._db_instance.id)
            await session.delete(token_in_session)
            await session.commit()
