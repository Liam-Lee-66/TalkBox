import sounddevice
from scipy.io.wavfile import write


def record() -> None:
    # sample_rate
    fs = 44100

    # Asking to enter the recording time
    second = int(input("Enter the Recording Time in seconds: "))
    print("Recording.....\n")

    # Record the voice
    record_voice = sounddevice .rec(int(second * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    write("recorded.wav", fs, record_voice)

    print("Recording is done please wait a moment for the prompt to process.")