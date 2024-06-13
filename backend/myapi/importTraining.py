import csv
import io
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatbotData, Flow

def cargar_datos_csv_a_bd(csv_reader, flow):
    print(csv_reader)
    for row in csv_reader:
        user_input = row['User Input']
        label = row['Label']
        training=ChatbotData.objects.create(user_input=user_input, label=label, flow=flow)
    

