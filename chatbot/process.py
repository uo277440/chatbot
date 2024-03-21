import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import string

class TextProcessor:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('spanish'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = CountVectorizer()
    
    def process_text(self, input_text):
        # Convertir el texto a minúsculas
        input_text = input_text.lower()
        
        # Eliminar signos de puntuación
        input_text = input_text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenización
        tokens = word_tokenize(input_text)
        
        # Eliminar stopwords
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        
        # Lematización
        lemmatized_tokens = [self.lemmatizer.lemmatize(word) for word in filtered_tokens]

        return lemmatized_tokens

# Ejemplo de uso:
text_processor = TextProcessor()
input_text = "Tenéis algún menú interesante?"
processed_text = text_processor.process_text(input_text)
print(processed_text)