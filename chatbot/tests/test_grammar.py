import pytest
from unittest.mock import patch, Mock
import requests
from chatbot.grammar import GrammarCorrector, SentenceChecker  # Ajusta esto a tu estructura de proyecto
##
# \brief Fixture que inicializa una instancia de GrammarCorrector.
#
# \return Instancia de GrammarCorrector.
#
@pytest.fixture
def grammar_corrector():
    return GrammarCorrector()
##
# \brief Fixture que inicializa una instancia de SentenceChecker.
#
# \return Instancia de SentenceChecker.
#
@pytest.fixture
def sentence_checker():
    return SentenceChecker()
##
# \brief Prueba que verifica la función correct_text en caso de éxito.
#
# Utiliza un mock para la respuesta de requests.post y verifica que se retornan las correcciones adecuadas.
#
# \param grammar_corrector Fixture que proporciona una instancia de GrammarCorrector.
#
def test_correct_text_success(grammar_corrector):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'matches': [
            {'offset': 0, 'length': 4, 'message': 'Possible spelling mistake found.'}
        ]
    }

    with patch('requests.post', return_value=mock_response):
        corrections = grammar_corrector.correct_text("Thiss is a test.")
        assert corrections == ["Suggestion: Possible spelling mistake found. In word: Thiss"]

##
# \brief Prueba que verifica la función correct_text en caso de fallo.
#
# Utiliza un mock para la respuesta de requests.post y verifica que se maneja correctamente el error.
#
# \param grammar_corrector Fixture que proporciona una instancia de GrammarCorrector.
#
def test_correct_text_failure(grammar_corrector):
    mock_response = Mock()
    mock_response.status_code = 400

    with patch('requests.post', return_value=mock_response):
        corrections = grammar_corrector.correct_text("Thiss is a test.")
        assert corrections is None
##
# \brief Prueba que verifica la función translate en caso de éxito para traducir a español.
#
# Utiliza un mock para la función GoogleTranslator.translate y verifica que la traducción es correcta.
#
# \param grammar_corrector Fixture que proporciona una instancia de GrammarCorrector.
#
def test_translate_success(grammar_corrector):
    with patch('deep_translator.GoogleTranslator.translate', return_value="Esto es una prueba"):
        translated_text = grammar_corrector.translate("This is a test", "es")
        assert translated_text == "Esto es una prueba"
##
# \brief Prueba que verifica la función translate para traducir de español a inglés.
#
# Utiliza un mock para la función GoogleTranslator.translate y verifica que la traducción es correcta.
#
# \param grammar_corrector Fixture que proporciona una instancia de GrammarCorrector.
#       
def test_translate_spanish_to_english(grammar_corrector):
    with patch('deep_translator.GoogleTranslator.translate', return_value="This is a test"):
        translated_text = grammar_corrector.translate("Esto es una prueba", "en")
        assert translated_text == "This is a test"
##
# \brief Prueba que verifica la función get_synonym_phrase en caso de éxito.
#
# Utiliza un mock para la respuesta de requests.post y verifica que se retorna el sinónimo correcto.
#
# \param grammar_corrector Fixture que proporciona una instancia de GrammarCorrector.
#
def test_get_synonym_phrase_success(grammar_corrector):
    mock_response = Mock()
    mock_response.json.return_value = {
        "choices": [
            {"message": {"content": "A test"}}
        ]
    }

    with patch('requests.post', return_value=mock_response):
        synonym = grammar_corrector.get_synonym_phrase("This is a test")
        assert synonym == "A test"
##
# \brief Prueba que verifica la función get_synonym_phrase en caso de fallo.
#
# Utiliza un mock para la respuesta de requests.post y simula una excepción para verificar el manejo de errores.
#
# \param grammar_corrector Fixture que proporciona una instancia de GrammarCorrector.
#
def test_get_synonym_phrase_failure(grammar_corrector):
    mock_response = Mock()
    mock_response.json.side_effect = Exception("API Error")

    with patch('requests.post', return_value=mock_response):
        synonym = grammar_corrector.get_synonym_phrase("This is a test")
        assert synonym is None
##
# \brief Prueba que verifica la función is_sentence_coherent.
#
# Verifica la coherencia de varias frases utilizando el modelo de lenguaje spaCy.
#
# \param sentence_checker Fixture que proporciona una instancia de SentenceChecker.
#
def test_is_sentence_coherent(sentence_checker):
    assert sentence_checker.is_sentence_coherent("Good morning, how can I help you?")
    assert not sentence_checker.is_sentence_coherent("Test.")
    assert sentence_checker.is_sentence_coherent("Give me your DNI")

