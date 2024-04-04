import json

class FlowManager:
    def __init__(self, json_file, flow_name):
        self.flow = self.load_flow(json_file, flow_name) 
        self.next_options = ["GREETING"]
        self.current_label=None
        self.finished = False
        self.response = None

    def load_flow(self, json_file, flow_name):
        with open(json_file, 'r') as file:
            flows_data = json.load(file)
        flows = flows_data.get('flows', [])
        for flow in flows:
            if flow.get('name') == flow_name:
                return flow
        return None
    def reset_flow(self):
        self.current_label = None
        self.next_options = ["GREETING"]
        self.finished = False
        self.response = None
        
    def suggest(self):
        for step in self.flow.get('steps', []):
                if step['label'] == self.current_label:
                    return step['suggestion']
        return 'Start with a greeting message!'

    def advance(self, next_label):
        if next_label in self.next_options:
            for step in self.flow.get('steps', []):
                if step['label'] == next_label:
                    self.current_label = next_label
                    self.next_options = step.get('options', [])
                    self.response = step['message']
                    if not self.next_options:
                        self.finished=True
                        print("FLUJO TERMINADO")
                    return True
        return False

# Uso del FlowManager
flow_manager = FlowManager('hotel_flujos.json', 'RESERVATION_FLOW')
print(flow_manager.advance("GREETING"))
print(flow_manager.advance("CHECK_AVAILABILITYd"))
print(flow_manager.next_options)
print(flow_manager.advance("CHECK_AVAILABILITY"))
print(flow_manager.next_options)
print(flow_manager.advance("TAKE_DETAILS"))
print(flow_manager.next_options)
print(flow_manager.advance("CONFIRM_RESERVATION"))
print(flow_manager.advance("ASK_QUESTION"))
print(flow_manager.next_options)
print(flow_manager.advance("FAREWELL"))