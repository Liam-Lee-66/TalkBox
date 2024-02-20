import deepl
import openai
from collections import deque


class Translator:

    def __init__(self, deepl_key: str, openai_key: str) -> None:
        self.DEEPL = deepl.Translator(deepl_key)
        self.OPENAI = openai
        self.OPENAI.api_key(openai_key)
        self.transcriptions = deque()
        self.queue = deque()

    def process_transcriptions(self):
        pass

    def _translate(self, message: str, target_lang: str) -> None:
        """
        Enqueue a str containing the target_lang translation of message.

        List of available languages:
        https://www.deepl.com/docs-api/translate-text/?utm_source=github&utm_medium=github-python-readme
        """
        self.queue.append(self.DEEPL.translate_text(message, target_lang=target_lang).text)

    def dequeue(self) -> str:
        if len(self.queue) > 0:
            return self.queue.popleft()
