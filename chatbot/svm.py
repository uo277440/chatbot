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
from io import StringIO
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import learning_curve,StratifiedKFold,GridSearchCV
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

##
# \class TextTokenizer
# \brief Transformer personalizado para tokenizar y lematizar texto.
#
# Esta clase convierte el texto de entrada en tokens lematizados, eliminando signos de puntuación y stopwords.
#
class TextTokenizer(BaseEstimator, TransformerMixin):
    ##
    # \brief Constructor de la clase.
    #
    # Inicializa el lematizador de WordNet y las stopwords en inglés.
    #
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    ##
    # \brief Método fit, necesario para cumplir con la API de scikit-learn.
    #
    # \param X Datos de entrada.
    # \param y Etiquetas, por defecto None.
    # \return La instancia de sí mismo.
    #
    def fit(self, X, y=None):
        return self
    
    ##
    # \brief Método transform, aplica la tokenización y lematización al texto de entrada.
    #
    # \param X Lista de textos a procesar.
    # \return Lista de textos procesados.
    #
    def transform(self, X):
        return [self.tokenize_and_lemmatize(text) for text in X]  
    
    ##
    # \brief Método que tokeniza y lematiza un texto de entrada.
    #
    # \param input_text Texto de entrada.
    # \return Texto procesado, tokenizado y lematizado.
    #
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
        # Lematización
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        return ' '.join(lemmatized_tokens)
##
# \class SVMChatbot
# \brief Chatbot basado en SVM que procesa entradas de usuario y genera respuestas.
#
# Esta clase carga datos, entrena un modelo SVM, evalúa el modelo, realiza predicciones y guarda/carga el modelo entrenado.
#
class SVMChatbot:
    ##
    # \brief Constructor de la clase.
    #
    # Inicializa las variables necesarias para el chatbot.
    #
    # \param csv_user_content Contenido CSV con datos de usuario.
    # \param model_path Ruta para guardar/cargar el modelo.
    # \param confidence_threshold Umbral de confianza para las predicciones.
    #
    def __init__(self, csv_user_content,model_path,confidence_threshold=0.10):
        self.csv_user_content = csv_user_content
        self.text_processor = TextTokenizer()
        self.pipeline = None
        self.confidence_threshold = confidence_threshold
        self.label_encoder = LabelEncoder()
        self.model_path = model_path
    ##
    # \brief Guarda el modelo entrenado en la ruta especificada.
    #
    def save_model(self):
        if(self.model_path):
            joblib.dump((self.pipeline, self.label_encoder), self.model_path)  
    ##
    # \brief Carga el modelo entrenado desde la ruta especificada.
    #
    # \return True si el modelo se cargó correctamente, False en caso contrario.
    #
    def load_model(self):
        if self.model_path and os.path.exists(self.model_path):
            print('lo cargo')
            self.pipeline, self.label_encoder = joblib.load(self.model_path)
            return True
        print('no lo cargo')
        return False
    ##
    # \brief Carga los datos desde un archivo CSV y los divide en conjuntos de entrenamiento y prueba.
    #
    def load_data(self):
        # Cargar el archivo CSV
        data = pd.read_csv(StringIO(self.csv_user_content))
        # Dividir los datos en características (X) y etiquetas (y)
        self.X = data['User Input']
        self.y = data['Label']
        # Dividir los datos en conjuntos de entrenamiento y prueba
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42,shuffle=True)
        print("Training set size:", len(self.X_train))
        print("Test set size:", len(self.X_test))
        print("Class distribution in training set:\n", self.y_train.value_counts())
        
    ##
    # \brief Entrena el modelo SVM utilizando GridSearchCV para encontrar el mejor hiperparámetro C.
    #
    def train_model(self):
        param_grid = {'classifier__estimator__C': [0.1, 1, 10]}
        base_classifier = SVC(kernel='linear', C=1.0)
        calibrated_classifier = CalibratedClassifierCV(base_classifier,cv=StratifiedKFold(n_splits=3))
        self.pipeline = Pipeline([
            ('tokenizer', TextTokenizer()),  # Tokenización y lematización personalizadas
            ('vectorizer', TfidfVectorizer()),  # Convertir el texto en vectores de características
            #('classifier', SVC(kernel='linear'))  # Clasificador SVM lineal
            ('classifier', calibrated_classifier)
        ])
        self.y_train_encoded = self.label_encoder.fit_transform(self.y_train)
         # Realizar una búsqueda en cuadrícula para encontrar el mejor valor de C
        grid_search = GridSearchCV(self.pipeline, param_grid, cv=StratifiedKFold(n_splits=3), n_jobs=-1, scoring='accuracy')
        grid_search.fit(self.X_train, self.y_train_encoded)

        # Guardar el mejor modelo encontrado
        self.pipeline = grid_search.best_estimator_
        # Debugging prints
        print("Best C value:", grid_search.best_params_)
        print("Unique labels in training set:", np.unique(self.y_train_encoded))
        print("Training set size after encoding:", len(self.y_train_encoded))
        print('A evaluar el modelo')
        self.evaluate_model()
        self.save_model()
    ##
    # \brief Evalúa el modelo utilizando el conjunto de prueba y muestra el reporte de clasificación.
    #
    def evaluate_model(self):
        y_test_encoded = self.label_encoder.transform(self.y_test)
        y_pred = self.pipeline.predict(self.X_test)
        accuracy = accuracy_score(y_test_encoded, y_pred)
        report = classification_report(y_test_encoded, y_pred, target_names=self.label_encoder.classes_)
        print(f'Accuracy: {accuracy}')
        print(f'Classification Report:\n{report}')
    ##
    # \brief Predice la respuesta del chatbot para un texto de entrada.
    #
    # \param input_text Texto de entrada del usuario.
    # \return Etiqueta predicha por el modelo.
    #
    def predict_response(self, input_text):
        processed_input_text = (self.text_processor.tokenize_and_lemmatize(input_text))
        predicted_response = self.pipeline.predict([processed_input_text])
        predicted_label = predicted_response[0]
        return predicted_label
    
    ##
    # \brief Predice la respuesta del chatbot con un umbral de confianza.
    #
    # \param input_text Texto de entrada del usuario.
    # \return Etiqueta predicha por el modelo si la confianza es suficiente, None en caso contrario.
    #
    def predict_response_with_confidence(self, input_text):
        
    # Preprocesar el texto
        processed_input_text = self.text_processor.tokenize_and_lemmatize(input_text)

        # Predecir la etiqueta y obtener las probabilidades
        predicted_scalar = self.pipeline.predict([processed_input_text])[0]
        probabilities = self.pipeline.predict_proba([processed_input_text])[0]
        predicted_labels = self.pipeline.classes_

        # Obtener la probabilidad asociada a la etiqueta predicha
        
        predicted_label = self.label_encoder.inverse_transform([predicted_scalar])[0]
        probability = probabilities[self.pipeline.classes_.tolist().index(predicted_scalar)]
        print("PROBABILIDAD")
        print(probability)
        if probability >= self.confidence_threshold:
            #return predicted_label,probability,probabilities
            return predicted_label
        else:
            #return None,probabilities,predicted_label,probability
            return None
    
    ##
    # \brief Dibuja la matriz de confusión para el conjunto de prueba.
    #
    def plot_confusion_matrix(self):
        y_test_encoded = self.label_encoder.transform(self.y_test)
        ConfusionMatrixDisplay.from_estimator(self.pipeline, self.X_test, y_test_encoded)
        plt.title("Confusion Matrix")
        plt.show()

    ##
    # \brief Dibuja la curva de aprendizaje del modelo.
    #
    def plot_learning_curve(self):
        """Plot the learning curve for the model."""
        # Ajustar los tamaños de entrenamiento para evitar tamaños demasiado pequeños
        train_sizes = np.linspace(0.2, 1.0, 5) * len(self.X)
        train_sizes = train_sizes[train_sizes <= len(self.X_train)]
        train_sizes = train_sizes.astype(int)

        train_sizes, train_scores, test_scores = learning_curve(
            self.pipeline, self.X, self.label_encoder.transform(self.y), cv=3, n_jobs=-1,
            train_sizes=train_sizes, random_state=42
        )
        
        print("Train sizes:", train_sizes)
        print("Train scores:\n", train_scores)
        print("Test scores:\n", test_scores)

        train_scores_mean = np.mean(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        plt.figure()
        plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label='Training score')
        plt.plot(train_sizes, test_scores_mean, 'o-', color='g', label='Cross-validation score')
        plt.title("Learning Curve")
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        plt.legend(loc="best")
        plt.show()
    def serialize(self):
        return {
            'model_path': self.model_path

        }

    @classmethod
    def deserialize(cls, data):
        instance = cls(None, model_path=data['model_path'])
        instance.load_model()  # Cargar el modelo durante la deserialización
        return instance
    


