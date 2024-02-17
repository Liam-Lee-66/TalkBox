# TalkBox

## Notes for testSpeechRecognition.py
### Import issue
The module **speech_recognition** will not be recognized in python until the below are imported.
    
    pip install SpeechRecognition
    pip install PyAudio
    pip install beautifulsoup4
    pip install googletrans
    pip install gTTS
    pip install gTTS-token
    pip install pipwin      
    pip install playsound   # still works without running
    pip install pyobjc      # for macOS
    pip install pylint
    pip install setuptools
    pip install Translator
    brew install flac       # still works without running
    brew install portaudio  # still works without running

### Method missing issue
During the processing, the yellow underline will be recognizable for;
    
    # the below runs even with a yellow underline
    print("You said: " + r.recognize_google(audio))
Ignore the above, the code should still run.