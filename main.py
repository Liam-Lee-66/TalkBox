from collections import deque
from threading import Thread
from listener import Listener
from translator import Translator

INPUT_LANGUAGE = "en"
OUTPUT_LANGUAGE = "ja"
RECORDING_SECONDS = 5
AUDIO_FILENAME = "input.wav"


class Handler:
    """

    """
    listener: Listener
    queue: deque
    thread: Thread
    translation_history: list[str]

    def __init__(self, listener: Listener) -> None:
        self.listener = listener
        self.queue = deque()
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
        self.listener.thread = None

    def _listener_off(self) -> None:
        self.listener.active = False
        if self.listener.thread.is_alive():
            self.listener.thread.join()


if __name__ == "__main__":
    import keyboard

    with open("credentials.txt", "r") as infile:
        DEEPL_KEY, OPENAI_KEY = infile.readlines()

    stt_engine = Listener(INPUT_LANGUAGE, OUTPUT_LANGUAGE, RECORDING_SECONDS, AUDIO_FILENAME)
    tl_engine = Translator(DEEPL_KEY, OPENAI_KEY)
    talk_box = Handler(stt_engine)

    talk_box.thread = Thread(target=stt_engine.run)
    running = True

    talk_box.toggle()

    while running:
        phrase = stt_engine.dequeue()

        if phrase:
            print(phrase)
            talk_box.queue.append(phrase)

        if keyboard.is_pressed("s"):
            running = False
            talk_box.toggle()
