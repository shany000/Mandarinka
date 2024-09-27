import io
import browser

import queue
import sounddevice as sd
import vosk


def Mandarinka(model_path):

    model = vosk.Model(model_path)
    audio_queue = queue.Queue()
    sample_rate = 16000

    spoken_text = ""

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        audio_queue.put(bytes(indata))

    with sd.RawInputStream(samplerate=sample_rate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):

        print("Говорите")

        while spoken_text!= "пока":
            recognizer = vosk.KaldiRecognizer(model, sample_rate)
            spoken_text = io.listen_and_recognize(recognizer,audio_queue)
            print(spoken_text)


Mandarinka("models/vosk-model-small-ru-0.22")
