from whisper import transcribe
from time import time
from time import sleep


def run(printing_interval: time):
    # todo: allow user input here

    # below is sample mp3
    transcribed = transcribe('test.mp3', 'en')

    for sentence in transcribed.split('.'):
        printing = sentence.strip()

        if len(printing) > 0 and printing[-1] != '.':
            print(printing + '.')
        else:
            print(printing)
        sleep(printing_interval)


if __name__ == "__main__":
    run(3)
