from collections import deque
import speech_recognition as sr


class Listener:
    """

    """
    queue: deque
    recognizer: sr.Recognizer
    input_language: str
    interval: float
    active: bool

    def __init__(self, input_language: str) -> None:
        self.queue = deque()
        self.recognizer = sr.Recognizer()
        self.input_language = input_language
        self.active = False

    def run(self) -> None:
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Listening...")

            while self.active:
                try:
                    audio_data = self.recognizer.listen(source, timeout=1)  # Adjust timeout as needed

                    # Perform speech-to-text
                    text = self.recognizer.recognize_google(audio_data)

                    self.queue.append(text)

                except sr.exceptions.WaitTimeoutError:
                    pass

                except sr.UnknownValueError:
                    pass  # Ignore if no speech is detected
                except sr.RequestError as e:
                    print(f"Speech recognition request failed: {e}")

    def dequeue(self) -> str:
        if self.queue:
            return self.queue.popleft()
