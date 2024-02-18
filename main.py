from whisper import transcribe
from listener import record
from time import time
from time import sleep


def run(printing_interval: time, translating_language: str):
    # todo: allow user input here
    record()

    # below is sample mp3
    transcribed = transcribe('recorded.wav', translating_language)

    for sentence in transcribed.split('.'):
        printing = sentence.strip()

        if len(printing) > 0 and printing[-1] != '.':
            print(printing + '.')
        else:
            print(printing)
        sleep(printing_interval)


if __name__ == "__main__":
    run(1, 'ja')
