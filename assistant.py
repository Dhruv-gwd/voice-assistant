import speech_recognition as sr
import pyttsx3
import subprocess
import os

#  TEXT TO SPEECH

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


#  SPEECH RECOGNIZER

recognizer = sr.Recognizer()
current_language = "en-IN"    #English only


#  OPEN APPLICATION FUNCTIONS

def open_steam(path):
    try:
        subprocess.Popen([path])
        speak("Opening Steam.")
    except Exception as e:
        speak("Unable to open Steam.")
        print(e)

def open_notepad():
    subprocess.Popen(["notepad.exe"])
    speak("Opening Notepad.")

def open_calculator():
    subprocess.Popen(["calc.exe"])
    speak("Opening Calculator.")


#  LISTEN FUNCTION

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language=current_language)
        print("You said:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""


#  COMMAND HANDLER

def process_command(command):

    # Open apps
    
    if "open steam" in command or "start steam" in command:
        open_steam(r"C:\Program Files (x86)\Steam\steam.exe")
        return

    if "open notepad" in command:
        open_notepad()
        return

    if "open calculator" in command:
        open_calculator()
        return

    # Stop / Exit bot
    
    if "stop" in command or "exit" in command or "bye" in command:
        speak("Goodbye!")
        exit()

    speak("I don't know this command.")


#  START ASSISTANT

speak("Hello, I am your assistant. How can I help you?")

while True:
    command = listen()
    if command:
        process_command(command)
