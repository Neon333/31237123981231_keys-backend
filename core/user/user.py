import bcrypt
from core.user.models.user import UserDataModel, UserRoleID, UserRepo


class User:
    def __init__(self, db_instance: UserDataModel):
        self._db_instance = db_instance

    @property
    def id(self) -> int:
        return self._db_instance.id

    @property
    def password_hash(self) -> str:
        return self._db_instance.password_hash

    @property
    def role(self) -> int:
        return self._db_instance.role

    @classmethod
    def from_db_instance(cls, db_instance: UserDataModel) -> 'User':
        return cls(db_instance)

    @classmethod
    async def create(cls, email: str, password: str):
        hashed_password = cls._hash_password(password)
        return cls.from_db_instance(await UserRepo.create(email, hashed_password))

    @classmethod
    def _hash_password(cls, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    @classmethod
    async def get_by_id(cls, user_id: int) -> 'User':
        user = await UserRepo.get_by_id(user_id)
        return cls.from_db_instance(user) if user is not None else None

    @classmethod
    async def get_by_email(cls, email: str) -> 'User':
        user = await UserRepo.get_by_email(email)
        return cls.from_db_instance(user) if user is not None else None

    async def set_role(self, role_id: UserRoleID):
        await self._db_instance.set_role_id(role_id)