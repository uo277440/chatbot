import json
from myapi.models import Flow,Step

class FlowManager:
    def __init__(self, id):
        self.flow = self.load_flow(id)
        self.id = id
        self.next_options = ["GREETING"]
        self.current_label = None
        self.finished = False
        self.response = None
        

    def load_flow(self, flow_id):
        try:
            flow = Flow.objects.get(id=flow_id)
            steps = Step.objects.filter(flow=flow)
            self.flow = flow
            self.steps = steps
        except Flow.DoesNotExist:
            return None

    def reset_flow(self):
        self.current_label = None
        self.next_options = ["GREETING"]
        self.finished = False
        self.response = None

    def suggest(self):
        for step in self.steps:
            if step.label == self.current_label:
                return step.suggestion
        return 'Start with a greeting message!'

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

    def is_finished(self):
        return self.finished

class Marker:
    def __init__(self):
        self.mark=10
        
    def decrease(self):
        if self.mark > 0:
            self.mark = self.mark -1 
        
    def restart(self):
        self.mark = 10

# Uso del FlowManager
