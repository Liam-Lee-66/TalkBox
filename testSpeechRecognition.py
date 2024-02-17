import speech_recognition as sr

r = sr.Recognizer()

micph = sr.Microphone()

with micph as source:
    print("You can now speak")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    print("Translating your speech...")
    # the below runs even with a yellow underline
    print("You said: " + r.recognize_google(audio))

