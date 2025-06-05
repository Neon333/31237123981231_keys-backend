from fastapi import FastAPI, Request, HTTPException, Depends
from core.user.auth import UserAuthentication, UserRoleID


async def admin_rights_check(request: Request):
    auth_header: str = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await UserAuthentication.auth_by_token(auth_header.replace('Bearer ', ''))
    if user is None or not user.role == UserRoleID.ADMIN:
        raise HTTPException(status_code=401, detail="Unauthorized")


def register_in_fastapi(app: FastAPI):
    from .games import admin_games_router
    from .keys import admin_keys_router
    from .auth import admin_login_router

    app.include_router(admin_games_router, prefix='/api/admin', dependencies=[Depends(admin_rights_check)])
    app.include_router(admin_keys_router, prefix='/api/admin', dependencies=[Depends(admin_rights_check)])
    app.include_router(admin_login_router, prefix='/api/admin')
