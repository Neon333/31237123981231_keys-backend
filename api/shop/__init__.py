from fastapi import FastAPI


def register_in_fastapi(app: FastAPI):
    from .games import shop_router
    from .order import shop_orders_router

    app.include_router(shop_router, prefix='/api')
    app.include_router(shop_orders_router, prefix='/api')
