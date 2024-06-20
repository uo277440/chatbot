from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from .firebase_config import db


class AppUserManager(BaseUserManager):
	def create_user(self,email,username, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email, username=username)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email,username, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email,username, password)
		user.is_superuser = True
		user.save()
		return user
class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=50, unique=True)
	username = models.CharField(max_length=50, unique=True)
	is_superuser=models.BooleanField(default=False)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	objects = AppUserManager()
 
	class Meta:
		db_table = 'appuser'
        
	def __str__(self):
		return self.username



class FlowService(models.Manager):
    def get_flow_by_name(self, name):
        try:
            return self.get(name=name)
        except Flow.DoesNotExist:
            return None

    def get_steps_for_flow(self, flow_name):
        flow = self.get_flow_by_name(flow_name)
        if flow:
            return flow.steps.all()
        return None
class ScenaryService(models.Manager):
    def get_scenary_by_name(self, name):
        try:
            return self.get(name=name)
        except Scenery.DoesNotExist:
            return None
    def get_all_scenarios(self):
        try:
            return Scenery.objects.all()
        except Scenery.DoesNotExist:
            return None
class Scenery(models.Model):
    name = models.CharField(max_length=100,unique=True)
    objects = ScenaryService()
    
    class Meta:
        db_table = 'scenery'
    
class Flow(models.Model):
    name = models.CharField(max_length=100,unique=False)
    objects = FlowService()
    scenery = models.ForeignKey(Scenery, on_delete=models.CASCADE, related_name='flows')
    description= models.CharField(max_length=500,unique=False,default="Bienvenido al flujo. Recuerda empezar saludando !")
    class Meta:
        db_table = 'flow'
        unique_together = ('name', 'scenery')

class Step(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name='steps')
    label = models.CharField(max_length=100)
    message = models.TextField()
    suggestion = models.TextField()
    options = ArrayField(models.CharField(max_length=100), blank=True)
    
    class Meta:
        db_table = 'step'

class Mark(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name='marks')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='marks')
    mark = models.DecimalField(max_digits=3, decimal_places=1)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'mark'
        
        
class ChatbotData(models.Model):
    user_input = models.TextField()
    label = models.CharField(max_length=50)
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name='chatbot_data')
    
    class Meta:
        db_table = 'training'
        
    def __str__(self):
        return f"{self.user_input} - {self.label}"

class ForumMessage(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='mensajes_foro')
    date = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False)

    class Meta:
        db_table = 'forum_message'
        ordering = ['-date']
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_firestore('send')

    def delete(self, *args, **kwargs):
        self.update_firestore('delete')
        super().delete(*args, **kwargs)

    def update_firestore(self, action):
        message_data = {
            'id': self.id,
            'message': self.message,
            'user_id': self.user.user_id,
            'username': self.user.username,
            'timestamp': self.date,
            'isPinned': self.pinned
        }

        if action == 'send' or action == 'edit':
            db.collection('messages').document(str(self.id)).set(message_data)
        elif action == 'delete':
            db.collection('messages').document(str(self.id)).delete()
        elif action == 'pin':
            db.collection('messages').document(str(self.id)).update({'isPinned': True})
        elif action == 'unpin':
            db.collection('messages').document(str(self.id)).update({'isPinned': False})
class ChatConversation(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='conversations')
    conversation = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_conversation'