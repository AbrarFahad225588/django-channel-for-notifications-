from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.authentication import JWTAuthentication


@database_sync_to_async
def get_user_from_token(token):
    try:
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        return jwt_auth.get_user(validated_token)
    except Exception:
        return AnonymousUser()


class JWTAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):

        headers = dict(scope["headers"])
     
        scope["user"] = AnonymousUser()

        auth_header = headers.get(b"authorization")
        # print(auth_header)

        if auth_header:
            try:
                auth_header = auth_header.decode()

                if auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]
                    scope["user"] = await get_user_from_token(token)

            except Exception:
                pass

        return await self.inner(scope, receive, send)