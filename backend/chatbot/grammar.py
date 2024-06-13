import requests
import spacy
from django.conf import settings
from deep_translator import GoogleTranslator
from openai import OpenAI
from django.conf import settings
import json
##
# \class GrammarCorrector
# \brief Clase para corregir la gramática de un texto, proporcionar sinónimos y traducciones.
#
class GrammarCorrector:
    SYSTEM_MESSAGE = "You are a helpful assistant that provides synonyms in English. Only provide the synonym phrase without any introductions or explanations."
    API_KEY = settings.OPENAI_API_KEY
    API_URL = 'https://api.openai.com/v1/chat/completions'
    ##
    # \brief Constructor de la clase GrammarCorrector.
    #
    # Inicializa el cliente de OpenAI con la clave API proporcionada.
    #
    def __init__(self):
        client = OpenAI(
        api_key=settings.OPENAI_API_KEY
        )
        self.client = client
    ##
    # \brief Corrige el texto dado utilizando la API de LanguageTool.
    #
    # \param text Texto a corregir.
    # \return Lista de correcciones sugeridas.
    #
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
    ##
    # \brief Genera un mensaje de corrección basado en las sugerencias proporcionadas.
    #
    # \param corrections Lista de correcciones sugeridas.
    # \param text Texto original.
    # \return Lista de mensajes de sugerencia.
    #
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
    ##
    # \brief Traduce el texto dado al idioma especificado.
    #
    # \param text Texto a traducir.
    # \param target_language Idioma objetivo para la traducción.
    # \return Texto traducido.
    #
    def translate(self,text, target_language):
        translator = GoogleTranslator(source='auto', target=target_language)
        translated_text = translator.translate(text)
        return translated_text
    ##
    # \brief Proporciona un sinónimo para la frase dada utilizando la API de OpenAI.
    #
    # \param input_text Texto de entrada para el cual se necesita un sinónimo.
    # \return Frase sinónima.
    #
    def get_synonym_phrase(self,input_text):
        # Construir el cuerpo de la solicitud JSON
        prompt = f"Provide a synonym for the following phrase: '{input_text}'"
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
##
# \class SentenceChecker
# \brief Clase para verificar la coherencia de una frase.
#
class SentenceChecker:
    ##
    # \brief Constructor de la clase SentenceChecker.
    #
    # Inicializa el modelo de lenguaje spaCy.
    #
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
    
    ##
    # \brief Verifica si una frase es coherente.
    #
    # La frase es coherente si tiene al menos un sujeto y un verbo, o si es imperativa.
    #
    # \param sentence Frase a verificar.
    # \return True si la frase es coherente, False en caso contrario.
    #
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

        # La frase es coherente si tiene al menos un sujeto y un verbo o es imperativa
        return (has_subject and has_verb) or is_imperative

