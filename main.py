from handler import Handler
from listener import Listener
from translator import Translator
from voicevox import VoiceVox

INPUT_LANGUAGE = "en-us"
OUTPUT_LANGUAGE = "ja"


if __name__ == "__main__":
    import keyboard
    import json
    import time

    with open("credentials.txt", "r") as infile:
        DEEPL_KEY = infile.readline()

    with open("speakers.json", "rb") as infile:
        speaker_list = [profile for profile in json.loads(infile.readline())["speakers"]]

    stt_engine = Listener(INPUT_LANGUAGE)
    tl_engine = Translator(OUTPUT_LANGUAGE, DEEPL_KEY)
    voicevox_engine = VoiceVox("14", 4.0, 1.5, 1.0, 1.0)

    talk_box = Handler(stt_engine, tl_engine, voicevox_engine)

    running = True

    while running:
        time.sleep(0.1)

        talk_box.update()

        if keyboard.is_pressed("s"):
            talk_box.toggle()
            running = False
            print("stopped")







