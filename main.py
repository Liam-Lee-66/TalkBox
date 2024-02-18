from whisper import transcribe
from listener import record
from collections import deque
from threading import Thread
from time import time


class Handler:
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


if __name__ == "__main__":
    import keyboard

    caption = ""

    primary_engine = Handler("en")
    primary_engine.active = True

    running = True

    main_thread = Thread(target=primary_engine.run)
    try:
        main_thread.start()
        while running:
            if keyboard.is_pressed("s"):
                running = False
                primary_engine.active = False

                if primary_engine.thread.is_alive():
                    primary_engine.thread.join()

                if main_thread.is_alive():
                    main_thread.join()

            caption += primary_engine.dequeue()
    finally:
        print(primary_engine.queue)
        print(caption)
