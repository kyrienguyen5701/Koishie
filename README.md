# Koishie
My multi-functional virtual desktop assistant, written in Python with the help of other Python APIs.
Some functions she can do:
- Browsing websites, tracking duration of browsing, and visualizing the activity history based on:
1. How much time browsing for a specific purpose (study, search, etc.)
2. How much time browsing at a specific basis (daily, weekly, etc.)
3. How much time browsing by day of week (Monday, Tuesday, etc.)
4. How much time browsing by purpose
- Playing music
- Taking selfies
- Translating between languages

### Requirement:
`Python: >= 3.7`

`Youtube Data API v3 API key (for using Music commands)`

`A browser using Chrome core (Microsoft Edge, Google Chrome, Chromium, etc.)`

### Installing

```bash
pip install -r requirements.txt
```
Instructions on installing Dlib for Windows: (read one of these sources)
- [Learn OpenCV](https://www.learnopencv.com/install-dlib-on-windows/)
- [Medium](https://medium.com/analytics-vidhya/how-to-install-dlib-library-for-python-in-windows-10-57348ba1117f)

Instructions on installing tracker function:
- Open your browser, select Extensions
- Check the box next to Developer mode to enable it
- Select Load unpacked extension and navigate to the folder `extension`
- Select OK to load the extension and it should appear in your Extensions list
- Check the box next to Enabled in the list and the icon should appear in your browser

### Running

Open 2 command prompts for these commands:
```bash
python koishie.py
python server.py
```

### TODO
- Add read mood function for Koishie so she can play the music that suits your mood UwU

### Contributing

Any contribution is welcome