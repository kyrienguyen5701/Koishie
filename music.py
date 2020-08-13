import json
import requests
import vlc
import pafy
import time
from word2number import w2n

PLAY = 'PLAY'
PAUSE = 'PAUSE'
RESUME = 'RESUME'
STOP = 'STOP'
API_KEY = '[YOUR_API_KEY]'

class MusicBot:

    def __init__(self):
        self.player = None
        self.url = None # youtube link
        self.state = None
        self.data = None # search results

    def search(self, song):
        r = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q={}&key={}}'.format(song, API_KEY))
        print(json.loads(r.text))
        self.data = json.loads(r.text)['items']

    def display_results(self):
        if self.data == None:
            return 'You have not searched anything yet.'
        for i in range(len(self.data)):
            temp = pafy.new('https://www.youtube.com/watch?v={}'.format(self.data[i]['id']['videoId']))
            print('{}. {} | {} views| Ratings: {:.2f}'.format(str(i + 1), temp.title, temp.viewcount, temp.rating))
        return 'Here are songs that you request'

    def get_choice(self, choice):
        try: 
            choice = w2n.word_to_num(choice)
            if choice * (choice - len(self.data) - 1) >= 0: # not in search result
                return 'Invalid number. Pwease say again.'
            else:
                id = self.data[choice - 1]['id']['videoId']
                song = pafy.new('https://www.youtube.com/watch?v={}'.format(id))
                self.url = song.getbestaudio().url
                self.state = PLAY
                self.player = vlc.MediaPlayer(self.url)
                self.player.play()
                # time.sleep(song.length)
                return ''
        except Exception as e: 
            return e

    def player_control(self, command):
        if self.url == None:
            return 'There is currently no song in the queue'
        if command.upper() == PLAY or command.upper() == RESUME:
            self.player.play()
            self.state = PLAY
            return 
        elif command.upper() == PAUSE:
            self.player.pause()
            self.state = PAUSE
            return
        elif command.upper() == STOP:
            self.player.stop()
            self.player = None
            self.song = None
            self.state = None
            self.media = None
            return
        else:
            return 'Invalid command. Please say again.'

# uncomment code below for testing
# mb = MusicBot()
# mb.search('Hartmann Youkai Girl')
# mb.display_results()
# mb.get_choice('one')
# # mb.player_control('play')
# for i in range(1000000):
#     print(i)
#     if (i == 150000):
#         mb.player_control('pause')