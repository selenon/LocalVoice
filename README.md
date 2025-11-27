# LocalVoice

A Python voice interface for local language models. Speak to your LLM and get spoken responses without relying on cloud services.

## What it does

LocalVoice turns your microphone into a voice interface for locally running language models. It captures your speech, converts it to text, sends it to your LLM, and speaks the response back to you.

## What you'll need

- Python 3.8 or newer
- Ollama running locally (default port 11434)
- A Vosk speech recognition model (download and extract to your system)
- Microphone and speakers

## How it works

1. **Listen** - Captures audio from your microphone using sounddevice
2. **Transcribe** - Converts speech to text using Vosk (works offline)
3. **Process** - Sends text to your local LLM (default: Ollama with Mistral)
4. **Speak** - Converts the LLM's response to speech using pyttsx3

The entire pipeline runs offline except for the LLM processing, which depends on whether you're using a local or remote model.

## Getting started

Install the requirements:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running on your system and you've downloaded a Vosk model. The code is set up to use Mistral by default, but you can modify it to work with any model supported by Ollama.

