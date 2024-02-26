import requests
import winsound
import json
from urllib.parse import urlencode

endpoint_url = "http://localhost:50021"

with open("speakers.json", "rb") as infile:
    speaker_json = json.loads(infile.readline())

speaker_library = speaker_json["speakers"]


class VoiceVox:
    """

    """
    speaker_id: str
    volume_scale: float
    intonation_scale: float
    pre_phoneme_length: float
    post_phoneme_length: float

    def __init__(self, speaker_id: str, volume: float, intonation: float, pre_phoneme: float, post_phoneme: float):
        self.speaker_id = speaker_id
        self.volume_scale = volume
        self.intonation_scale = intonation
        self.pre_phoneme_length = pre_phoneme
        self.post_phoneme_length = post_phoneme

    def speak(self, sentence: str) -> None:
        # generate initial query
        params_encoded = urlencode({'text': sentence, 'speaker': self.speaker_id})
        r = requests.post(f'{endpoint_url}/audio_query?{params_encoded}')
        voicevox_query = r.json()
        voicevox_query["volumeScale"] = self.volume_scale
        voicevox_query["intonationScale"] = self.intonation_scale
        voicevox_query["prePhonemeLength"] = self.pre_phoneme_length
        voicevox_query["postPhonemeLength"] = self.post_phoneme_length

        # synthesize voice as wav file
        params_encoded = urlencode({'speaker': self.speaker_id})
        r = requests.post(f'{endpoint_url}/synthesis?{params_encoded}', json=voicevox_query)

        with open("output.wav", "wb") as outfile:
            outfile.write(r.content)

        winsound.PlaySound("output.wav", winsound.SND_FILENAME)

    def set_speaker(self, speaker_string: str, version_index: int = 0) -> None:
        self.speaker_id = speaker_library[speaker_string][version_index]



