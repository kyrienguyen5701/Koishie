# Koishie
My virtual desktop assistant, written in Python with the help of other Python APIs.

### Requirement:
`Python: >= 3.7`
`Youtube Data API v3 API key (for using Music commands)`

### Installing

```bash
pip install -r requirements.txt
```

### Running

```bash
python koishie.py
```

### TODO
- Come up with new functions :kek:

### Contributing

Any Contribution is welcome

### Update log
- Aug 13th, 2020: Koishie can now play music! Thanks to Youtube API v3, Koishie is able to search for any song at your request. (Still some minor bugs in pausing and stopping and very limited daily search count)
To use this function, go to `music.py` and change `[YOUR_API_KEY]` to your own Google Cloud API Key. More at [here](https://cloud.google.com/docs/authentication/api-keys)
- Aug 12th, 2020 (First version): Some simple tasks that Koishie can do:
1. Tell the current time and the date within a close range of the current date.
2. Browsing certain websites, check available websites in `browser.py`
3. Summarize useful information from wikipedia based on your request.
