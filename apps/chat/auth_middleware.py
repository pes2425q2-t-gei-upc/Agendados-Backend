import jwt
from django.contrib.auth.models import User, AnonymousUser
from urllib.parse import parse_qs
from rest_framework.exceptions import AuthenticationFailed
from channels.db import database_sync_to_async

SECRET_KEY = 'your_secret_key'

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        print('code on auth middleware')
        query_string = scope.get('query_string', b'').decode('utf-8')
        query_params = parse_qs(query_string)

        token = query_params.get('token', [None])[0]

        if token:
            scope['user'] = await self.get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            return User.objects.get(auth_token=token)
        except User.DoesNotExist:
            return AnonymousUser()
