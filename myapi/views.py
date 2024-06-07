from django.contrib.auth import get_user_model,login,logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework.views import APIView
from .serializer import UserSerializer,UserRegisterSerializer,UserLoginSerializer,ScenerySerializer,FlowSerializer,UserSerializer,MarkSerializer,AverageMarkSerializer,ForumMessageSerializer
from .models import Flow, Step,FlowService,ScenaryService,Mark,AppUser,ForumMessage,Scenery
from chatbot.svm import SVMChatbot
from chatbot.grammar import GrammarCorrector
from chatbot.grammar import SentenceChecker
from chatbot.reproductor import text_to_audio
from chatbot.flow_manager import FlowManager,Marker
from .validations import custom_validation,validate_email,validate_password
from django.contrib.auth import get_user_model, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from .importarFlujos import cargar_datos_a_bd
from .importTraining import cargar_datos_csv_a_bd
from .generateCsv import generar_csv_entrenamiento
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db.models import Q
import csv
import random
import json
import os
from django.db import transaction



sentence_checker = SentenceChecker()
marker = Marker()
chatbot = None
scenary_service = ScenaryService()
grammarCorrector = GrammarCorrector()  
flowManager = None

def is_admin(user):
    return user.is_superuser
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_chatbot(request):
    if chatbot and flowManager:
        print(flowManager.description)
        print(flowManager.id)
        return Response({'chatbot': True,'description':flowManager.description},status=status.HTTP_200_OK)
    else:
        return Response({'chatbot': False},status=status.HTTP_200_OK)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def scenarios(request):
    try:
        scenarios = scenary_service.get_all_scenarios()
        serializer = ScenerySerializer(scenarios, many=True)
        return Response({'scenarios': serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Error en el servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def update_flow_manager(request):
    flow_id = request.GET.get('flow_id')
    first_charge = False
    try:
        flow = Flow.objects.get(id=flow_id)
    except Flow.DoesNotExist:
        return JsonResponse({'error': 'Flujo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    global flowManager
    global chatbot
    if(not flowManager):
        first_charge = True
    # Definir la ruta del archivo del modelo específico para el flujo
    model_path = f'models/svm_model_{flow_id}.pkl'
    # Crear la carpeta models si no existe
    os.makedirs('models', exist_ok=True)
    new_flow_manager = FlowManager(flow.id)
    new_chatbot = SVMChatbot(generar_csv_entrenamiento(flow.id), model_path=model_path)
    if not new_chatbot.load_model():
        new_chatbot.load_data()  
        new_chatbot.train_model()
    flowManager = new_flow_manager
    chatbot = new_chatbot
    return JsonResponse({'message': 'flowManager actualizado correctamente','first_charge':first_charge},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_scenary(request):
    json_file = request.FILES.get('json_file')
    scenario = request.data.get('scenario')
    if json_file:
        # Lógica para procesar el archivo JSON y cargarlo en la base de datos
        flow = cargar_datos_a_bd(json_file,scenario)
        return JsonResponse({'message': 'El JSON se ha subido correctamente', 'flow': {'id': flow.id, 'name': flow.name}}, status=200)
    else:
        return JsonResponse({'error': 'No se proporcionó ningún archivo JSON'}, status=400)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_training(request):
    csv_file = request.FILES.get('csv_file')
    flow = request.data.get('flow')
    if csv_file and flow:
        # Lógica para procesar el archivo JSON y cargarlo en la base de datos
        cargar_datos_csv_a_bd(csv_file,flow)
        return JsonResponse({'message': 'El JSON se ha subido correctamente'}, status=200)
    else:
        return JsonResponse({'error': 'No se proporcionó ningún archivo JSON'}, status=400)
from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_combined(request):
    json_file = request.FILES.get('json_file')
    csv_file = request.FILES.get('csv_file')
    scenario = request.data.get('scenario')
    if not json_file or not csv_file or not scenario:
        return JsonResponse({'error': 'JSON file, CSV file, and scenario are required'}, status=400)
    # Parse the JSON file
    try:
        json_data = json.load(json_file)
    except json.JSONDecodeError:
        print('cague?')
        return JsonResponse({'error': 'Invalid JSON file'}, status=400)

    # Read the CSV file
    try:
        print('joujou')
        csv_content = csv_file.read().decode('utf-8').splitlines()
        csv_data = list(csv.DictReader(csv_content))
        csv_file.seek(0)  
    except Exception as e:
        return JsonResponse({'error': 'Invalid CSV file'}, status=400)

    # Extract JSON keys and CSV headers
    json_labels = {step['label'] for flow in json_data['flows'] for step in flow['steps']}
    csv_labels_count = {label: 0 for label in json_labels}
    print('jaja')
    for row in csv_data:
        label = row.get('Label')
        if label in csv_labels_count:
            csv_labels_count[label] += 1

    # Check if all JSON labels are in CSV and have at least 10 phrases
    for label, count in csv_labels_count.items():
        if count < 10:
            print(count)
            print(label)
            return JsonResponse({'error': f'Label {label} has less than 10 phrases in the CSV file'}, status=400)
    print('perdi?')
    # Proceed with saving JSON and CSV data to the database
    try:
        with transaction.atomic():
            flow = cargar_datos_a_bd(json_data, scenario)
            csv_file.seek(0)  # Reset the file pointer again before re-reading for saving
            csv_data = csv.DictReader(csv_content)  # Re-read for actual processing
            cargar_datos_csv_a_bd(csv_data, flow)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Files uploaded and verified successfully', 'flow': {'id': flow.id, 'name': flow.name}}, status=200)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_flows_by_scenario_url(request):
    scenery_id = request.GET.get('scenery_id')
    if scenery_id is not None:
        try:
            flows = Flow.objects.filter(scenery_id=scenery_id)
            serializer = FlowSerializer(flows, many=True)
            return Response({'flows': serializer.data},status=200)
        except Flow.DoesNotExist:
            return Response({'error': 'No se encontraron flujos para el escenario dado'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Se requiere el parámetro "scenery_id"'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chatbot_response(request):
    if request.method == 'GET':
        user_message = request.GET.get('message', '')
        suggestions = grammarCorrector.correct_text(user_message)
        if suggestions:
            marker.decrease()
            response_text = '\n'.join(suggestions)
            return Response({'response': response_text,'suggestion':True},status=200)
        if not sentence_checker.is_sentence_coherent(user_message):
            return Response({'response':'La frase debe ser coherente y bien ligada','suggestion':True},status=200)
        bot_response = chatbot.predict_response_with_confidence(user_message)
        if(not bot_response):
            return Response({'response': 'Creo que no te entiendo del todo'},status=200)
        if(flowManager.advance(bot_response)):
            response=flowManager.response 
            if random.random() < 0.25:
                print('TOCO')
                try:
                    response=grammarCorrector.get_synonym_phrase(response)
                except Exception as e:
                    pass
            if flowManager.is_finished():
                mark_value = marker.mark
                try:
                    user = AppUser.objects.get(user_id=request.user.user_id)
                    flow = Flow.objects.get(id=flowManager.id)
                    mark = Mark.objects.create(flow=flow, user=user, mark=mark_value)
                    mark.save()
                except AppUser.DoesNotExist:
                    return Response({'response': 'Usuario no encontrado'},status=status.HTTP_404_NOT_FOUND)
                except Flow.DoesNotExist:
                    return Response({'response': 'Flujo no encontrado'},status=status.HTTP_404_NOT_FOUND)
        else:
            response="FLUJO NO VA BIEN" + bot_response
        if(response is None):
            return Response({'response': 'La respuesta es incoherente'},status=200)
        return Response({'response': response,'is_finished':flowManager.is_finished(),'mark': marker.mark,'suggestion':False},status=200)
@api_view(['GET'])
@permission_classes([AllowAny])
def mascot_message(request):
    if request.method == 'GET':
        marker.decrease()
        return Response({'response': flowManager.suggest()},status=200)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_student(request):
    search_param = request.query_params.get('search_param', None)
    if search_param:
        users = AppUser.objects.filter(Q(username=search_param) | Q(email=search_param))
        if users.exists():
            user = users.first()
            user_serializer = UserSerializer(user)
            marks = Mark.objects.filter(user=user)
            marks_serializer = MarkSerializer(marks, many=True)
            return Response({'user': user_serializer.data, 'marks': marks_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Username parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transform(request):
    if request.method == 'GET':
        text = request.GET.get('text', '')
        sourceLang = request.GET.get('source', '')
        return Response({'delay': text_to_audio(text,sourceLang)},status=200)
    return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restart_flow(request):
    if request.method == 'GET':
        flowManager.reset_flow()
        marker.restart()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def translate(request):
    if request.method == 'GET':
        text = request.GET.get('text', '')
        targetLang = request.GET.get('target', '')
        translated_text=grammarCorrector.translate(text,targetLang)
        if(targetLang == 'es'):
            marker.decrease()
        return Response({'translated_text': translated_text},status=200)
    return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    user = request.user

    # Serializar datos del usuario
    user_serializer = UserSerializer(user)

    # Obtener las notas medias de cada flujo para el usuario
    marks = Mark.objects.filter(user=user).values('flow').annotate(average_mark=Avg('mark'))
    
    # Crear lista de datos serializados con las notas medias
    average_marks = []
    for mark in marks:
        flow = Flow.objects.get(id=mark['flow'])
        average_marks.append({'flow': flow, 'average_mark': mark['average_mark']})

    average_marks_serializer = AverageMarkSerializer(average_marks, many=True)

    return Response({
        'user': user_serializer.data,
        'average_marks': average_marks_serializer.data
    }, status=status.HTTP_200_OK)
	    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request,message_id):
    try:
        message = ForumMessage.objects.get(id=message_id)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ForumMessage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_message(request,message_id):
    try:
        message = ForumMessage.objects.get(id=message_id, user=request.user)
    except ForumMessage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ForumMessageSerializer(message, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=200)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def forum_messages(request):
    try:
        messages = ForumMessage.objects.all().order_by('date')
        pinned_message = ForumMessage.objects.filter(pinned=True).first()
        serializer = ForumMessageSerializer(messages, many=True)
        pinned_serializer = ForumMessageSerializer(pinned_message)
        return Response({'messages':serializer.data,'pinnedMessage': pinned_serializer.data if pinned_serializer else None}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
'''
class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        try:
            clean_data = custom_validation(request.data)
            serializer = UserRegisterSerializer(data=clean_data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.create(clean_data)
                if user:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)
'''
@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    try:
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_flow(request):
    flow_id = request.data.get('flow_id')
    if not flow_id:
        return Response({'error': 'Flow ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        flow = Flow.objects.get(id=flow_id)
        scenery = flow.scenery
        model_path = f'models/svm_model_{flow_id}.pkl'
        flow.delete()
        if os.path.exists(model_path):
            os.remove(model_path)
        if not scenery.flows.exists():
            scenery.delete()
        return Response({'message': 'Flow deleted successfully'}, status=status.HTTP_200_OK)
    except Flow.DoesNotExist:
        return Response({'error': 'Flow not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_flows_by_scenario(request, scenario_name):
    try:
        scenario = Scenery.objects.get(name=scenario_name)
        flows = scenario.flows.all()
        flows_data = [{'id': flow.id, 'name': flow.name} for flow in flows]
        return Response({'flows': flows_data}, status=status.HTTP_200_OK)
    except Scenery.DoesNotExist:
        return Response({'error': 'Scenario not found'}, status=status.HTTP_404_NOT_FOUND)
'''
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    def post(self, request):
        data = request.data
        try:
            validate_email(data)
            validate_password(data)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserLoginSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.check_user(data)
                login(request, user)
                user_data = UserSerializer(user).data
                return Response({'user': user_data }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No autorizado'}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)
       
    
class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
        '''
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication])
def user_login(request):
    data = request.data
    try:
        validate_email(data)
        validate_password(data)
    except ValidationError as e:
        return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserLoginSerializer(data=data)
    try:
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            user_data = UserSerializer(user).data
            return Response({'user': user_data }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No autorizado'}, status=status.HTTP_401_UNAUTHORIZED)
    except ValidationError as e:
        return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'message': 'Los datos introducidos son incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def user_logout(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def user_view(request):
    serializer = UserSerializer(request.user)
    return Response({'user': serializer.data}, status=status.HTTP_200_OK)

