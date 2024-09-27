import google
import os
import queue
import sounddevice as sd
import vosk

def recognize_speech_vosk():
    model_path = "models/vosk-model-small-ru-0.22"
    if not os.path.exists(model_path):
        print(f"Модель по пути '{model_path}' не найдена.")
        return

    model = vosk.Model(model_path)
    audio_queue = queue.Queue()
    sample_rate = 16000

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        audio_queue.put(bytes(indata))

    with sd.RawInputStream(samplerate=sample_rate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Говорите, я вас слушаю...")

        recognizer = vosk.KaldiRecognizer(model, sample_rate)

        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = result.split('"text" : ')[-1].strip('}').replace('"', '').strip()
                print(f"Вы сказали: {text}")
recognize_speech_vosk()