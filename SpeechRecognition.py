from speech_recognition.exceptions import UnknownValueError
import speech_recognition as sr


def listen() -> str:
    r = sr.Recognizer()

    mic = sr.Microphone()

    with mic as source:
        print("You can now speak")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print("Translating your speech...")

        try:
            # the below runs even with a yellow underline
            txt = r.recognize_google(audio)
            print("Transcript: " + txt)
            return txt
        except Exception:
            print('Input was inaudible to transcript.')
            return '*Inaudible*'



listen()
