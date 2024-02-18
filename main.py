from whisper import transcribe
from listener import record
from translator import translate
from collections import deque
from threading import Thread
from tts import text_to_speech
from time import time


RECORDING_SECONDS = 5

_language_to_whisper_code = {
    'Arabic': 'ar',
    'Bulgarian': 'bg',
    'Czech': 'cs',
    'Danish': 'da',
    'German': 'de',
    'Greek': 'el',
    'English': 'en',
    'Spanish': 'es',
    'Estonian': 'et',
    'Finnish': 'fi',
    'French': 'fr',
    'Hungarian': 'hu',
    'Indonesian': 'id',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Lithuanian': 'lt',
    'Latvian': 'lv',
    'Dutch': 'nl',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Chinese (simplified)': 'zh'
}
_language_to_dl_code = {
    'Arabic': 'AR',
    'Bulgarian': 'BG',
    'Czech': 'CS',
    'Danish': 'DA',
    'German': 'DE',
    'Greek': 'EL',
    'English': 'EN-US',
    'Spanish': 'ES',
    'Estonian': 'ET',
    'Finnish': 'FI',
    'French': 'FR',
    'Hungarian': 'HU',
    'Indonesian': 'ID',
    'Italian': 'IT',
    'Japanese': 'JA',
    'Korean': 'KO',
    'Lithuanian': 'LT',
    'Latvian': 'LV',
    'Norwegian (Bokmål)': 'NB',
    'Dutch': 'NL',
    'Polish': 'PL',
    'Portuguese': 'PT',
    'Romanian': 'RO',
    'Russian': 'RU',
    'Slovak': 'SK',
    'Slovenian': 'SL',
    'Swedish': 'SV',
    'Turkish': 'TR',
    'Ukrainian': 'UK',
    'Chinese (simplified)': 'ZH'
}


def _split_for(input_: str, look_for: list[str]) -> list[str]:
    returning = []
    tracking = 0

    for i in range(len(input_)):
        if input_[i] in look_for:
            returning.append(input_[tracking:i + 1])
            tracking = i + 2

    if tracking < len(input_):
        returning.append(input_[tracking:len(input_)])
    return returning


class Scribe:
    """

    """
    queue: deque
    thread: Thread
    recording_interval: time
    input_language: str
    output_language: str
    active: bool

    def __init__(self, input_language: str, output_language: str) -> None:
        self.queue = deque()
        self.thread = None
        self.recording_interval = RECORDING_SECONDS
        self.input_language = input_language
        self.output_language = output_language
        self.active = False

    def _capture(self) -> None:
        transcribed = transcribe('recorded.wav', self.input_language)
        if transcribed:
            phrases = _split_for(transcribed, ['.', '?', '!'])

            for phrase in phrases:
                self.queue.append(translate(phrase, self.output_language))

    def run(self) -> None:
        while self.active:
            self.thread = Thread(target=self._capture)
            # records input audio and creates a mp3
            record(self.recording_interval)
            self.thread.start()
        print("services halted.")

    def dequeue(self) -> str:
        if len(self.queue) > 0:
            return self.queue.popleft()


class Handler:
    """

    """
    translated_lst: list[str]
    input_language: str
    output_language: str
    thread: Thread
    scribeEngine: Scribe

    def __init__(self, input_language, output_language) -> None:
        self.translated_lst = []
        self.input_language = input_language
        self.output_language = output_language
        self.scribeEngine = None
        self.thread = None

    def setup(self):
        self.scribeEngine = Scribe(self.input_language, self.output_language)
        self.scribeEngine.active = True
        self.thread = Thread(target=self.scribeEngine.run)


if __name__ == "__main__":
    import keyboard

    talkBox = Handler("hi", "EN-US")

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

            sentence = engine.dequeue()

            if sentence:
                print(f"{sentence}")

    finally:
        print(talkBox.translated_lst)
