from threading import Thread
from listener import Listener
from translator import Translator
from voicevox import VoiceVox


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
            self.thread = Thread(target=self.listener.run)
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