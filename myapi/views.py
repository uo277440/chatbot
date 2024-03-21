from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import UserSerializer
from .models import User


class UserView(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset = User.objects.all()
    
@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})