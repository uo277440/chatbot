import json
from .models import Flow, Step,Scenery

def cargar_datos_a_bd(json_file, scenario_name):
    # Lee el contenido del archivo JSON desde el objeto InMemoryUploadedFile
    json_data = json_file.read().decode('utf-8')

    # Procesa el contenido del archivo JSON y cárgalo en la base de datos
    datos = json.loads(json_data)
    
    # Obtener el escenario o crear uno nuevo si no existe
    scenario,created = Scenery.objects.get_or_create(name=scenario_name)
    
    for flow_data in datos['flows']:
        # Crea el flujo asociado al escenario
        flow = Flow.objects.create(name=flow_data['name'], scenery=scenario)
        for step_data in flow_data['steps']:
            # Crea los pasos dentro del flujo y los asocia con el escenario
            Step.objects.create(
                flow=flow,
                label=step_data['label'],
                message=step_data['message'],
                suggestion=step_data['suggestion'],
                options=step_data['options']
            )
            return flow