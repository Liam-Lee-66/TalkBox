import requests
import SpeechRecognition

endpoint_url = "http://localhost:9000"


def transcribe(file_path, target_lang):
    with open(file_path, "rb") as infile:
        files = {"audio_file": infile}
        response = requests.post(f"{endpoint_url}/asr?task=transcribe&language={target_lang}&output=json", files=files)
        return response.json()["text"]


SpeechRecognition.record()
print(transcribe("MyRecording2.wav", "en"))