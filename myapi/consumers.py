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
        action = text_data_json.get('action', 'send')
        

        # Enviar el mensaje al grupo de WebSocket
        if action == 'send':
            message = text_data_json['message']
            user = text_data_json['user'] 
            user = await self.get_user_from_id(user)
            # Guardar el mensaje en la base de datos solo si el usuario está presente
            if user:
                forum_message = await self.save_forum_message(message, user)
            await(self.channel_layer.group_send)(
                'forum_group',
                {
                    'type': 'send_message',
                    'id': forum_message.id,
                    'message': message,
                    'username': user.username if user else 'Anonymous',  
                    'user_id': user.user_id,
                    'is_superuser': user.is_superuser,
                }
            )
        elif action == 'delete':
            id = text_data_json['id']
            await self.delete_forum_message(id)
            await self.channel_layer.group_send(
                'forum_group',
                {
                    'type': 'delete_message',
                    'id': id
                }
            )
        elif action == 'edit':
            message = text_data_json['message']
            id = text_data_json['id']
            await self.edit_forum_message(id, message)
            await self.channel_layer.group_send(
                'forum_group',
                {
                    'type': 'edit_message',
                    'message': message,
                    'id': id
                }
            )
        
    async def delete_message(self, event):
        await self.send(text_data=json.dumps({
            'action': 'delete',
            'id': event['id']
        }))

    async def edit_message(self, event):
        await self.send(text_data=json.dumps({
            'action': 'edit',
            'message': event['message'],
            'id': event['id']
        }))
        
    
    async def send_message(self, event):
        # Verificar si 'username' está en el evento
        if 'username' in event:
            print(event)
            message = event['message']
            username = event['username']
            user_id = event['user_id']
            is_superuser = event['is_superuser']
            id=event['id']
            print('metodo send_message')

            await self.send(text_data=json.dumps({
                'action':'send',
                'message': message,
                'user': {'username': username,'user_id': user_id,'is_superuser':is_superuser},
                'id':id,
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
        return ForumMessage.objects.create(message=message, user=user)
    @staticmethod
    @database_sync_to_async
    def delete_forum_message(message_id):
        ForumMessage.objects.filter(id=message_id).delete()

    @staticmethod
    @database_sync_to_async
    def edit_forum_message(message_id, new_content):
        ForumMessage.objects.filter(id=message_id).update(message=new_content)