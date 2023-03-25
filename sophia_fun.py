from re import split
import pydub
import requests, json, sophia_api,asyncio,audioread, playsound
from os import listdir
from os.path import isfile, join
from pygame import mixer

#current weather
def current_weather(comm):
    city = str(comm[28:])
    complete_url = sophia_api.base_url + "appid=" + sophia_api.api_weather + "&q=" + city
    response = requests.get(complete_url)
    x = response.json()
    print("dobio sam response")
    if x["cod"] != "404":
        y = x["main"]
        temp = y["temp"]
        pressure = y["pressure"]
        humidity = y["humidity"]
        z = x["weather"]
        description = z[0]["description"]
        n = x["wind"]
        wind = n["speed"]
        return "Temperature is " +  str(round(temp-273,2)) + "Celsius Preasure is" + str(pressure) +"hPa, Humidity is " + str(humidity) + "%" + "Wind is blowing "+str(wind) +" meters per seccond"+ str(description)
    else:
        return "error city not found"

#MusicPlayer
music_files = [f for f in listdir("/home/taany/Desktop/Sophia 2.0/music") if isfile(join("/home/taany/Desktop/Sophia 2.0/music", f))]
def play_music():
    mixer.init()
    mixer.music.load(f"/home/taany/Desktop/Sophia 2.0/music/{music_files[0]}")
    mixer.music.play()
    n = 0
    with audioread.audio_open(f"/home/taany/Desktop/Sophia 2.0/music/HS 214. Pripravite Sion harfe.wav") as d:
        total_sec = d.duration
        print(total_sec)
        return total_sec, n 
def pause_music():
    mixer.music.pause()
def unpause_music():
    mixer.music.unpause()
def stop_music():
    mixer.music.stop()
def next_song(n):
    n=n+1
    if n>len(music_files)-1:
        n=0
    mixer.init()
    mixer.music.load(f"/home/taany/Desktop/Sophia 2.0/music/{music_files[n]}")
    mixer.music.play()
    with audioread.audio_open(f"/home/taany/Desktop/Sophia 2.0/music/{music_files[n]}") as d:
        total_sec = d.duration
        print(total_sec)
        return total_sec, n 

def previous_song(n):
    n=n-1
    if n == -1:
        n = len(music_files)-1
    mixer.init()
    mixer.music.load(f"/home/taany/Desktop/Sophia 2.0/music/{music_files[n]}")
    mixer.music.play()
    with audioread.audio_open(f"/home/taany/Desktop/Sophia 2.0/music/{music_files[n]}") as d:
        total_sec = d.duration
        print(total_sec)
        return total_sec, n 

                
