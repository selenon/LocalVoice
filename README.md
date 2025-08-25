# Voice-Assistant-With-Local-LLM
A simple Python project that turns your microphone into a voice interface for a local LLM (e.g. Ollama (https://ollama.ai/)).
# Features
- Voice input with [sounddevice](https://python-sounddevice.readthedocs.io/)  
- Speech-to-text with [Vosk](https://alphacephei.com/vosk/) (offline)  
- Query a local LLM (default: [Ollama Mistral](https://ollama.ai/library/mistral))  
- Voice output with [pyttsx3](https://pyttsx3.readthedocs.io/)  
- Runs fully offline (except LLM, depending on your model)  

You can install dependencies using "pip install -r requirements.txt".
