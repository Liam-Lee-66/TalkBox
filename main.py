from whisper import transcribe
from listener import record
from translator import translate
from tts import text_to_speech
from time import time
from time import sleep


def _split_for(input_: str, look_for: list[str]) -> list[str]:
    """
    >>> a = "1. 2? 3! 4/ 5_ 6"
    >>> b = "1. 2? 3! 4/ 5_ 6`"
    >>> _split_for(a, ['.', '?', '!', '/', '_'])
    ['1.', '2?', '3!', '4/', '5_', '6']
    >>> _split_for(b, ['.', '?', '!', '/', '_', '`'])
    ['1.', '2?', '3!', '4/', '5_', '6`']
    >>> c = 'uh'
    >>> _split_for(c, ['.'])
    ['uh']
    """

    returning = []
    tracking = 0

    for i in range(len(input_)):
        if input_[i] in look_for:
            returning.append(input_[tracking:i + 1])
            tracking = i + 2

    if tracking < len(input_):
        returning.append(input_[tracking:len(input_)])
    return returning


def run(printing_interval: time, inputting_language: str):
    record()

    # transcribed = transcribe('recorded.wav', translating_language)
    # print(transcribed)
    # text_to_speech(transcribed)

    transcribed = _split_for(transcribe('recorded.wav', inputting_language), ['.', '?', '!'])

    for sentence in transcribed:
        to_read = translate(sentence.strip(), 'EN-US')
        print(f"{sentence.strip()} -> {to_read}")
        text_to_speech(to_read)
        sleep(printing_interval)


if __name__ == "__main__":
    run(1, 'ko')
