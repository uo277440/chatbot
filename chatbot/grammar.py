import requests
import spacy
from django.conf import settings
from deep_translator import GoogleTranslator
from openai import OpenAI
from django.conf import settings
import json
class GrammarCorrector:
    SYSTEM_MESSAGE = "You are a helpful assistant that provides synonyms in English."
    API_KEY = settings.OPENAI_API_KEY
    API_URL = 'https://api.openai.com/v1/chat/completions'
    def __init__(self):
        client = OpenAI(
        api_key=settings.OPENAI_API_KEY
        )
        self.client = client
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
                    suggestion_messages.append("Suggestion: "+ correction[2] + " In word: " +word)
                current_offset += len(word) + 1
        return suggestion_messages
    '''
     def translate_to_spanish(self,text,targetLang):
        translator = Translator(to_lang='en')
        translation = translator.translate(text)
        translated_text = translation.text
        return translated_text
    '''
    def translate(self,text, target_language):
        translator = GoogleTranslator(source='auto', target=target_language)
        translated_text = translator.translate(text)
        return translated_text
    def get_synonym_phrase(self,input_text):
        # Construir el cuerpo de la solicitud JSON
        prompt = f"Please provide a synonym for the following phrase: '{input_text}'"
        json_body = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": GrammarCorrector.SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ]
        }

        # Convertir el cuerpo de la solicitud a formato JSON
        json_data = json.dumps(json_body)

        # Configurar las cabeceras de la solicitud
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GrammarCorrector.API_KEY}"
        }

        try:
            # Enviar la solicitud POST y obtener la respuesta
            response = requests.post(GrammarCorrector.API_URL, headers=headers, data=json_data)
            
            # Parsear la respuesta JSON
            json_response = response.json()

            # Extraer el contenido del mensaje
            choices = json_response["choices"]
            content = choices[0]["message"]["content"].strip()
            print("CONTENIDO", content)
            return content
        except Exception as e:
            print(e)
            return None
class SentenceChecker:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def is_sentence_coherent(self, sentence):
        doc = self.nlp(sentence)
        has_subject = False
        has_verb = False
        is_imperative = False 
        for token in doc:
            if token.dep_ in ('nsubj', 'csubj', 'nsubjpass', 'csubjpass'):  
                has_subject = True
            if token.pos_ == 'VERB':  # Verificar si hay un verbo
                has_verb = True
                if token.tag_ == 'VB':
                    is_imperative = True

        # La frase es coherente si tiene al menos un sujeto y un verbo
        return (has_subject and has_verb) or is_imperative

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