from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from ..database import get_async_session
from ..database.sql_models import SteamKeySqlModel, GameSqlModel
from ..database.sql_models.order import OrderSqlModel, OrderItemSqlModel, OrderStatusID
from .dto import NewOrder


class OrderModelException(Exception):
    pass


class OrderAlreadyCompleted(OrderModelException):
    pass


class OrderNotCompleted(OrderModelException):
    pass


class OrderRepo:

    @classmethod
    async def create(cls, order: NewOrder):
        async with get_async_session() as session:
            games_from_order = {
                game.id: game
                for game in
                (await session.execute(select(GameSqlModel).where(GameSqlModel.id.in_([i.game_id for i in order.items])))).scalars()
            }
            new_order = OrderSqlModel(
                client_ip=order.client_ip,
                items=[
                    OrderItemSqlModel(game_id=item.game_id, count=item.count)
                    for item in order.items
                ],
                amount=sum([games_from_order[item.game_id].current_price * item.count for item in order.items]),
                # status=OrderStatusID.FAILED
            )
            session.add(new_order)
            await session.commit()
            await session.refresh(new_order)

            return OrderModel.from_db_instance(new_order)

    @classmethod
    async def get_by_id(cls, order_id: str) -> Union['OrderModel', None]:
        async with get_async_session() as session:
            query = select(OrderSqlModel).options(joinedload(OrderSqlModel.items)).filter(OrderSqlModel.id == order_id)
            query_result = await session.execute(query)
            order = query_result.unique().scalar()
            return None if order is None else OrderModel.from_db_instance(order)


class OrderModel:
    def __init__(self, db_instance: OrderSqlModel):
        self._db_instance: OrderSqlModel = db_instance

    @classmethod
    def from_db_instance(cls, db_instance: OrderSqlModel) -> 'OrderModel':
        return cls(db_instance)

    @property
    def id(self) -> str:
        return self._db_instance.id

    @property
    def amount(self) -> int:
        return self._db_instance.amount

    async def get_status(self) -> OrderStatusID:
        async with get_async_session() as session:
            db_instance_in_session: OrderSqlModel = await session.get(OrderSqlModel, self.id)
            return db_instance_in_session.status

    async def set_status(self, new_status: OrderStatusID, in_session: AsyncSession = None):
        async with (in_session or get_async_session()) as session:
            query = select(OrderSqlModel).where(OrderSqlModel.id == self.id).with_for_update()
            query_result = await session.execute(query)
            db_instance_in_session: OrderSqlModel = query_result.scalar_one()
            db_instance_in_session.status = new_status
            await session.commit()

    async def fulfil_order(self):
        if await self.get_status() == OrderStatusID.PAYED:
            raise OrderAlreadyCompleted

        async with get_async_session() as session:
            order_items = self._db_instance.items
            order_completed_items = dict()

            for item in order_items:
                game_query = select(GameSqlModel).where(GameSqlModel.id == item.game_id)
                game_result = await session.execute(game_query)
                game = game_result.scalar_one()
                keys_query = select(SteamKeySqlModel).where(
                    SteamKeySqlModel.category_id == game.key_category_id,
                    SteamKeySqlModel.order_item_id == None
                ).limit(item.count).with_for_update()

                keys = await session.execute(keys_query)
                keys = keys.scalars().all()
                for key in keys:
                    key.order_item_id = item.id

                order_completed_items[game.name] = [k.value for k in keys]
                await session.commit()

            await self.set_status(OrderStatusID.PAYED, in_session=session)

        return order_completed_items

    async def get_items(self):
        if await self.get_status() != OrderStatusID.PAYED:
            raise OrderNotCompleted

        async with get_async_session() as session:
            order_items = self._db_instance.items
            order_completed_items = dict()
            for item in order_items:
                game_query = select(GameSqlModel).where(GameSqlModel.id == item.game_id)
                game_result = await session.execute(game_query)
                game = game_result.scalar_one()
                keys_query = select(SteamKeySqlModel).where(
                    SteamKeySqlModel.order_item_id == item.id
                )

                keys = await session.execute(keys_query)
                keys = keys.scalars().all()
                order_completed_items[game.name] = [k.value for k in keys]

        return order_completed_items
