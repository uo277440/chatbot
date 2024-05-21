import csv
import io
from django.http import HttpResponse
from .models import ChatbotData  

def generar_csv_entrenamiento(flow_id):
    chatbot_data = ChatbotData.objects.filter(flow_id=flow_id)

    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)

    csv_writer.writerow(['User Input', 'Label'])

    for data in chatbot_data:
        csv_writer.writerow([data.user_input, data.label])

    csv_content = csv_buffer.getvalue()
    
    csv_buffer.close()

    return csv_content
