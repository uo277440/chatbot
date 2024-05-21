import csv
import io
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatbotData, Flow

def cargar_datos_csv_a_bd(csv_file, flow_id):
    # Lee el contenido del archivo CSV desde el objeto InMemoryUploadedFile
    csv_data = io.StringIO(csv_file.read().decode('utf-8'))

    # Obtener el flujo o lanzar una excepción si no existe
    try:
        flow = Flow.objects.get(id=flow_id)
    except ObjectDoesNotExist:
        raise ValueError("El flujo especificado no existe.")

    # Leer el archivo CSV e insertar los datos en la base de datos
    reader = csv.DictReader(csv_data)
    for row in reader:
        user_input = row['User Input']
        label = row['Label']
        ChatbotData.objects.create(user_input=user_input, label=label, flow=flow)

    

