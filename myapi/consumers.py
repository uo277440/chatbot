# myapi/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ForumMessage
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .serializer import UserSerializer
from asgiref.sync import async_to_sync

User = get_user_model()

class ForumConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_scope(self.scope)
        await self.channel_layer.group_add(
            'forum_group',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'forum_group',
            self.channel_name
        )
    async def get_user_from_id(self,user_id):
        try:
            user = await database_sync_to_async(User.objects.get)(user_id=user_id)
            return user
        except User.DoesNotExist:
            return None
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']  # Asegúrate de que esta clave sea consistente con lo que envías desde el frontend
        print('metodo receive')
        # Obtener el usuario
        user = await self.get_user_from_id(user)
        # Guardar el mensaje en la base de datos solo si el usuario está presente
        if user:
            await self.save_forum_message(message, user)

        # Enviar el mensaje al grupo de WebSocket
        
        await(self.channel_layer.group_send)(
            'forum_group',
            {
                'type': 'send_message',
                'message': message,
                'username': user.username if user else 'Anonymous',  
            }
        )
        
        
        
    
    async def send_message(self, event):
        # Verificar si 'username' está en el evento
        if 'username' in event:
            print(event)
            message = event['message']
            username = event['username']
            print('metodo send_message')

            await self.send(text_data=json.dumps({
                'message': message,
                'user': {'username': username}
            }))
        else:
            print('Username not in event:', event)

    @staticmethod
    @database_sync_to_async
    def get_user_from_scope(scope):
        user = None
        if 'user' in scope:
            user = scope['user']
        print('metodo scope')
        return user

    @staticmethod
    @database_sync_to_async
    def save_forum_message(message, user):
        print('metodo bd')
        ForumMessage.objects.create(content=message, user=user)