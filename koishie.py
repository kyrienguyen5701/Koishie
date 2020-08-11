import pyttsx3
import speech_recognition as sr
import wikipedia

import browser, dateNtime, hiNbye

# Speak Method will help us in taking the voice from the machine.
def speak(audio):

    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    for voice in voices:
            engine.setProperty('voice', voices[1].id) # setter method to choose the voice from your computer
    engine.say(audio)
    engine.runAndWait() 

# This method will take in queries and return the desired output
def take_query():

    speak(hiNbye.hello())
    while True:
        query = take_command().lower()
        if 'open' in query:
            store = browser.web_store()
            for web in store.keys():
                print(store[web])
                if web in query:
                    browser.browse(web)
                    break
            continue

        elif 'date' in query:
            available_dates = dateNtime.to_now()
            for date in available_dates:
                if date in query:
                    speak(dateNtime.tellDate(date))
            continue

        elif 'tell me the time' in query:
            speak(dateNTime.tellTime())
            continue

        elif 'goodbye' in query:
            speak(hiNbye.bye())
            exit()

        elif 'from wikipedia' in query:
            speak('Checking the wikipedia') 
            query = query.replace('wikipedia', '') 
            result = wikipedia.summary(query, sentences=4) 
            speak('According to wikipedia') 
            speak(result) 
          
        elif 'your name' in query: 
            speak('I am Koishie. Your beloved waifu')

def take_command():
    
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        print('Listening')  
        r.pause_threshold = 0.7 # seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source) 
          
        #try and catch methods 
        try: 
            print("Recognizing") 
            query = r.recognize_google(audio, language='en-us') 
            print("The command is", query) 
              
        except Exception as e: 
            print(e) 
            print('Say that again darling') 
            return "None"
          
        return query

if __name__ == '__main__': 
    
    take_query()