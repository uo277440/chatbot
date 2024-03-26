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
            return corrections
        else:
            print("Error:", response.status_code)

# Ejemplo de uso
grammar = GrammarCorrector()
input_text = "I am an engineer and I love programming."
corrections = grammar.correct_text(input_text)
for correction in corrections:
    print("Sugerencia:", correction[2], "En posición:", correction[0])