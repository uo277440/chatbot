import pyttsx3

def text_to_audio(text, language='en', rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate) 
    engine.setProperty('voice', f'{language}')
    engine.say(text)
    engine.runAndWait()



