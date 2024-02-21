import deepl
from collections import deque


class Translator:
    """

    """

    def __init__(self, output_language: str, deepl_key: str) -> None:
        self.output_language = output_language
        self._DEEPL = deepl.Translator(deepl_key)
        self.transcriptions = deque()
        self.queue = deque()

    def process_transcriptions(self) -> None:

        while self.transcriptions:
            transcript = self.transcriptions.pop()
            self.queue.append(self._translate(transcript, self.output_language))

    def _translate(self, message: str, target_lang: str) -> None:
        """
        Enqueue a str containing the target_lang translation of message.

        List of available languages:
        https://www.deepl.com/docs-api/translate-text/?utm_source=github&utm_medium=github-python-readme
        """
        self.queue.append(self._DEEPL.translate_text(message, target_lang=target_lang).text)

    def dequeue(self) -> str:
        if self.queue:
            return self.queue.popleft()
