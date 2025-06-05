from enum import IntEnum
from ... import BaseModel
from sqlalchemy import Column, Integer, String, Enum as PgEnum


class UserRoleID(IntEnum):
    USER = 1
    ADMIN = 2


class UserSqlModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(64))
    role = Column(PgEnum(UserRoleID), default=UserRoleID.USER)
