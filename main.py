import speech_recognition as sr # type: ignore
import webbrowser
import subprocess
import datetime
import urllib.parse
import whisper

import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
openai.api_key = OPENAI_API_KEY

def chat_with_gpt(prompt):
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model = "gpt-4o",
            messages =[{"role":"user","content":prompt}]
        )
        answer = response["chhoices"][0]["message"]["content"]
        return answer
    except Exception as e:
        return f"Fehler bei der Kommunikation mit ChatGPT: {e}"
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Jarvis hört zu...")
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True

        recognizer.pause_threshold = 1.0
        recognizer.operation_timeout = 5

        audio = recognizer.listen(source)
    try:
        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
            text = recognizer.recognize_google(audio, language="de-DE")
        print(f"Du hast gesagt: {text}")
        return text
    except sr.UnknownValueError:
        print("Jarvis konnte nicht verstehen.")
        return None
    except sr.RequestError:
        print("Jarvis konnte dich nicht verstehen.")
        return None

def execute_command(command):
    if "öffne google" in command:
        print("Öffne Google...")
        webbrowser.open("https://www.google.com")
    elif "suche nach" in command:
        search_query = command.replace("suche nach", "").strip()
        if search_query:
            encoded_query = urllib.parse.quote(search_query)
            print(f"Suche nach {search_query} auf Google...")
            webbrowser.open(f"https://google.com/search?q={encoded_query}") 
    elif "suche auf wikipedia nach" in command:
        wiki_query = command.replace("suche auf Wikipedia nach", "").strip()
        if wiki_query:
            encoded_query=urllib.parse.quote(wiki_query)
            print(f"Suche nach {wiki_query} auf Wikipedia...")
            webbrowser.open(f"https://de.wikipedia.org/wiki/{encoded_query}")
    elif "öffne rechner" in command:
        print("Öffne den Taschenrechner...")
        subprocess.run("calc")
    elif "wie spät ist es" in command or "uhrzeit" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        print(f"Die aktuelle Uhrzeit ist {now}")
    elif "frage chatgpt" in command:
        user_question = command.replace("frage chatgpt", "").strip()
        if user_question:
            print("Sende Anfrage an ChatGPT...")
            response = chat_with_gpt(user_question)
            print(f"ChatGPT: {response}")
    elif "stopp" in command.lower():
        print("Jarvis wird beendet.")
        return False
    return True

def wait_for_hotword():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sag 'Hey Jarvis', um den Assistenten zu starten...")

        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True

        recognizer.pause_threshold = 1.0
        recognizer.operation_timeout = 5
        while True:
            print("Warte auf Aktivierungswort...")
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language="de-DE")
                print(f"Erkannt: {text}")

                if "hey jarvis" in text.lower():
                    print("Hey Jarvis erkannt! Starte Assistenten...")
                    break
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Fehler bei der Spracherkennung.")
                pass


if __name__ == "__main__":
    wait_for_hotword()

    while True:
        command = recognize_speech()
        if command:
            if not execute_command(command):
                break
