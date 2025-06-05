from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import api.admin as admin_api
import api.shop as shop_api
import api.payments as payments_api


fast_api_app = FastAPI()
fast_api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin_api.register_in_fastapi(fast_api_app)
shop_api.register_in_fastapi(fast_api_app)
payments_api.register_in_fastapi(fast_api_app)
