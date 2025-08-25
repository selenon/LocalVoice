#Library for getting responses from the LLM
import requests
#Library for getting voice feedback from the LLM
import vosk
#Library for getting voice input
import sounddevice as vinput
import queue
import json
import pyttsx3
import os

#Vosk model
model_path = "ENTER_PATH_FOR_VOSK"
if not os.path.exists(model_path):
    raise FileNotFoundError("File not found")

vmodel = vosk.Model(model_path)
#Holds the query from voice input
q = queue.Queue()

#Function to process voice into text
def callback(indata, frames, time, status):
    if status:
        print("Voice error:", status)
    q.put(bytes(indata))

#Function for getting voice input
def listen():
    with vinput.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
        print("Listening")
        rec = vosk.KaldiRecognizer(vmodel, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    return text

#Function get prompts to the LLM
def ask(prompt, model_name="MODEL_NAME"):
    print(f"Prompt: {prompt}")
    try:
        response = requests.post("http://localhost:11434/api/generate", json={"model": model_name, "prompt": prompt, "stream": False}, timeout=60)
        if response.status_code != 200:
            print(f"LLM error [{response.status_code}]: {response.text}")
            return "LLM gave an error."
        
        data = response.json()
        print("LLM's raw answer:", data)

        reply = data.get("response", "").strip()
        if not reply:
            return "LLM couldn't reply."
        print(f"Reply: {reply}")
        return reply

    except requests.exceptions.RequestException as e:
        print("Couldn't reach LLM. Make sure the LLM is active.", e)
        return "Couldn't reach LLM."

#Function to get voice output
def speak(reply):
    engine = pyttsx3.init()
    engine.say(reply)
    engine.runAndWait()

#Main function
if __name__ == "__main__":
    print("LLM ready. (To stop use CRTL+C)")
    try:
        while True:
            voice_input = listen()
            print("User input: ", voice_input)
            reply = ask(voice_input)
            speak(reply)
    except KeyboardInterrupt:
        print("Quitting program...")
