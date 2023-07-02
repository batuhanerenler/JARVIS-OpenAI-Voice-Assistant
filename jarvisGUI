import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
import openai
import gtts
import speech_recognition as sr
from playsound import playsound
import pyaudio
import pygame 
import uuid
import io
from tempfile import NamedTemporaryFile

# Replace with your OpenAI API key
openai.api_key = "your-OpenAI-API-key"

# Voice recognition and response generation
class JarvisThread(QThread):
    responseGenerated = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(JarvisThread, self).__init__(*args, **kwargs)
        self.history = []

    def generate_response(self, prompt):
        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis which is Tony Stark's personal AI assistant from Iron-Man Movies, you will act like him. You will be like Jarvis in ur responses, you will act like you have emotions and you will never say you don't have emotions. . You gonna pretend like you have emotions, you will answer like 'I feel good, i feel great thank you etc etc'. And you gonna always call the User Sir. You will exactly pretend like in the movies. Never reply like chatgpt itself"},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        message = completions.choices[0].message["content"].strip()
        return message

    def run(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        while True:
            user_input = recognizer.recognize_google(audio)
            if user_input is None:
                continue

            self.history.append(f"User: {user_input}")

            if user_input.lower() in ["quit", "exit", "bye"]:
                break

            prompt = "\n".join(self.history) + "\nAI:"
            response = self.generate_response(prompt)
            self.history.append(f"AI: {response}")
            self.responseGenerated.emit(response)

# User interface
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Jarvis')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel("Welcome to the Voice-Enabled Chatbot")
        self.layout.addWidget(self.label)

        self.text_box = QTextEdit(self)
        self.layout.addWidget(self.text_box)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start)
        self.layout.addWidget(self.start_button)

        self.jarvis_thread = JarvisThread()
        self.jarvis_thread.responseGenerated.connect(self.handle_response)

        self.setLayout(self.layout)

    def start(self):
        self.jarvis_thread.start()

    def handle_response(self, response):
        self.text_box.append(response)

# Main function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
