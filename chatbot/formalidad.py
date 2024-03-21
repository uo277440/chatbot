import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy

class TextFormalityAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.nlp = spacy.load("en_core_web_sm")

    def analyze_formality(self, text):
        # Calcular el puntaje de sentimiento
        sentiment_score = self.sentiment_analyzer.polarity_scores(text)["compound"]
        
        # Analizar la sintaxis y las entidades nombradas con spaCy
        doc = self.nlp(text)
        entity_count = len(doc.ents)
        average_token_length = sum(len(token.text) for token in doc) / len(doc)
        
        # Calcular un puntaje de formalidad basado en las métricas anteriores
        formality_score = (sentiment_score + (entity_count * 0.5)) / (average_token_length * 0.1)
        
        return formality_score

# Ejemplo de uso
analyzer = TextFormalityAnalyzer()
text = "Fuck you."
formality_score = analyzer.analyze_formality(text)
print("Formality Score:", formality_score)