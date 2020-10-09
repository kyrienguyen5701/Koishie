import pyttsx3
import speech_recognition as sr
import wikipedia
import browser, dateNtime, greetings
from music import MusicBot
from selfie import selfie
from translator import languages, trans

version = '0.0.4'

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
    speak(greetings.hello())
    while True:
        # query = take_command().lower()
        query = input('Type here: ')
        if 'browser' in query or 'open' in query:
            store = browser.web_store()
            for web in store.keys():
                print(store[web])
                if web in query:
                    browser.browse(web)
                    break
            continue

        elif 'music' in query:
            lil_Koishie = MusicBot()
            speak('What song you want to hear?')
            while True: # make sure the query is not empty
                song = take_command().lower()
                if song != 'none':
                    break
                else:
                    speak('Invalid query. Pwease try again.')
            lil_Koishie.search(song)
            speak('Here are what I have found. Choose the number of the song you want to listen')
            lil_Koishie.display_results()
            message = lil_Koishie.get_choice(take_command().lower())
            while message != '':
                speak(message)
                message = lil_Koishie.get_choice(take_command().lower())
            while lil_Koishie.state != None:
                control = take_command().lower()
                speak(lil_Koishie.player_control(control))
            continue

        elif 'selfie' in query:
            speak('Smile. Press Q to exit.')
            selfie()
            continue

        elif 'translate' in query or 'translator' in query or 'translation' in query:
            speak('Tell me what language you want to translate to')
            trial = 0
            while trial < 3:
                to_lang = take_command().lower()
                if to_lang not in languages.values():
                    trial += 1
                    speak('Undetected language. Please try again')
                else:
                    break
            if trial == 3:
                speak('Sorry, seem like I have not learnt this language yet.')
            else:
                speak('What you want to translate?')
                sentence = take_command().lower()
                result = trans(sentence, to_lang)
                print(result['Text'])
                speak(result['Pronunciation'])
            continue

        elif 'date' in query:
            available_dates = dateNtime.to_now()
            for date in available_dates:
                if date in query:
                    speak(dateNtime.tellDate(date))
            continue

        elif 'tell me the time' in query:
            speak(dateNtime.tellTime())
            continue

        elif 'goodbye' in query or 'bye' in query:
            speak(greetings.bye())
            exit()

        elif 'from wikipedia' in query:
            speak('Checking the wikipedia') 
            query = query.replace('wikipedia', '') 
            result = wikipedia.summary(query, sentences=4) 
            speak('According to wikipedia') 
            speak(result)
            continue 
          
        elif 'your name' in query: 
            speak('I am Koishie. Your beloved waifu')
            continue

        elif 'version' in query:
            speak('My current version is {}'.format(version))
            continue

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