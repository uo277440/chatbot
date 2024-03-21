from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        #fields=('id','name','password') para no hacer todos
        fields = '__all__'