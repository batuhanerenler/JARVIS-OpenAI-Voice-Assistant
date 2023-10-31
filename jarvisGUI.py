import os
import sys
import tempfile
import threading
import queue
import pygame
import gtts
import speech_recognition as sr
from tkinter import Tk, Text, Button, END, Label
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
if not OPENAI_API_KEY:
    print("OpenAI API key not found. Please set it in your environment variables.")
    sys.exit(1)
openai.api_key = OPENAI_API_KEY

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are JARVIS, an AI assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I am experiencing difficulty processing your request at the moment."

def setup_tts():
    pygame.mixer.init()
    return pygame.mixer

def text_to_speech(text, mixer):
    try:
        tts = gtts.gTTS(text, lang="en")
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
            tts.save(fp.name)
            mixer.music.load(fp.name)
            mixer.music.play()
            while mixer.music.get_busy():
                pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def recognize_speech_from_mic(recognizer, microphone):
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "I'm sorry, I didn't catch that."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

def listen_and_respond(mixer, queue, recognizer, microphone, text_widget):
    while True:
        text_widget.insert(END, "\nJARVIS: I'm listening...")
        user_input = recognize_speech_from_mic(recognizer, microphone)
        text_widget.insert(END, f"\nYou: {user_input}")

        if user_input.lower() in ["quit", "exit", "bye"]:
            text_widget.insert(END, "\nJARVIS: Goodbye, Sir. Have a great day ahead.")
            break

        response = generate_response(user_input)
        text_widget.insert(END, f"\nJARVIS: {response}")
        queue.put(response)

def update_speech(queue, mixer):
    while True:
        response = queue.get()
        if response:
            text_to_speech(response, mixer)

def create_gui():
    root = Tk()
    root.title("JARVIS AI Assistant")

    text_widget = Text(root, height=20, width=80)
    text_widget.pack(padx=10, pady=10)
    text_widget.insert(END, "JARVIS: Hello Sir, I am your assistant. How may I assist you today?")

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    mixer = setup_tts()
    response_queue = queue.Queue()

    threading.Thread(target=listen_and_respond, args=(mixer, response_queue, recognizer, microphone, text_widget), daemon=True).start()
    threading.Thread(target=update_speech, args=(response_queue, mixer), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
