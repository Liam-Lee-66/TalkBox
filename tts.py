import pyttsx3


def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    # You can adjust the voice, rate, volume, etc.
    # For example:
    # engine.setProperty('rate', 150)  # Speed of speech (words per minute)

    # Convert text to speech
    engine.say(text)

    # Play the speech
    engine.runAndWait()
