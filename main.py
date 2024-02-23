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

    def update(self):
        if not self.listener.active:
            self.thread = Thread(target=stt_engine.run)
            self.toggle()

        transcription = self.listener.dequeue()

        if transcription:
            self.translator.transcriptions.append(transcription)

        self.translator.process_transcriptions()

        translation = self.translator.dequeue()

        if translation:
            print(f"{transcription} -> {translation}")
            self.toggle()
            self.voicevox.speak(translation)

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
    voicevox_engine = VoiceVox("17", 4.0, 1.5, 1.0, 1.0)

    talk_box = Handler(stt_engine, tl_engine, voicevox_engine)

    running = True

    while running:
        time.sleep(0.1)

        talk_box.update()

        if keyboard.is_pressed("s"):
            print("stopped")
            running = False
            talk_box.toggle()





