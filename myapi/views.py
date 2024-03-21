from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import UserSerializer
from .models import User
from chatbot.svm import SVMChatbot


class UserView(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset = User.objects.all()

chatbot = SVMChatbot('hotel_usuario.csv', 'hotel_chatbot.csv')
    
@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

@api_view(['GET'])
def chatbot_response(request):
    if request.method == 'GET':
        user_message = request.GET.get('message', '')
        chatbot.load_data()  
        chatbot.train_model()
        bot_response = chatbot.predict_response(user_message)
        return Response({'response': bot_response})