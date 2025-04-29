import json
from django.utils.timezone import localtime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.chat.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.room_group_name = f'event_{self.event_id}'

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

        #Send message history to the user
        await self.send_message_history()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        # Comprobar si es una solicitud de eliminación
        if 'action' in text_data_json and text_data_json['action'] == 'delete_message':
            message_id = text_data_json['message_id']
            
            # Eliminar cualquier mensaje sin verificar propietario (para pruebas)
            await self.delete_message(message_id)
            
            # Notificar a todos los clientes sobre la eliminación
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_deleted',
                    'deleted_message_id': message_id,
                }
            )
            return
        
        # Código existente para manejar mensajes normales
        message = text_data_json['message']

        user = self.scope['user']
        saved_message = await self.save_message(message)
        message_timestamp = localtime(saved_message.timestamp).strftime('%Y-%m-%d %H:%M:%S')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
                'user_id': user.id,
                'timestamp': message_timestamp,
                'message_id': saved_message.id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id']
        }))
        
    async def message_deleted(self, event):
        # Enviar mensaje de eliminación al WebSocket
        await self.send(text_data=json.dumps({
            'deleted_message_id': event['deleted_message_id']
        }))

    @database_sync_to_async
    def save_message(self, message):
        user = self.scope['user']
        chat_message = Message.objects.create(
            event_id=self.event_id,
            content=message,
            sender_id=user.id
        )
        return chat_message
            
    @database_sync_to_async
    def delete_message(self, message_id):
        Message.objects.filter(id=message_id).delete()

    async def send_message_history(self):
        messages = await self.get_message_history()

        if messages:
            await self.send(text_data=json.dumps({
                'message_history': messages
            }))

    @database_sync_to_async
    def get_message_history(self):
        messages = Message.objects.filter(
            event_id=self.event_id
        ).order_by('timestamp')

        history = []
        for msg in messages:
            username = msg.sender.username
            message_timestamp = localtime(msg.timestamp).strftime('%Y-%m-%d %H:%M:%S')

            history.append({
                'message': msg.content,
                'username': username,
                'user_id': msg.sender_id,
                'timestamp': message_timestamp,
                'message_id': msg.id
            })
        return history