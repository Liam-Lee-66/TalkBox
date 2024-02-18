import sounddevice
from scipy.io.wavfile import write
from threading import Thread
from time import time


def record(second: time) -> None:
    # sample_rate
    fs = 44100

    print("Recording.....\n")

    # Record the voices
    record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    Thread(target=write, args=["recorded.wav", fs, record_voice]).start()

    print("Recording is done please check your folder to listen to the recording")