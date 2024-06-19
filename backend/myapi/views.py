from django.contrib.auth import get_user_model,login,logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework.views import APIView
from .serializer import UserSerializer,UserRegisterSerializer,UserLoginSerializer,ScenerySerializer,FlowSerializer,UserSerializer,MarkSerializer,AverageMarkSerializer,ForumMessageSerializer,ChatConversationSerializer
from .models import Flow, Step,FlowService,ScenaryService,Mark,AppUser,ForumMessage,Scenery,ChatConversation
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
import pandas as pd
from django.db import transaction
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from firebase_admin import firestore
from .firebase_config import db

sentence_checker = SentenceChecker()
#marker = Marker()
#chatbot = None
scenary_service = ScenaryService()
grammarCorrector = GrammarCorrector()  
#flowManager = None
@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def getCSRFToken(request):
    token = get_token(request)
    return JsonResponse({"token": token}, status=200)
def is_admin(user):
    return user.is_superuser
def get_session_objects(session):
    chatbot_data = session.get('chatbot')
    flow_manager_data = session.get('flowManager')
    marker_data = session.get('marker')

    chatbot = SVMChatbot.deserialize(chatbot_data) if chatbot_data else None
    flow_manager = FlowManager.deserialize(flow_manager_data) if flow_manager_data else None
    marker = Marker.deserialize(marker_data) if marker_data else Marker()

    return chatbot, flow_manager, marker
def set_session_objects(session, chatbot=None, flow_manager=None, marker=None):
    if chatbot is not None:
        session['chatbot'] = chatbot.serialize()
    if flow_manager is not None:
        session['flowManager'] = flow_manager.serialize()
    if marker is not None:
        session['marker'] = marker.serialize()
    session.modified = True

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_chatbot(request):
    chatbot, flowManager, marker = get_session_objects(request.session)
    if chatbot and flowManager:
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
    chatbot, flowManager, marker = get_session_objects(request.session)
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
    #flowManager = new_flow_manager
    #chatbot = new_chatbot
    set_session_objects(request.session, new_chatbot, new_flow_manager, marker)
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
@permission_classes([permissions.IsAuthenticated])
def submit_conversation(request):
    conversation_data = request.data.get('conversation', None)
    if conversation_data:
        user = request.user
        conversation = ChatConversation.objects.create(
            user=user,
            conversation=conversation_data
        )
        serializer = ChatConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Conversation data is required'}, status=status.HTTP_400_BAD_REQUEST)
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
        return JsonResponse({'error': 'Invalid JSON file'}, status=400)

    # Read the CSV file
    try:
        csv_df = pd.read_csv(csv_file)
    except Exception as e:
        return JsonResponse({'error': 'Invalid CSV file'}, status=400)

    # Extract JSON keys and CSV headers
    json_labels = {step['label'] for flow in json_data['flows'] for step in flow['steps']}
    json_options = {option for flow in json_data['flows'] for step in flow['steps'] for option in step['options']}
    all_labels = json_labels.union(json_options)

    # Count occurrences of each label in the CSV
    csv_labels_count = csv_df['Label'].value_counts().to_dict()

    # Check if all JSON labels are in CSV and have at least 10 phrases
    for label in all_labels:
        if csv_labels_count.get(label, 0) < 10:
            return JsonResponse({'error': f'Label {label} has less than 10 phrases in the CSV file'}, status=400)

    # Proceed with saving JSON and CSV data to the database
    try:
        with transaction.atomic():
            flow = cargar_datos_a_bd(json_data, scenario)
            cargar_datos_csv_a_bd(csv_df.to_dict('records'), flow)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Files uploaded and verified successfully'}, status=200)

    
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
        chatbot, flowManager, marker = get_session_objects(request.session)
        if suggestions:
            marker.decrease(0.75)
            response_text = (suggestions)
            set_session_objects(request.session, chatbot, flowManager, marker)
            return Response({'response': response_text,'suggestion':True},status=200)
        if not sentence_checker.is_sentence_coherent(user_message):
            marker.decrease(0.5)
            set_session_objects(request.session, chatbot, flowManager, marker)
            return Response({'response':'La frase no parece ser coherente. Asegúrate de que contenga al menos un sujeto y un verbo, o que sea una frase imperativa.','suggestion':True},status=200)
        bot_response = chatbot.predict_response_with_confidence(user_message)
        if(not bot_response):
            marker.decrease()
            set_session_objects(request.session, chatbot, flowManager, marker)
            return Response({'response': 'Creo que no te entiendo del todo','suggestion':True},status=200)
        if(flowManager.advance(bot_response)):
            response=flowManager.response 
            if random.random() < 0.5:
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
            marker.decrease(0.75)
            set_session_objects(request.session, chatbot, flowManager, marker)
            return Response({'response': "Lo siento, parece que no entendí tu mensaje. Si te encuentras perdido en el flujo, no dudes en usar el botón de ayuda",'suggestion':True},status=200)
        if(response is None):
            return Response({'response': 'El texto que has introducido incoherente con el flujo','suggestion':True},status=200)
        set_session_objects(request.session, chatbot, flowManager, marker)
        return Response({'response': response,'is_finished':flowManager.is_finished(),'mark': marker.mark,'suggestion':False},status=200)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication])
def mascot_message(request):
    chatbot, flowManager, marker = get_session_objects(request.session)
    marker.decrease(0.5)
    suggestion=flowManager.suggest()
    set_session_objects(request.session, chatbot, flowManager, marker)
    return Response({'suggestion': suggestion},status=200)
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
            
            # Añadir conversaciones
            conversations = {}
            for mark in marks:
                chat_conversations = ChatConversation.objects.filter(user=user, date__date=mark.date.date())
                for chat in chat_conversations:
                    conversations[mark.id] = (chat.conversation)
            
            return Response({'user': user_serializer.data, 'marks': marks_serializer.data, 'conversations': conversations}, status=status.HTTP_200_OK)
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
        chatbot, flowManager, marker = get_session_objects(request.session)
        flowManager.reset_flow()
        marker.restart()
        set_session_objects(request.session, chatbot, flowManager, marker)
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
            chatbot, flowManager, marker = get_session_objects(request.session)
            marker.decrease()
            set_session_objects(request.session, chatbot, flowManager, marker)
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
        return Response({'message': 'Los datos introducidos son incorrectos'},status=status.HTTP_400_BAD_REQUEST)
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
        return Response({'message': 'EL flujo se ha eliminado correctamente'}, status=status.HTTP_200_OK)
    except Flow.DoesNotExist:
        return Response({'error': 'No se ha encontrado el flujo'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_flows_by_scenario(request, scenario_name):
    try:
        scenario = Scenery.objects.get(name=scenario_name)
        flows = scenario.flows.all()
        flows_data = [{'id': flow.id, 'name': flow.name} for flow in flows]
        return Response({'flows': flows_data}, status=status.HTTP_200_OK)
    except Scenery.DoesNotExist:
        return Response({'error': 'no se ha encontrado el escenario'}, status=status.HTTP_404_NOT_FOUND)
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
def index(request):
    return render(request, 'index.html')
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication])
@ensure_csrf_cookie
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
        return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
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

class ForumView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, *args, **kwargs):
        messages_ref = db.collection('messages').order_by('timestamp')
        messages = [doc.to_dict() for doc in messages_ref.stream()]
        pinned_message = next((msg for msg in messages if msg.get('isPinned')), None)
        
        return JsonResponse({'messages': messages, 'pinnedMessage': pinned_message})

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        message_id = request.POST.get('id')
        message_content = request.POST.get('message')

        if action == 'send':
            user = self.get_user_from_id(user_id)
            if user:
                message_data = {
                    'message': message_content,
                    'user_id': user.user_id,
                    'username': user.username,
                    'timestamp': firestore.SERVER_TIMESTAMP,
                    'isPinned': False
                }
                db.collection('messages').add(message_data)
                return JsonResponse({'action': 'send'})

        elif action == 'delete':
            db.collection('messages').document(message_id).delete()
            return JsonResponse({'action': 'delete', 'id': message_id})

        elif action == 'edit':
            doc_ref = db.collection('messages').document(message_id)
            doc_ref.update({'message': message_content})
            return JsonResponse({'action': 'edit', 'id': message_id, 'message': message_content})

        elif action == 'pin':
            self.unpin_current_message()
            doc_ref = db.collection('messages').document(message_id)
            doc_ref.update({'isPinned': True})
            return JsonResponse({'action': 'pin', 'message': self.serialize_message(message_id, {'isPinned': True})})

        elif action == 'unpin':
            self.unpin_current_message()
            return JsonResponse({'action': 'unpin'})

    @staticmethod
    def get_user_from_id(user_id):
        try:
            return AppUser.objects.get(user_id=user_id)
        except AppUser.DoesNotExist:
            return None

    @staticmethod
    def serialize_message(doc_id, message_data):
        message_data['id'] = doc_id
        return message_data

    def unpin_current_message(self):
        pinned_messages = db.collection('messages').where('isPinned', '==', True).stream()
        for msg in pinned_messages:
            msg.reference.update({'isPinned': False})