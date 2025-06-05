from fastapi import APIRouter, Request
from fastapi.params import Depends

import config
from api.schemas.shop.order import OrderCreated
from core import get_crystalpay_client, CrystalPayAsyncClient
from core.order.dto import CompletedOrder, CompletedOrderItem, PendingOrder, FailedOrder
from core.database.sql_models.order import OrderStatusID
from core.order import Order
from core.order.dto import NewOrder

shop_orders_router = APIRouter(prefix="")


@shop_orders_router.get("/orders/{order_id}")
async def get_order(order_id: str):
    order = await Order.get_by_id(order_id)
    status = await order.get_status()
    if status == OrderStatusID.PAYED:
        items = await order.get_items()
        return CompletedOrder(
            id=order.id,
            status=OrderStatusID.PAYED,
            items=[CompletedOrderItem(game_name=name, keys=keys) for name, keys in items.items()]
        )
    order_data_cls = FailedOrder if status == OrderStatusID.FAILED else PendingOrder
    return order_data_cls(
        id=order.id,
        status=status,
    )


@shop_orders_router.post("/orders", response_model=OrderCreated)
async def create_order(new_order: NewOrder, request: Request, crystal_pay: CrystalPayAsyncClient = Depends(get_crystalpay_client)):
    new_order.client_ip = request.client.host
    created_order = await Order.create(new_order)
    created_order = await Order.get_by_id(created_order.id)
    payment_form_html = await crystal_pay.generate_payment_form(
        created_order.amount, invoice_type='purchase', lifetime=10,
        redirect_url=f'https://{config.WEBSITE_DOMAIN}/order-status',
        callback_url=f'https://{config.PAYMENTS_WEBHOOK_URL}',
        extra=created_order.id
    )

    return OrderCreated(id=created_order.id, payment_form_html=payment_form_html)
