from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from core.user.auth import UserAuthentication

admin_login_router = APIRouter()


class AuthSchema(BaseModel):
    email: str
    password: str


class SuccessAuthSchema(BaseModel):
    token: str


@admin_login_router.post("/login3487324823", response_model=SuccessAuthSchema)
async def auth(account: AuthSchema):
    token = await UserAuthentication.auth_by_password(account.email, account.password)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return SuccessAuthSchema(token=token)
