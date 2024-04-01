from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import UserSerializer
from .models import User
from chatbot.svm import SVMChatbot
from chatbot.grammar import GrammarCorrector
from chatbot.flow_manager import FlowManager


class UserView(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset = User.objects.all()

chatbot = SVMChatbot('hotel_usuario.csv')
chatbot.load_data()  
chatbot.train_model()
grammarCorrector = GrammarCorrector()  
flowManager = FlowManager('hotel_flujos.json', 'RESERVATION_FLOW')
@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

@api_view(['GET'])
def chatbot_response(request):
    if request.method == 'GET':
        print('holaaaaaaaaaa')
        user_message = request.GET.get('message', '')
        suggestions = grammarCorrector.correct_text(user_message)
        if suggestions:
            return Response({'response': suggestions})
        bot_response = chatbot.predict_response_with_confidence(user_message)
        if(flowManager.advance(bot_response)):
            response=flowManager.response + bot_response
        else:
            response="FLUJO NO VA BIEN" + bot_response
        if(response is None):
            return Response({'response': 'La respuesta es incoherente'})
        return Response({'response': response})
@api_view(['GET'])
def mascot_message(request):
    if request.method == 'GET':
        return Response({'response': flowManager.suggest()})