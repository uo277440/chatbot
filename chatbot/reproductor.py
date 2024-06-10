import pyttsx3

##
# \brief Convierte texto en audio utilizando el motor de síntesis de voz pyttsx3.
#
# Esta función toma un texto y lo convierte en audio, utilizando diferentes configuraciones
# de velocidad y voz según el idioma especificado.
#
# \param text Texto a convertir en audio.
# \param language Idioma de la voz (por defecto 'en' para inglés).
# \param rate Velocidad del habla (por defecto 150 palabras por minuto).
# \return Duración estimada del audio en segundos.
#
def text_to_audio(text, language='en', rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate) 
    if(language == 'en'):
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    else:
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0')
    engine.say(text)
    engine.runAndWait()
    return  (len(text) / rate) * 60

##
# \brief Prueba todas las voces disponibles en el sistema.
#
# Esta función inicializa el motor de síntesis de voz pyttsx3 y recorre todas las voces
# disponibles, pronunciando "Hello World!" en cada una de ellas.
#
def probar_voces():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        engine.setProperty('voice', voice.id)
        engine.say("Hello World!")
        engine.runAndWait()
        engine.stop()




