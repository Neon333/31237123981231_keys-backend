import datetime
import uuid
from enum import IntEnum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ... import BaseModel
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Enum as PgEnum


class OrderStatusID(IntEnum):
    PENDING = 1
    PAYED = 2
    FAILED = 3


class OrderSqlModel(BaseModel):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    client_ip = Column(String(64), default=None, nullable=True)
    status = Column(PgEnum(OrderStatusID), default=OrderStatusID.PENDING)
    amount = Column(Integer)
    items = relationship('OrderItemSqlModel', cascade="all, delete-orphan")


class OrderItemSqlModel(BaseModel):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(UUID, ForeignKey('orders.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'))
    count = Column(Integer)

    game = relationship('GameSqlModel')
