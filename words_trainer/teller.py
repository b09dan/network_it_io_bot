import pyttsx3

text = "Hello, how are you?"

# TTS initialization
engine = pyttsx3.init()

# say the text
engine.say(text)

# end
engine.runAndWait()
