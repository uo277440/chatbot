from django.contrib.auth import get_user_model,login,logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework.views import APIView
from .serializer import UserSerializer,UserRegisterSerializer,UserLoginSerializer,ScenerySerializer,FlowSerializer
from .models import Flow, Step,FlowService,ScenaryService,Mark
from chatbot.svm import SVMChatbot
from chatbot.grammar import GrammarCorrector
from chatbot.reproductor import text_to_audio
from chatbot.flow_manager import FlowManager,Marker
from .validations import custom_validation,validate_email,validate_password
from django.contrib.auth import get_user_model, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from .importarFlujos import cargar_datos_a_bd
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test




mark = Marker()
chatbot = SVMChatbot('hotel_usuario.csv')
chatbot.load_data()  
chatbot.train_model()
scenary_service = ScenaryService()
grammarCorrector = GrammarCorrector()  
flowManager = FlowManager('hotel_flujos.json', 'RESERVATION_FLOW')
def is_admin(user):
    return user.is_superuser
@api_view(['GET'])
def hello_world(request):
    print('adioss')
    return Response({'message': 'Hello, world!'})
@api_view(['GET'])
@permission_classes([AllowAny])
def scenarios(request):
    scenarios = scenary_service.get_all_scenarios()
    serializer = ScenerySerializer(scenarios, many=True)
    return Response({'scenarios': serializer.data})
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_scenary(request):
    print('holaaaaaa')
    json_file = request.FILES.get('json_file')
    scenario = request.data.get('scenario')
    print('holaaaaaa')
    print(scenario)
    if json_file:
        # Lógica para procesar el archivo JSON y cargarlo en la base de datos
        cargar_datos_a_bd(json_file,scenario)
        return JsonResponse({'message': 'El JSON se ha subido correctamente'}, status=200)
    else:
        return JsonResponse({'error': 'No se proporcionó ningún archivo JSON'}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_flows_by_scenario(request):
    scenery_id = request.GET.get('scenery_id')
    if scenery_id is not None:
        try:
            flows = Flow.objects.filter(scenery_id=scenery_id)
            serializer = FlowSerializer(flows, many=True)
            return Response({'flows': serializer.data})
        except Flow.DoesNotExist:
            return Response({'error': 'No se encontraron flujos para el escenario dado'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Se requiere el parámetro "scenery_id"'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chatbot_response(request):
    if request.method == 'GET':
        print('holaaaaaaaaaa')
        user_message = request.GET.get('message', '')
        suggestions = grammarCorrector.correct_text(user_message)
        if suggestions:
            response_text = '\n'.join(suggestions)
            print(response_text)
            return Response({'response': response_text})
        bot_response = chatbot.predict_response_with_confidence(user_message)
        if(flowManager.advance(bot_response)):
            response=flowManager.response + bot_response
            '''
            if flowManager.is_finished():
                mark_value = mark.
                user = request.user  
                flow = 
                mark = Mark.objects.create(flow=flow, user=user, mark=mark_value)
                mark.save()
                '''
                
        else:
            response="FLUJO NO VA BIEN" + bot_response
        if(response is None):
            return Response({'response': 'La respuesta es incoherente'})
        return Response({'response': response})
@api_view(['GET'])
@permission_classes([AllowAny])
def mascot_message(request):
    if request.method == 'GET':
        mark.decrease()
        return Response({'response': flowManager.suggest()})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transform(request):
    if request.method == 'GET':
        print('hola')
        text = request.GET.get('text', '')
        sourceLang = request.GET.get('source', '')
        return Response({'delay': text_to_audio(text,sourceLang)})
    return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restart_flow(request):
    if request.method == 'GET':
        flowManager.reset_flow()
        mark.restart()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def translate(request):
    if request.method == 'GET':
        text = request.GET.get('text', '')
        targetLang = request.GET.get('target', '')
        translated_text=grammarCorrector.translate_to_spanish(text,targetLang)
        mark.decrease()
        return Response({'translated_text': translated_text})
    return Response(status=status.HTTP_400_BAD_REQUEST)
	    

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)