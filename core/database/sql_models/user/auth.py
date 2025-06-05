from ... import BaseModel
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey


class AuthTokenSqlModel(BaseModel):
    __tablename__ = 'auth_tokens'

    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String(128), primary_key=True)
    expiration_date = Column(DateTime)
