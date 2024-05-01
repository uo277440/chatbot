import json
from .models import Flow, Step

def cargar_datos_json_a_bd(json_file):
    # Lee el contenido del archivo JSON desde el objeto InMemoryUploadedFile
    json_data = json_file.read().decode('utf-8')

    # Procesa el contenido del archivo JSON y cárgalo en la base de datos
    datos = json.loads(json_data)
    for flow_data in datos['flows']:
        flow = Flow.objects.create(name=flow_data['name'])
        for step_data in flow_data['steps']:
            Step.objects.create(
                flow=flow,
                label=step_data['label'],
                message=step_data['message'],
                suggestion=step_data['suggestion'],
                options=step_data['options']
            )