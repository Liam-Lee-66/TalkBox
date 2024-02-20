import requests
import subprocess

endpoint_url = "http://localhost:9000"


def is_silent(filename: str, second: float) -> bool:
    cmd = f"ffmpeg -i {filename} -af silencedetect=noise=-30dB:d=0.5 -f null -"

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error = process.communicate()

    output = error.decode("utf-8")

    if not output.split()[-1].replace(".", "").isdigit():
        return False
    else:
        return float(output.split()[-1]) == second


def transcribe(filename: str, target_lang: str, second: float) -> str:
    if is_silent(filename, second):
        return

    with open(filename, "rb") as infile:
        files = {"audio_file": infile}
        response = requests.post(f"{endpoint_url}/asr?task=transcribe&language={target_lang}&output=json", files=files)
        return response.json()["text"] if response else ""
