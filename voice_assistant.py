
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
from ai_engine import ask_ai

from automation import open_application, take_screenshot


class VoiceAssistant:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 170)
        self.engine.setProperty("volume", 1.0)

    def speak(self, text):
        print("Abhinav AI:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):

        try:
            print("\nAbhinav AI is listening...")
            print("Speak your English command now...")

            audio = sd.rec(
                int(5 * 16000),
                samplerate=16000,
                channels=1,
                dtype="float32"
            )

            sd.wait()

            audio = np.squeeze(audio)
            audio = (audio * 32767).astype(np.int16)

            audio_bytes = audio.tobytes()

            recorded_audio = sr.AudioData(
                audio_bytes,
                16000,
                2
            )

            command = self.recognizer.recognize_google(
                recorded_audio,
                language="en-US"
            )

            print("You:", command)

            return command.lower()

        except sr.UnknownValueError:
            print("Voice not understood.")
            return ""

        except sr.RequestError:
            self.speak("Speech recognition service is unavailable.")
            return ""

        except Exception as e:
            print("Microphone Error:", e)
            return ""

    def execute_command(self, command):

        if "notepad" in command:
            return open_application("notepad")

        elif "calculator" in command:
            return open_application("calculator")

        elif "chrome" in command:
            return open_application("chrome")

        elif "youtube" in command:
            return open_application("youtube")

        elif "google" in command:
            return open_application("google")

        elif "screenshot" in command:
            return take_screenshot()

        elif "exit" in command or "stop assistant" in command:
            return "EXIT"

        else:
            return ask_ai(command)


if __name__ == "__main__":

    assistant = VoiceAssistant()

    assistant.speak(
        "Hello! I am Abhinav AI. Your personal assistant is ready."
    )

    while True:

        command = assistant.listen()

        if not command:
            continue

        response = assistant.execute_command(command)

        if response == "EXIT":
            assistant.speak("Goodbye! Shutting down.")
            break

        assistant.speak(response)
