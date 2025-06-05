from fastapi import Request, HTTPException, APIRouter
from fastapi.params import Depends

from core import CrystalPayAsyncClient, get_crystalpay_client
from core.order import Order


payments_router = APIRouter()



@payments_router.post("/payment-webhook04328261")
async def payment_webhook(request: Request, crystal_pay: CrystalPayAsyncClient = Depends(get_crystalpay_client)):
    data = await request.json()
    received_sign = data.get("signature")
    amount = int(data.get("rub_amount"))

    ps_order_id = data.get("id")
    local_order_id = data.get("extra")

    if not crystal_pay.verify_signature(ps_order_id, received_sign):
        raise HTTPException(status_code=400, detail="Invalid signature")

    if (order := await Order.get_by_id(local_order_id)) is None:
        raise HTTPException(status_code=400, detail="Order not found")

    if order.amount != amount:
        raise HTTPException(status_code=400, detail="Invalid amount")

    await order.fulfil_order()
    return {'s': 's'}
