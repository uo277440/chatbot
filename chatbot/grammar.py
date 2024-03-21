import requests

def correct_text(text):
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
input_text = "I am an engineer and I love programming."
corrections = correct_text(input_text)
for correction in corrections:
    print("Sugerencia:", correction[2], "En posición:", correction[0])