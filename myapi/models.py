from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
import json

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
	username = models.CharField(max_length=50)
	is_superuser=models.BooleanField(default=False)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	objects = AppUserManager()
 
	class Meta:
		db_table = 'appuser'
        
	def __str__(self):
		return self.username

class Flow(models.Model):
    name = models.CharField(max_length=100)

class Step(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name='steps')
    label = models.CharField(max_length=100)
    message = models.TextField()
    suggestion = models.TextField()
    options = ArrayField(models.CharField(max_length=100), blank=True)


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
    name = models.CharField(max_length=100,unique=True)
    objects = FlowService()
    scenery = models.ForeignKey(Scenery, on_delete=models.CASCADE, related_name='scenery')
    class Meta:
        db_table = 'flow'
		

class Step(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name='steps')
    label = models.CharField(max_length=100)
    message = models.TextField()
    suggestion = models.TextField()
    options = ArrayField(models.CharField(max_length=100), blank=True)
    
    class Meta:
        db_table = 'step'