import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import string
from sklearn.calibration import CalibratedClassifierCV


class TextTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [self.tokenize_and_lemmatize(text) for text in X]

    def tokenize_and_lemmatize(self, input_text):
        lemmatizer = WordNetLemmatizer()
        # Convertir el texto a minúsculas
        input_text = input_text.lower()
        
        # Eliminar signos de puntuación
        input_text = input_text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenización
        tokens = word_tokenize(input_text)
        
        # Eliminar stopwords
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        # Lematización y búsqueda de sinónimos
        synonyms = set()
        '''
        for word in filtered_tokens:
            word_synonyms = [synset.lemmas()[0].name() for synset in wordnet.synsets(word)]
            synonyms.update(word_synonyms[:3])
        print('Hola') 
        print(synonyms)
        '''
        return ' '.join(lemmatized_tokens)
class SVMChatbot:
    def __init__(self, csv_user_file,confidence_threshold=0.33):
        self.csv_user_file = csv_user_file
        self.text_processor = TextTokenizer()
        self.pipeline = None
        self.confidence_threshold = confidence_threshold
       
        

    def load_data(self):
        # Cargar el archivo CSV
        data = pd.read_csv(self.csv_user_file)
        print(data)
        # Dividir los datos en características (X) y etiquetas (y)
        self.X = data['User Input']
        self.y = data['Label']
        # Dividir los datos en conjuntos de entrenamiento y prueba
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        

    def train_model(self):
        base_classifier = SVC(kernel='linear')
        calibrated_classifier = CalibratedClassifierCV(base_classifier)
        self.pipeline = Pipeline([
            ('tokenizer', TextTokenizer()),  # Tokenización y lematización personalizadas
            ('vectorizer', CountVectorizer()),  # Convertir el texto en vectores de características
            #('classifier', SVC(kernel='linear'))  # Clasificador SVM lineal
            ('classifier', calibrated_classifier)
        ])
        print(self.X)
        self.pipeline.fit(self.X_train,self.y_train)

    def evaluate_model(self):
        # Evaluar el modelo en el conjunto de prueba
        accuracy = self.pipeline.score(self.X_test, self.y_test)
        print("Precisión del modelo en el conjunto de prueba:", accuracy)
    
    def predict_response(self, input_text):
        processed_input_text = (self.text_processor.tokenize_and_lemmatize(input_text))
        predicted_response = self.pipeline.predict([processed_input_text])
        predicted_label = predicted_response[0]
        return predicted_label
    def predict_response_with_confidence(self, input_text):
    # Preprocesar el texto
        processed_input_text = self.text_processor.tokenize_and_lemmatize(input_text)

        # Predecir la etiqueta y obtener las probabilidades
        predicted_label = self.pipeline.predict([processed_input_text])[0]
        probabilities = self.pipeline.predict_proba([processed_input_text])[0]
        predicted_labels = self.pipeline.classes_
        for label, probability in zip(predicted_labels, probabilities):
            print(f"Etiqueta: {label}, Probabilidad: {probability}")

        # Obtener la probabilidad asociada a la etiqueta predicha
        probability = probabilities[self.pipeline.classes_.tolist().index(predicted_label)]

        # Verificar si la confianza supera el umbral
        if probability >= self.confidence_threshold:
            #return predicted_label,probability,probabilities
            return predicted_label
        else:
            #return None,probabilities,predicted_label,probability
            return None
    

# Uso de la clase SVMChatbot
chatbot = SVMChatbot('hotel_usuario.csv')  # Crear una instancia del chatbot
chatbot.load_data()  # Cargar los datos de entrenamiento
chatbot.train_model()  # Entrenar el modelo SVM

input_text = "I like to travel to hotels"
predicted_response = chatbot.predict_response_with_confidence(input_text)
print("Chatbot Response:", predicted_response)

