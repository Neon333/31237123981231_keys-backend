from typing import Union

from .order_model import OrderModel, OrderRepo
from ..database.sql_models.order import OrderStatusID
from .dto import NewOrder as OrderDTO


class Order:
    def __init__(self, db_instance: OrderModel):
        self._db_instance: OrderModel = db_instance

    @classmethod
    async def create(cls, order: OrderDTO):
        new_order_db_instance = await OrderRepo.create(order)
        return cls.from_db_instance(new_order_db_instance)

    @classmethod
    async def get_by_id(cls, order_id: str) -> Union['Order', None]:
        order = await OrderRepo.get_by_id(order_id)
        return cls.from_db_instance(order) if order is not None else None

    @classmethod
    def from_db_instance(cls, db_instance: OrderModel) -> 'Order':
        return cls(db_instance)

    @property
    def id(self) -> str:
        return self._db_instance.id

    @property
    def amount(self) -> int:
        return self._db_instance.amount

    async def get_status(self) -> OrderStatusID:
        return await self._db_instance.get_status()

    async def set_status(self, new_status: OrderStatusID):
        await self._db_instance.set_status(new_status)

    async def fulfil_order(self) -> dict:
        return await self._db_instance.fulfil_order()

    async def get_items(self):
        return await self._db_instance.get_items()
