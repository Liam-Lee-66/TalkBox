import sounddevice
from scipy.io.wavfile import write


def record() -> None:
    # sample_rate
    fs = 44100

    # Asking to enter the recording time
    second = int(input("Enter the Recording Time in seonds: "))
    print("Recording.....\n")

    # Record the voice
    record_voice = sounddevice .rec(int(second * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    write("MyRecording2.wav", fs, record_voice)

    print("Recording is done please check your folder to listen to the recording")