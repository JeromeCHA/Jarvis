import speech_recognition as sr
import openai
import pyttsx3

#初期化
engine = pyttsx3.init()

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',  # You can try other engines as well
        prompt=prompt,
        max_tokens=50,  # Adjust the response length as needed
        temperature=0.7,  # Controls the randomness of the output
        n=1,  # Generate a single response
        stop=None,  # You can add a custom stop condition if desired
        timeout=None,  # You can set a timeout in seconds if desired
    )
    return response.choices[0].text.strip()

# Create a recognizer object
recognizer = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Say something...")
    while True:
        # Listen for audio input
        audio = recognizer.listen(source)
        
        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)

            # Exit
            if text in ['bye', 'goodbye', 'exit', 'bye-bye']:
                print("ChatGPT: Goodbye!")
                break

            response = chat_with_gpt(text)
            print(response)
            
        except sr.UnknownValueError:
            print("Unable to recognize speech")
            
        except sr.RequestError as e:
            print("Error: ", e)

