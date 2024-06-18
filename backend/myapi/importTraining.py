import csv
import io
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatbotData, Flow

def cargar_datos_csv_a_bd(csv_data, flow, batch_size=500):
    chat_data_instances = []

    for row in csv_data:
        user_input = row['User Input']
        label = row['Label']
        chat_data_instances.append(ChatbotData(user_input=user_input, label=label, flow=flow))

        # Insert batch_size number of records at a time
        if len(chat_data_instances) >= batch_size:
            ChatbotData.objects.bulk_create(chat_data_instances)
            chat_data_instances = []

    # Insert any remaining records
    if chat_data_instances:
        ChatbotData.objects.bulk_create(chat_data_instances)
    

