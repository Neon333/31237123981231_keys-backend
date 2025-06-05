import bcrypt
import secrets
from .user import User, UserRoleID
from .models.auth import AuthTokenRepo


class UserAuthentication:

    @classmethod
    async def auth_by_password(cls, email: str, password: str) -> str | None:
        user = await User.get_by_email(email)
        print(user)
        auth_success = user is not None and bcrypt.checkpw(password.encode(), user.password_hash.encode())
        if not auth_success:
            return None

        token_val = secrets.token_hex(64)
        await AuthTokenRepo.create(user.id, value=token_val)
        return token_val

    @classmethod
    async def auth_by_token(cls, auth_token: str) -> User | None:
        token = await AuthTokenRepo.get_by_value(auth_token)
        return await User.get_by_id(token.user_id) if token is not None else None
