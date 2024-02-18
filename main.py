from whisper import transcribe
from listener import record
from collections import deque
from threading import Thread
from time import time


class Scribe:
    """

    """
    queue: deque
    thread: Thread
    recording_interval: time
    language: str
    active: bool

    def __init__(self, language: str) -> None:
        self.queue = deque()
        self.thread = None
        self.recording_interval = 4
        self.language = language
        self.active = False

    def capture(self) -> None:
        # below is sample mp3
        transcribed = transcribe('recorded.wav', self.language)
        for sentence in transcribed.split('.'):
            printing = sentence.strip()

            if len(printing) > 0 and printing[-1] != '.':
                self.queue.append(printing + '.')
            else:
                self.queue.append(printing)

    def run(self) -> None:
        while self.active:
            self.thread = Thread(target=self.capture)
            # records input audio and creates a mp3
            record(self.recording_interval)
            self.thread.start()
        print("services halted.")

    def dequeue(self) -> str:
        if len(self.queue) > 0:
            return self.queue.popleft()
        return ""


class Handler:
    """

    """
    caption: str
    src_language: str
    dst_language: str
    thread: Thread
    scribeEngine: Scribe

    def __init__(self, src_language, dst_language) -> None:
        self.caption = ""
        self.src_language = src_language
        self.dst_language = dst_language
        self.scribeEngine = None
        self.thread = None

    def setup(self):
        self.scribeEngine = Scribe(self.src_language)
        self.scribeEngine.active = True
        self.thread = Thread(target=self.scribeEngine.run)


if __name__ == "__main__":
    import keyboard

    talkBox = Handler("en", "zh")

    running = True

    try:
        talkBox.setup()
        talkBox.thread.start()
        engine = talkBox.scribeEngine
        while running:
            if keyboard.is_pressed("s"):
                running = False
                engine.active = False

                if talkBox.scribeEngine.thread.is_alive():
                    engine.thread.join()

                if talkBox.thread.is_alive():
                    talkBox.thread.join()

            talkBox.caption += engine.dequeue()

    finally:
        print(talkBox.caption)
