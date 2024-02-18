from queue import Queue
from threading import Thread, Event
import time
from googletrans import Translator, LANGUAGES


# Assuming integration with an external library for VAD and language detection

class TalkBox:
    """
    TalkBox enables AI-based parsing and translation of system audio to text for real-time caption display.

    This application captures incoming audio from voice or video calls, translates the spoken words into
    the user's preferred language, and displays the text as live captions.

    === Public Attributes ===
    - language (str): The target language for translation.
    - disp_freq (float): The base frequency (in seconds) for displaying
    text captions. Adjusted dynamically based on sentence length.

    === Representation Invariants ===
    - language must be a valid language code as per googletrans.LANGUAGES.
    - disp_freq > 0

    === Private Attributes ===
    - _text_queue (Queue): Manages sentences for display,
    ensuring smooth and timely captions.
    - _translator (Translator): Handles translation of text to the target language.
    - _stop_event (Event): Signals the display thread for graceful shutdown.
    - _display_thread (Thread): Background thread for managing text display.
    """

    def __init__(self, language: str = 'en', disp_freq: float = 2.0) -> None:
        """
        Initializes TalkBox with a target language and display frequency.

        :param language: Target language for translation, default is English ('en').
        :param disp_freq: Base frequency for displaying text captions, in seconds.
        """
        self.language = language
        self.disp_freq = disp_freq
        self._text_queue = Queue()
        self._translator = Translator()
        self._stop_event = Event()

    def _translate_text(self, text: str) -> str:
        """
        Translates the given text to the target language.

        :param text: The text to translate.
        :return: The translated text.
        """
        translated = self._translator.translate(text, dest=self.language)
        return translated.text

    def _text_display_worker(self) -> None:
        """
        Background thread worker for managing the display of text.
        Adjusts display timing based on sentence complexity.
        """
        while not self._stop_event.is_set():
            if not self._text_queue.empty():
                text_to_display = self._text_queue.get()
                # Placeholder for actual UI display logic
                print(f"Displaying: {text_to_display}")
                self._text_queue.task_done()
                # Adjust sleep based on text length for dynamic display timing
                time.sleep(max(self.disp_freq, len(text_to_display) / 100))
            else:
                time.sleep(0.1)  # Prevent busy waiting

    def add_text_for_display(self, text: str) -> None:
        """
        Adds text to the queue for display after translation.

        :param text: The text to be displayed.
        """
        translated_text = self._translate_text(text)
        self._text_queue.put(translated_text)

    def start_displaying(self) -> None:
        """
        Starts the background thread for text display.
        """
        self._stop_event.clear()
        self._display_thread = Thread(target=self._text_display_worker)
        self._display_thread.start()

    def stop_displaying(self) -> None:
        """
        Stops the background thread and waits for it to finish.
        """
        self._stop_event.set()
        self._display_thread.join()

    def update_language(self, new_language: str) -> None:
        """
        Updates the target language for translation.

        :param new_language: The new language code.
        """
        if new_language.lower() in LANGUAGES.values():
            self.language = new_language
        else:
            print(f"{new_language} is not a supported language.")
