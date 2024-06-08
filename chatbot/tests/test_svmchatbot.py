import pytest
from unittest.mock import patch
from chatbot.svm import SVMChatbot  # Ajusta esto a tu estructura de proyecto
import pandas as pd
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import os

@pytest.fixture
def csv_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'HOTEL.csv')
    with open(csv_path, 'r') as file:
        csv_content = file.read()
    return csv_content

@pytest.fixture
def svm_chatbot(csv_data):
    return SVMChatbot(csv_user_content=csv_data, model_path=None)

def test_train_model_calls_evaluate_model(svm_chatbot):
    with patch.object(SVMChatbot, 'evaluate_model', wraps=svm_chatbot.evaluate_model) as mocked_evaluate:
        svm_chatbot.load_data()
        svm_chatbot.train_model()
        mocked_evaluate.assert_called_once()

def test_accuracy_above_90(svm_chatbot):
    svm_chatbot.load_data()
    svm_chatbot.train_model()
    y_test_encoded = svm_chatbot.label_encoder.transform(svm_chatbot.y_test)
    y_pred = svm_chatbot.pipeline.predict(svm_chatbot.X_test)
    accuracy = accuracy_score(y_test_encoded, y_pred)
    assert accuracy > 0.90, f"Accuracy was below 90%: {accuracy}"

@pytest.fixture
def trained_svm_chatbot(svm_chatbot):
    svm_chatbot.load_data()
    svm_chatbot.train_model()
    return svm_chatbot

def test_predict_response(trained_svm_chatbot):
    response = trained_svm_chatbot.predict_response("Hello")
    assert response is not None

def test_predict_response_with_confidence(trained_svm_chatbot):
    response = trained_svm_chatbot.predict_response_with_confidence("Hello")
    assert response is not None

def test_plot_confusion_matrix(trained_svm_chatbot):
    trained_svm_chatbot.plot_confusion_matrix()
    assert True  # Si no hay excepciones, la prueba pasa

def test_plot_learning_curve(trained_svm_chatbot):
    trained_svm_chatbot.plot_learning_curve()
    assert True  # Si no hay excepciones, la prueba pasa
