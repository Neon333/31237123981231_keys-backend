from fastapi import FastAPI


def register_in_fastapi(app: FastAPI):
    from .webhook import payments_router
    app.include_router(payments_router, prefix='/api')
