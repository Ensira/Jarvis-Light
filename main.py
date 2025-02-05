import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Jarvis hört zu...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="de-DE")
        print(f"Du hast gesagt: {text}")
        return text
    except sr.UnknownValueError:
        print("Jarvis konnte nicht verstehen.")
        return None
    except sr.RequestError:
        print("Jarvis konnte dich nicht verstehen.")
        return None
    
if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if command and "stopp" in command.lower():
            print("Jarvis wird beendet.")
            break
