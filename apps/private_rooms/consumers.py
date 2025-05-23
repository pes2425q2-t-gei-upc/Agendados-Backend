from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.private_rooms.models import PrivateRoom
import json

from apps.users.seralizers import UserSerializer

@sync_to_async
def serialize_user(user):
    return UserSerializer(user).data

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

        #Create the room-user relation
        room, _ = await sync_to_async(PrivateRoom.objects.get_or_create)(code=self.room_code)
        await sync_to_async(room.participants.add)(user)

        #Notify room participants
        serialized_user = await serialize_user(user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user': serialized_user,
            }
        )

    async def disconnect(self, close_code):
        user = self.scope['user']
        #Delete the room-user relation
        room, _ = await sync_to_async(PrivateRoom.objects.get_or_create)(code=self.room_code)
        await sync_to_async(room.participants.remove)(user)

        #Leave the room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        #Notify room participants
        serialized_user = await serialize_user(user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'user': serialized_user,
            }
        )

    # Handler for user_joined event
    async def user_joined(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'user': event['user'],
        }))

    # Handler for user_left event
    async def user_left(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'user': event['user'],
        }))