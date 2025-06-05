from pydantic import BaseModel
from core.database.sql_models.order import OrderStatusID


class OrderItem(BaseModel):
    game_id: int
    count: int


class OrderItemInDB(OrderItem):
    order_id: int


class NewOrder(BaseModel):
    items: list[OrderItem]
    client_ip: str = None


class OrderInDB(NewOrder):
    id: str
    status: int
    items: list[OrderItemInDB]


class CompletedOrderItem(BaseModel):
    game_name: str
    keys: list[str]


class _OrderWithStatus(BaseModel):
    id: str
    status: int


class PendingOrder(_OrderWithStatus):
    status = OrderStatusID.PENDING


class FailedOrder(_OrderWithStatus):
    status = OrderStatusID.FAILED


class CompletedOrder(_OrderWithStatus):
    items: list[CompletedOrderItem]
    status = OrderStatusID.PAYED

