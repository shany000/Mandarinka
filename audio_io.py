import pyttsx3


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()


def listen_and_recognize(recognizer, audio_queue):
    while True:
        data = audio_queue.get()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = result.split('"text" : ')[-1].strip('}').replace('"', '').strip()
            if text:
                print(text)
                return text
