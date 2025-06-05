from typing import Union

from sqlalchemy.future import select

from core.database import get_async_session
from core.database.sql_models.user.user import UserSqlModel, UserRoleID


class UserRepo:

    @classmethod
    async def create(cls, email: str, password_hash: str) -> 'UserDataModel':
        async with get_async_session() as session:
            new_user = UserSqlModel(
                email=email,
                password_hash=password_hash
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return UserDataModel.from_db_instance(new_user)

    @classmethod
    async def get_by_id(cls, user_id: int = None) -> Union['UserDataModel', None]:
        async with get_async_session() as session:
            user_in_session: UserSqlModel = await session.get(UserSqlModel, user_id)
            return UserDataModel.from_db_instance(user_in_session) if user_in_session is not None else None

    @classmethod
    async def get_by_email(cls, email: str) -> Union['UserDataModel', None]:
        async with get_async_session() as session:
            user_in_session: UserSqlModel = await session.scalars(select(UserSqlModel).where(UserSqlModel.email == email))
            user_in_session = user_in_session.first()
            # print(user_in_session)
            return UserDataModel.from_db_instance(user_in_session) if user_in_session is not None else None


class UserDataModel:
    def __init__(self, db_instance: UserSqlModel):
        self._db_instance = db_instance

    @property
    def id(self) -> int:
        return self._db_instance.id

    @classmethod
    def from_db_instance(cls, db_instance: UserSqlModel) -> 'UserDataModel':
        return cls(db_instance)

    @property
    def password_hash(self) -> str:
        return self._db_instance.password_hash

    @property
    def role(self) -> int:
        return self._db_instance.role
    
    # async def get_role_id(self) -> UserRoleID:
    #     async with get_async_session() as session:
    #         user_in_session: UserSqlModel = await session.get(UserSqlModel, self._db_instance.id)
    #         return user_in_session.role

    async def set_role_id(self, role_id: UserRoleID):
        async with get_async_session() as session:
            user_in_session: UserSqlModel = await session.get(UserSqlModel, self._db_instance.id)
            user_in_session.role = role_id
            await session.commit()
