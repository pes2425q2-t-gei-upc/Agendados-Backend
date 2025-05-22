from channels.generic.websocket import AsyncWebsocketConsumer


class PrivateRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Connecting to private room consumer')
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        user = self.scope['user']

        print(self.room_code)
        print(user)
