import speech_recognition as sr
import openai
import pyttsx3 as tts
from sys import platform
from os import system

class Jarvis:
    ignoreWords = ['www', 'jarvis']
    isWindows = False
    initMessage = """
    Act like a server. Your name is Jarvis. 

    All commands starts with <command_name> : <description>
    Please use only those commands. 

    Commands :
    - !text <message> : To say something on Twitch
    """

    def __init__(self):
        # Init TTS only for Windows platform
        # Otherwise we got a segmentation fault error
        self.isWindows = platform == "win32"

        # InitChatGPT
        self.initChatGPT()

    def chatWithGPT(self, prompt):
        response = openai.Completion.create(
            engine='gpt-4',  # You can try other engines as well
            prompt=prompt,
            max_tokens=50,  # Adjust the response length as needed
            temperature=0.7,  # Controls the randomness of the output
            n=1,  # Generate a single response
            stop=None,  # You can add a custom stop condition if desired
            timeout=None,  # You can set a timeout in seconds if desired
        )
        return response.choices[0].text.strip()

    def initTTS(self):
        # TTS Init
        self.engine = tts.init()
        
        # Select the voice for the TTS
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice',voices[0].id)

        # Set Rate for the TTS
        self.engine.setProperty('rate', 150)


    def sayTTS(self, text):
        # Don't say if there is an ignore word
        # or if the text start with a command
        if [word.lower() for word in self.ignoreWords if(word in text.lower())] or text.startswith("!"):
            return

        if self.isWindows:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            system(text)

    def initChatGPT(self):
        response = self.chatWithGPT(self.initMessage)
        print(response)

    def start(self):
        # Create a recognizer object
        recognizer = sr.Recognizer()

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            while True:
                # Listen for audio input
                audio = recognizer.listen(source)
                
                try:
                    # Recognize speech using Google Speech Recognition
                    text = recognizer.recognize_google(audio)

                    # Use ChatGPT
                    response = self.chatWithGPT(text)

                    # TTS
                    self.sayTTS(response)

                except sr.UnknownValueError:
                    print("Unable to recognize speech")
                    
                except sr.RequestError as e:
                    print("Error: ", e)