import requests
class GrammarCorrector:
    def correct_text(self,text):
        url = 'https://languagetool.org/api/v2/check'
        params = {'text': text, 'language': 'en-US'}
        response = requests.post(url, data=params)
        if response.status_code == 200:
            data = response.json()
            corrections = []
            for match in data['matches']:
                corrections.append((match['offset'], match['length'], match['message']))
            return self.messaje(corrections,text)
        else:
            print("Error:", response.status_code)
    def messaje(self,corrections,text):
        suggestion_messages = []
        for correction in corrections:
            #print("Sugerencia:", correction[2], "En posición:", correction[0])
            error_offset = correction[0]
            words = text.split()
            current_offset = 0
            for word in words:
                if current_offset <= error_offset < current_offset + len(word):
                    suggestion_messages.append("Sugerencia:"+ correction[2] + " En la palabra:" +word)
                current_offset += len(word) + 1
        return suggestion_messages

# Ejemplo de uso
'''
grammar = GrammarCorrector()
input_text = "Welcome to our hotel how may I help you today?"
for suggestion in grammar.correct_text(input_text):
    print(suggestion)
#print(grammar.correct_text(input_text))
'''
'''
print(corrections)
for correction in corrections:
    print("Sugerencia:", correction[2], "En posición:", correction[0])
    # Obtener la palabra en la posición del error
    error_offset = correction[0]
    words = input_text.split()  # Dividir el texto en palabras
    word_index = 0
    current_offset = 0
    for word in words:
        if current_offset <= error_offset < current_offset + len(word):
            print("Palabra en la posición del error:", word)
            break
        current_offset += len(word) + 1  # Sumar 1 para contar el espacio después de cada palabra
        '''