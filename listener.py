import sounddevice
from whisper import transcribe
from collections import deque
from scipy.io.wavfile import write
from threading import Thread


class Listener:
    """

    """
    queue: deque
    thread: Thread
    input_language: str
    output_language: str
    interval: float
    filename: str
    active: bool

    def __init__(self, input_language: str, output_language: str, interval: float, filename: str) -> None:
        self.queue = deque()
        self.thread = None
        self.input_language = input_language
        self.output_language = output_language
        self.interval = interval
        self.filename = filename
        self.active = False

    def _record(self) -> None:
        fs = 44100

        print("Recording.....\n")

        record_voice = sounddevice.rec(int(self.interval * fs), samplerate=fs, channels=2)
        thread = Thread(target=write, args=[self.filename, fs, record_voice])
        sounddevice.wait()

        thread.start()

        print("Stopped Recording.")

    def _capture(self) -> None:
        transcribed = transcribe(self.filename, self.input_language, self.interval)
        if transcribed:
            self.queue.append(transcribed)

    def run(self) -> None:
        while self.active:
            self.thread = Thread(target=self._capture)
            self._record()
            self.thread.start()

    def dequeue(self) -> str:
        if len(self.queue) > 0:
            return self.queue.popleft()
