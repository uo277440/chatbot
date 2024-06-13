import json
from .models import Flow, Step,Scenery

def cargar_datos_a_bd(json_data, scenario_name):
    flow=None 
    print('ENTRE AL METODO')
    print(scenario_name)
    scenario,created = Scenery.objects.get_or_create(name=scenario_name)
    print(scenario)
    print(created)
    for flow_data in json_data['flows']:
        # Crea el flujo asociado al escenario
        print(flow_data['description'])
        flow = Flow.objects.create(name=flow_data['name'],description=flow_data['description'], scenery=scenario)
        print('pum')
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