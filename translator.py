import deepl

with open("credentials.txt", "r") as infile:
    AUTH_KEY = infile.readline()

translator = deepl.Translator(AUTH_KEY)


def translate(message: str, target_lang: str) -> str:
    """
    Return a str containing the target_lang translation of message.

    List of available languages:
    https://www.deepl.com/docs-api/translate-text/?utm_source=github&utm_medium=github-python-readme
    """
    return translator.translate_text(message, target_lang=target_lang).text
