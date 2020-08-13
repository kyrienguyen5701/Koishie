import vlc
import pafy
import time

url = "https://www.youtube.com/watch?v=ikljneOm3Hw"
video = pafy.new(url)
best = video.getbestaudio()
playurl = best.url
player = vlc.MediaPlayer(playurl)
print(player)
player.play()
time.sleep(video.length)