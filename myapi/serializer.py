from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .models import Scenery,Mark,Flow,Step,ForumMessage,ChatConversation

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'],username=clean_data['username'],password=clean_data['password'])
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
class ScenerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenery
        fields = ('id', 'name') 
class FlowSerializer(serializers.ModelSerializer):
    scenery = ScenerySerializer(read_only=True)
    class Meta:
        model = Flow
        fields = '__all__'  
class MarkSerializer(serializers.ModelSerializer):
    flow = FlowSerializer(read_only=True)
    date = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    class Meta:
        model = Mark
        fields = ('id', 'flow', 'user', 'mark','date')
class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'
class AverageMarkSerializer(serializers.Serializer):
    flow = FlowSerializer()
    average_mark = serializers.FloatField()

class ForumMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ForumMessage
        fields = ['id', 'message', 'user', 'date', 'pinned']
class ChatConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatConversation
        fields = ['conversation', 'date']
  