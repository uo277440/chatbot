import pytest
from unittest.mock import patch
from chatbot.svm import SVMChatbot  # Ajusta esto a tu estructura de proyecto
import pandas as pd
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
##
# \brief Fixture que carga los datos CSV desde un archivo.
#
# Este fixture lee el contenido del archivo CSV 'HOTEL.csv' ubicado en el directorio 'data'.
#
# \return Contenido del archivo CSV como una cadena de texto.
#
@pytest.fixture
def csv_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'HOTEL.csv')
    with open(csv_path, 'r') as file:
        csv_content = file.read()
    return csv_content
##
# \brief Fixture que inicializa una instancia de SVMChatbot con los datos CSV proporcionados.
#
# \param csv_data Contenido del archivo CSV.
# \return Instancia de SVMChatbot.
#
@pytest.fixture
def svm_chatbot(csv_data):
    return SVMChatbot(csv_user_content=csv_data, model_path=None)
##
# \brief Prueba que verifica si la clase se inicializa correctamente.
#
# 
#
# \param csv_data datos de entrenamiento
#
def test_constructor(csv_data):
    bot = SVMChatbot(csv_user_content=csv_data, model_path="dummy_path")
    assert bot.csv_user_content == csv_data
    assert bot.model_path == "dummy_path"
    assert bot.confidence_threshold == 0.10

##
# \brief Prueba que verifica si el método test_load_data es llamado durante el entrenamiento del modelo.
#
# 
#
# \param svm_chatbot Fixture que proporciona una instancia de SVMChatbot.
#
def test_load_data(svm_chatbot):
    svm_chatbot.load_data()
    assert len(svm_chatbot.X_train) > 0
    assert len(svm_chatbot.X_test) > 0
##
# \brief Prueba que verifica si el método evaluate_model es llamado durante el entrenamiento del modelo.
#
# Utiliza patch.object para envolver el método evaluate_model y verificar que es llamado una vez.
#
# \param svm_chatbot Fixture que proporciona una instancia de SVMChatbot.
#
def test_train_model_calls_evaluate_model(svm_chatbot):
    with patch.object(SVMChatbot, 'evaluate_model', wraps=svm_chatbot.evaluate_model) as mocked_evaluate:
        svm_chatbot.load_data()
        svm_chatbot.train_model()
        mocked_evaluate.assert_called_once()
##
# \brief Prueba que verifica si la precisión del modelo entrenado es superior al 90%.
#
# Carga los datos, entrena el modelo y calcula la precisión sobre el conjunto de prueba.
#
# \param svm_chatbot Fixture que proporciona una instancia de SVMChatbot.
#
def test_accuracy_above_90(svm_chatbot):
    svm_chatbot.load_data()
    svm_chatbot.train_model()
    y_test_encoded = svm_chatbot.label_encoder.transform(svm_chatbot.y_test)
    y_pred = svm_chatbot.pipeline.predict(svm_chatbot.X_test)
    accuracy = accuracy_score(y_test_encoded, y_pred)
    assert accuracy > 0.90, f"Accuracy was below 90%: {accuracy}"
##
# \brief Fixture que proporciona una instancia entrenada de SVMChatbot.
#
# Carga los datos y entrena el modelo antes de devolver la instancia.
#
# \param svm_chatbot Fixture que proporciona una instancia de SVMChatbot.
# \return Instancia entrenada de SVMChatbot.
#
@pytest.fixture
def trained_svm_chatbot(svm_chatbot):
    svm_chatbot.load_data()
    svm_chatbot.train_model()
    return svm_chatbot
##
# \brief Prueba que verifica si el chatbot puede predecir una respuesta para un texto de entrada.
#
# \param trained_svm_chatbot Fixture que proporciona una instancia entrenada de SVMChatbot.
#
def test_predict_response(trained_svm_chatbot):
    response = trained_svm_chatbot.predict_response("Hello")
    assert response is not None
##
# \brief Prueba que verifica si el chatbot puede predecir una respuesta con confianza para un texto de entrada.
#
# \param trained_svm_chatbot Fixture que proporciona una instancia entrenada de SVMChatbot.
#
def test_predict_response_with_confidence(trained_svm_chatbot):
    response = trained_svm_chatbot.predict_response_with_confidence("Hello")
    assert response is not None
##
# \brief Prueba que verifica si la matriz de confusión se puede dibujar sin excepciones.
#
# \param trained_svm_chatbot Fixture que proporciona una instancia entrenada de SVMChatbot.
#
def test_plot_confusion_matrix(trained_svm_chatbot):
    trained_svm_chatbot.plot_confusion_matrix()
    assert True  # Si no hay excepciones, la prueba pasa
##
# \brief Prueba que verifica si la curva de aprendizaje se puede dibujar sin excepciones.
#
# \param trained_svm_chatbot Fixture que proporciona una instancia entrenada de SVMChatbot.
#
def test_plot_learning_curve(trained_svm_chatbot):
    trained_svm_chatbot.plot_learning_curve()
    assert True  # Si no hay excepciones, la prueba pasa
