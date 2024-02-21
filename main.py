from threading import Thread
from listener import Listener
from translator import Translator
from voicevox import VoiceVox

INPUT_LANGUAGE = "en-us"
OUTPUT_LANGUAGE = "ja"


class Handler:
    """

    """
    listener: Listener
    translator: Translator
    thread: Thread
    translation_history: list[str]

    def __init__(self, listener: Listener, translator: Translator, voicevox: VoiceVox) -> None:
        self.listener = listener
        self.translator = translator
        self.voicevox = voicevox
        self.thread = None
        self.translation_history = []

    def toggle(self) -> None:
        if not self.listener.active:
            self._listener_on()
            self.thread.start()
        else:
            self._listener_off()
            self.thread.join()

    def _listener_on(self) -> None:
        self.listener.active = True

    def _listener_off(self) -> None:
        self.listener.active = False


if __name__ == "__main__":
    import keyboard
    import time

    with open("credentials.txt", "r") as infile:
        DEEPL_KEY = infile.readline()

    stt_engine = Listener(INPUT_LANGUAGE)
    tl_engine = Translator(OUTPUT_LANGUAGE, DEEPL_KEY)
    voicevox_engine = VoiceVox("14", 4.0, 1.5, 1.0, 1.0)

    talk_box = Handler(stt_engine, tl_engine, voicevox_engine)

    talk_box.thread = Thread(target=stt_engine.run)
    running = True

    talk_box.toggle()

    while running:

        if keyboard.is_pressed("s"):
            running = False
            talk_box.toggle()

        time.sleep(0.1)

        transcription = stt_engine.dequeue()

        if transcription:
            print(f"Transcription: {transcription}")
            tl_engine.transcriptions.append(transcription)

        tl_engine.process_transcriptions()

        translation = tl_engine.dequeue()

        if translation:
            print(f"Translation: {translation}")
            voicevox_engine.speak(translation)


