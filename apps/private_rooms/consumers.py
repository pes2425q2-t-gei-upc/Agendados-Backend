from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.private_rooms.models import PrivateRoom, PrivateRoomEvent, PrivateRoomVote
import json

from apps.users.seralizers import UserSerializer

@sync_to_async
def serialize_user(user, many=False):
    return UserSerializer(user, many=many).data

@sync_to_async
def serialize_event(event, many=False):
    return EventSerializer(event, many=many).data


@sync_to_async
def get_vote_results(private_room_event):
    """Get vote results for a private room event"""
    votes = PrivateRoomVote.objects.filter(private_room_event=private_room_event)
    total_votes = votes.count()
    true_votes = votes.filter(vote=True).count()
    false_votes = votes.filter(vote=False).count()

    return {
        'total_votes': total_votes,
        'true_votes': true_votes,
        'false_votes': false_votes,
    }

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
        serialized_participants = await serialize_user(room.participants, True)
        serialized_user = await serialize_user(user, False)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'participants': serialized_participants,
                'user_joined': serialized_user
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
        serialized_participants = await serialize_user(room.participants, True)
        serialized_user = await serialize_user(user, False)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'participants': serialized_participants,
                'user_left': serialized_user
            }
        )

    # Handler for user_joined event
    async def user_joined(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'participants': event['participants'],
            'user_joined': event['user_joined'],
        }))

    # Handler for user_left event
    async def user_left(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'participants': event['participants'],
            'user_left': event['user_left'],
        }))

    # Handler for receiving events
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'start_room':
            await self.start_room()

    async def start_room(self):
        user = self.scope['user']
        room = await sync_to_async(PrivateRoom.objects.get)(code=self.room_code)
        if user.id != room.admin_id:
            return

        room.is_active = True
        await sync_to_async(room.save)()

        # Notify all participants
        events = await sync_to_async(lambda: list(Event.objects.order_by('-id')[:50]))()
        events_serialized = await serialize_event(events, True)
        # Create PrivateRoomEvent instances for each event
        for index, event in enumerate(events):
            await sync_to_async(PrivateRoomEvent.objects.create)(
                private_room=room,
                event=event,
                is_current=(index == 0)
            )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_started',
                'event': events_serialized[0],
            }
        )

    async def room_started(self, event):
        await self.send(text_data=json.dumps({
            'type': 'room_started',
            'event': event['event'],
        }))

    async def handle_vote(self, data):
        user = self.scope['user']
        vote_value = data.get('vote')

        # Get the room and current event
        room = await sync_to_async(PrivateRoom.objects.get)(code=self.room_code)
        current_event = await sync_to_async(
            PrivateRoomEvent.objects.get
        )(private_room=room, is_current=True)

        # Create the vote
        vote, created = await sync_to_async(PrivateRoomVote.objects.get_or_create)(
            private_room_event=current_event,
            participant=user,
            defaults={'vote': vote_value}
        )

        vote_results = await get_vote_results(current_event)
        serialized_user = await serialize_user(user, False)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'vote_casted',
                'user': serialized_user,
                'vote': vote_value,
                'vote_results': vote_results,
            }
        )

    async def vote_cast(self, event):
        await self.send(text_data=json.dumps({
            'type': 'vote_cast',
            'user': event['user'],
            'vote': event['vote'],
            'vote_results': event['vote_results'],
        }))