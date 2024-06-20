import pytest
from unittest.mock import patch, Mock
import pyttsx3
from chatbot.reproductor import text_to_audio, probar_voces  

##
# \brief Prueba que verifica la función text_to_audio para el idioma inglés.
#
# Utiliza un mock para la inicialización de pyttsx3 y verifica que se llamen las funciones correctas con los parámetros adecuados.
#
def test_text_to_audio_english():
    with patch('pyttsx3.init') as mock_init:
        mock_engine = Mock()
        mock_init.return_value = mock_engine

        text = "Hello, this is a test."
        duration = text_to_audio(text, language='en', rate=150)

        mock_engine.setProperty.assert_any_call('rate', 150)
        mock_engine.setProperty.assert_any_call('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')
        mock_engine.say.assert_called_once_with(text)
        mock_engine.runAndWait.assert_called_once()
        
        assert duration == pytest.approx((len(text) / 150) * 60)
##
# \brief Prueba que verifica la función text_to_audio para el idioma español.
#
# Utiliza un mock para la inicialización de pyttsx3 y verifica que se llamen las funciones correctas con los parámetros adecuados.
#
def test_text_to_audio_spanish():
    with patch('pyttsx3.init') as mock_init:
        mock_engine = Mock()
        mock_init.return_value = mock_engine

        text = "Hola, esto es una prueba."
        duration = text_to_audio(text, language='es', rate=150)

        mock_engine.setProperty.assert_any_call('rate', 150)
        mock_engine.setProperty.assert_any_call('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0')
        mock_engine.say.assert_called_once_with(text)
        mock_engine.runAndWait.assert_called_once()
        
        assert duration == pytest.approx((len(text) / 150) * 60)

##
# \brief Prueba que verifica la función probar_voces.
#
# Utiliza un mock para la inicialización de pyttsx3 y verifica que se llamen las funciones correctas para cada voz disponible.
#
def test_probar_voces():
    with patch('pyttsx3.init') as mock_init:
        mock_engine = Mock()
        mock_voice = Mock()
        mock_engine.getProperty.return_value = [mock_voice, mock_voice]
        mock_init.return_value = mock_engine

        probar_voces()

        assert mock_engine.setProperty.call_count == 2
        assert mock_engine.say.call_count == 2
        assert mock_engine.runAndWait.call_count == 2
        assert mock_engine.stop.call_count == 2
