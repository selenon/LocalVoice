#local LLM modelinden soru sorup cevap almayi sağlayan library
import requests
#LLM'in ses ile cevap vermesini sağlayan library
import vosk
#Kullanicidan ses almayi sağlayan library
import sounddevice as salici
import queue
import json
import pyttsx3
import os

#Vosk modeli
model_path = "vosk_modelleri/modeller"
if not os.path.exists(model_path):
    raise FileNotFoundError("Dosya bulunamadi")

vmodel = vosk.Model(model_path)
#Sesin text halini tutacak queue
q = queue.Queue()

#Sesi processleyecek function
def callback(indata, frames, time, status):
    if status:
        print("Ses hatasi:", status)
    q.put(bytes(indata))

#Mikrofondan ses alacak function
def dinle():
    with salici.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
        print("Dinliyor")
        rec = vosk.KaldiRecognizer(vmodel, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    return text

#local LLM modeline soruyu iletecek function
def sor(prompt, model_name="mistral"):
    print(f"Soru: {prompt}")
    try:
        response = requests.post("http://localhost:11434/api/generate", json={"model": model_name, "prompt": prompt, "stream": False}, timeout=60)
        if response.status_code != 200:
            print(f"LLM hatasi [{response.status_code}]: {response.text}")
            return "LLM hata verdi."
        
        data = response.json()
        print("LLM'in raw cevabi:", data)

        reply = data.get("response", "").strip()
        if not reply:
            return "LLM cevap veremedi."
        print(f"Cevap: {reply}")
        return reply

    except requests.exceptions.RequestException as e:
        print("LLM modeline baglanamadi. LLM modelinin calistigindan emin olun.", e)
        return "LLM modeline baglanamadi."

#Cevabi sesli olarak verecek function
def konus(cevap):
    engine = pyttsx3.init()
    engine.say(cevap)
    engine.runAndWait()

#Main function
if __name__ == "__main__":
    print("LLM hazir. (Durmak için CRTL+C kullanin)")
    try:
        while True:
            ses_input = dinle()
            print("Kullanici input: ", ses_input)
            cevap = sor(ses_input)
            konus(cevap)
    except KeyboardInterrupt:
        print("Program sonlandiriliyor...")
