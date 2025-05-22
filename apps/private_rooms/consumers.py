from channels.generic.websocket import AsyncWebsocketConsumer


class PrivateRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Connecting to private room consumer')
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'room_{self.room_code}'

        #Get user
        user = self.scope['user']
        if not user.is_authenticated:
            print('User not authenticated, closing connection')
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )