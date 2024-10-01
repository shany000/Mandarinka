import audio_io
import browser
import file_utils

import sys
import queue
import sounddevice as sd
import vosk
import ctypes


def run_as_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return True
    except Exception as e:
        print(f"Ошибка при запросе прав администратора: {e}")
        return False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def mandarinka(model_path):

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

        audio_io.speak("Говорите")

        recognizer = vosk.KaldiRecognizer(model, sample_rate)
        while spoken_text != "пока":
            spoken_text = audio_io.listen_and_recognize(recognizer,audio_queue)
            if "открыть" in spoken_text or "открой" in spoken_text:
                if "браузер" in spoken_text:
                    audio_io.speak("Что вам открыть?")
                    browser.search(audio_io.listen_and_recognize(recognizer, audio_queue))
                elif "файл" in spoken_text:
                    audio_io.speak("Какой ключ к файлу?")
                    file_utils.open_file_by_key(audio_io.listen_and_recognize(recognizer, audio_queue))
            elif "добавь" in spoken_text:
                audio_io.speak("Какое слово будет ключом?")
                keys = []
                while True:
                    keys.append(audio_io.listen_and_recognize(recognizer, audio_queue))
                    audio_io.speak("Хотите добавить еще?")
                    spoken_text = audio_io.listen_and_recognize(recognizer, audio_queue)
                    if "да" in spoken_text:
                        audio_io.speak("Назовите слово")
                        keys.append(audio_io.listen_and_recognize(recognizer, audio_queue))
                    elif "нет" in spoken_text:
                        break
                audio_io.speak("Напишите полный путь к файлу")
                path = input("Полный путь к файлу: ")
                file_utils.add_shortcuts(keys,path)
                audio_io.speak("Я добавила")
            print("Спасибо за обращение)")


if is_admin():
    mandarinka("models/vosk-model-small-ru-0.22")
else:
    print("Программа требует прав администратора. Перезапуск...")
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except Exception as e:
        print(f"Не удалось перезапустить программу с правами администратора: {e}")
