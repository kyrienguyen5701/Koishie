# Koishie
My virtual desktop assistant, written in Python with the help of other Python APIs.

### Requirement:
`Python: >= 3.7`

### Libraries
- requests 
- pyttsx3 (speech-to-text)
- SpeechRecognition
- wikipedia 
- pyaudio (complement for SR)
- pafy (getting youtube videos' information)
- vlc (play youtube video in audio only)
- word2number


To install those libraries, simply type `pip install {dependency_name}` or `python -m pip install {dependency_name}` into your command prompt.
If you have errors installing PyAudio, please refer to this [source](https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14)

### Update log
- Aug 13th, 2020: Koishie can now play music! Thanks to Youtube API v3, Koishie is able to searh for any song at your request. (Still some minor bugs in pausing and stopping and very limited daily search count)
To use this function, go to `music.py` and change `[YOUR_API_KEY]` to your own Google Cloud API Key. More at [here](https://cloud.google.com/docs/authentication/api-keys)
- Aug 12th, 2020 (First version): Some simple tasks that Koishie can do:
1. Tell the current time and the date within a close range of the current date.
2. Browsing certain websites, check available websites in `browser.py`
3. Summarize useful information from wikipedia based on your request.
