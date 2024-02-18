from threading import Thread, Event
import time
from queue import SimpleQueue

class Portal:
    """
    Portal interfaces with a backend and user interface for audio processing
    and language translation, facilitating real-time captioning
    for live audio inputs.

    It converts speech to text and displays it in the user's preferred language,
    acting as a bridge between complex audio processing operations
    and user interactions.

    === Public Attributes ===
    input_language (str): The language of the incoming audio.
                          Can be read directly by the backend.
    output_language (str): The target language for displaying captions.
                           Can be read directly by the backend.
    disp_freq: The frequency, in seconds, at which text captions are updated
               and displayed.

    === Representation Invariants ===
    - disp_freq > 0:
        - The display frequency must be positive,
          ensuring a meaningful interval between displaying text captions.

    === Private Attributes ===
    _text_queue: Manages sentences for display, ensuring smooth and
                 timely captions.
    _stop_event: Signals the display thread for graceful shutdown.
    _display_thread: Background thread managing the display of text captions.

    === Methods for Backend Communication ===
    - Backend can directly read `input_language` and `output_language`
      to understand the current language settings.
    - Backend can call `update_text(text: str)`
      to push new strings for display,
      which are then queued for captioning on the UI.

    === Methods for Frontend (UI) Communication ===
    - The UI can instantiate a Portal object,
      optionally specifying default values for `input_language`,
      `output_language`, and `disp_freq`
      to customize the captioning experience.
    - UI can use `change_input_language(language: str)` and
      `change_output_language(language: str)` to dynamically adjust
      language settings based on user preferences on requirements.
    - UI can invoke `stop_displaying()` to gracefully terminate
      the caption display process, useful for stopping captioning
      on user command or when the application is being closed.

    Note: The instantiation of the Portal object by the UI,
          and subsequent adjustments to language settings or display frequency,
          allows for a flexible and user-driven captioning experience.
          These interactions ensure that the Portal can adapt to
          various user needs and preferences, from language selection
          to the pacing of caption display.
    """
    input_language: str
    output_language: str
    disp_freq: float
    _text_queue: SimpleQueue
    _stop_event_: Event
    _display_thread: Thread

    def __init__(self, input_language: str = 'English',
                 output_language: str = 'English',
                 disp_freq: float = 2.0) -> None:
        """
        Initializes the TalkBox with default languages and display frequency.

        :param input_language: Language of the incoming audio,
                               default is English.
        :param output_language: Target language for captions,
                                default is English.
        :param disp_freq: Frequency at which captions are updated/displayed,
                          in seconds.
        :return: None
        """
        self.input_language = input_language
        self.output_language = output_language
        self.disp_freq = disp_freq

        self._text_queue = SimpleQueue()
        self._stop_event = Event()
        self._display_thread = Thread(target=self._text_display_worker)
        self._display_thread.start()

    def _text_display_worker(self) -> None:
        """
        Continuously checks the queue for new text to display
        at specified intervals.

        :return: None
        """
        # Infinitely loop to update the text to display every 100ms.
        while not self._stop_event.is_set():
            if not self._text_queue.is_empty():
                text_to_display = self._text_queue.dequeue()
                # Placeholder for actual display logic from UI
                print(f"Displaying: {text_to_display}")
                time.sleep(self.disp_freq)
            else:
                time.sleep(0.1)  # Do this check every 100ms

    def update_text(self, text: str) -> None:
        """
        Updates the queue with new text from the backend.

        :param text: New text to be displayed.
        :return: None
        """
        self._text_queue.enqueue(text)

    def change_input_language(self, language: str) -> None:
        """
        Updates the input language.

        :param language: The new input language.
        :return: None
        """
        self.input_language = language

    def change_output_language(self, language: str) -> None:
        """
        Updates the output language.

        :param language: The new output language.
        :return: None
        """
        self.output_language = language

    def stop_displaying(self) -> None:
        """
        Stops the background thread that manages the display of text.
        :return: None
        """
        self._stop_event.set()
        self._display_thread.join()
