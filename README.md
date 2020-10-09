# Koishie
My virtual desktop assistant, written in Python with the help of other Python APIs.

### Requirement:
`Python: >= 3.7`
`Youtube Data API v3 API key (for using Music commands)`

### Installing

```bash
pip install -r requirements.txt
```
Installing Dlib can be a little bit burdensome, you can choose to opt it out and disable selfie function

### Running

```bash
python koishie.py
```

### TODO
- Add read mood function for Koishie so she can play the music that suits your mood

### Contributing

Any contribution is welcome

### Update log
- October 9th, 2020 (0.0.4): Koishie is now an interpreter (probably)! If you want to learn new words from different languages, just ask Koishie. She will tell you how to write those words, as well as how to pronounce them!
- October 2nd, 2020 (0.0.3): Koishie can now take selfies! Wait, not just ordinary selfie, but only selfie of you smiling. If you are not sure how to smile properly, Koishie is there to help you. Else, show Koishie your brightest smile!
WARNING: I still haven't found a way to make dlib easy to install, use this function at your own risk.
- October 1st, 2020 (0.0.2): Restructuring the project and adding local admin function to add future websites or greetings scripts.
- Aug 13th, 2020 (0.0.1): Koishie can now play music! Thanks to Youtube API v3, Koishie is able to search for any song at your request. (Still some minor bugs in pausing and stopping and very limited daily search count)
To use this function, go to `music.py` and change `[YOUR_API_KEY]` to your own Google Cloud API Key. More at [here](https://cloud.google.com/docs/authentication/api-keys)
- Aug 12th, 2020 (0.0.0): Some simple tasks that Koishie can do:
1. Tell the current time and the date within a close range of the current date.
2. Browsing certain websites, check available websites in `data.json`
3. Summarize useful information from wikipedia based on your request.
