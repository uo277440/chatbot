import json
from myapi.models import Flow,Step
##
# \class FlowManager
# \brief Clase para gestionar los flujos de trabajo.
#
# Esta clase permite cargar, reiniciar y avanzar en un flujo de trabajo, así como sugerir el siguiente paso.
#
class FlowManager:
    ##
    # \brief Constructor de la clase FlowManager.
    #
    # \param id ID del flujo a gestionar.
    #
    def __init__(self, id):
        self.flow = self.load_flow(id)
        self.id = id
        self.next_options = ["GREETING"]
        self.current_label = None
        self.finished = False
        self.response = None
        
        
    ##
    # \brief Carga un flujo de trabajo desde la base de datos.
    #
    # \param flow_id ID del flujo a cargar.
    # \return Objeto Flow cargado o None si no existe.
    #
    def load_flow(self, flow_id):
        try:
            flow = Flow.objects.get(id=flow_id)
            self.description=flow.description
            steps = Step.objects.filter(flow=flow)
            self.flow = flow
            self.steps = steps
        except Flow.DoesNotExist:
            return None
    ##
    # \brief Reinicia el flujo de trabajo a su estado inicial.
    #
    def reset_flow(self):
        self.current_label = None
        self.next_options = ["GREETING"]
        self.finished = False
        self.response = None
    ##
    # \brief Sugiere el siguiente paso en el flujo de trabajo.
    #
    # \return Sugerencia para el siguiente paso.
    #
    def suggest(self):
        for step in self.steps:
            if step.label == self.current_label:
                return step.suggestion
        return 'Start with a greeting message!'
    ##
    # \brief Avanza al siguiente paso en el flujo de trabajo.
    #
    # \param next_label Etiqueta del siguiente paso.
    # \return True si se avanzó correctamente, False en caso contrario.
    #
    def advance(self, next_label):
        if next_label in self.next_options:
            for step in self.steps:
                if step.label == next_label:
                    self.current_label = next_label
                    self.next_options = step.options
                    self.response = step.message
                    if not self.next_options:
                        self.finished = True
                    return True
        return False
    ##
    # \brief Verifica si el flujo de trabajo ha finalizado.
    #
    # \return True si el flujo ha finalizado, False en caso contrario.
    def is_finished(self):
        return self.finished
    ##
    # \brief Serializa el estado actual del flujo de trabajo.
    #
    # \return Diccionario con el estado serializado.
    #
    def serialize(self):
        return {
            'id': self.id,
            'current_label': self.current_label,
            'next_options': self.next_options,
            'finished': self.finished,
            'response': self.response,
        }
    ##
    # \brief Deserializa un flujo de trabajo desde un diccionario de datos.
    #
    # \param data Diccionario con los datos del flujo de trabajo.
    # \return Instancia de FlowManager deserializada.
    #
    @classmethod
    def deserialize(cls, data):
        instance = cls(data['id'])
        instance.current_label = data['current_label']
        instance.next_options = data['next_options']
        instance.finished = data['finished']
        instance.response = data['response']
        instance.load_flow(data['id'])
        return instance
##
# \class Marker
# \brief Clase para gestionar una marca con un valor decreciente.
#
# Esta clase permite disminuir y reiniciar el valor de la marca.
#
class Marker:
    ##
    # \brief Constructor de la clase Marker.
    #
    def __init__(self):
        self.mark=10
    ##
    # \brief Disminuye el valor de la marca en uno.
    #
    def decrease(self):
        if self.mark > 0:
            self.mark = self.mark -1 
    ##
    # \brief Reinicia el valor de la marca a 10.
    #
    def restart(self):
        self.mark = 10
    ##
    # \brief Serializa el estado actual de la marca.
    #
    # \return Diccionario con el estado serializado.
    #
    def serialize(self):
        return {
            'mark': self.mark
        }
    ##
    # \brief Deserializa una marca desde un diccionario de datos.
    #
    # \param data Diccionario con los datos de la marca.
    # \return Instancia de Marker deserializada.
    #
    @classmethod
    def deserialize(cls, data):
        instance = cls()
        instance.mark = data['mark']
        return instance


