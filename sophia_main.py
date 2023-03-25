from itertools import count
from logging import exception
import speech_recognition as sr
import pyaudio, os, time, sys, pyodbc, openai, threading 
import sophia_sql, sophia_fun, sophia_api
from getmac import get_mac_address as gma
from gtts import gTTS

r = sr.Recognizer()

def speak_text(command):
    tts = gTTS(text=command, lang='en')
    tts.save("audio.mp3")
    os.system("mpg123 audio.mp3")

def talk():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration = 1)
            audio = r.listen(source)
            MyText = r.recognize_google(audio)
            MyText = MyText.lower()
            return MyText
    except sr.RequestError as e:
        print("Could not request result; {0}".format(e))
    except sr.UnknownValueError:
        print("Unknown error occured")

def check_sophia(command):
    if ("sophia" in command) or ("sofia" in command):
        return True
    else:
        return False


#CheckMacAdress
mac_adress = gma()
data = sophia_sql.get_mac()
if data == 0:
    try:
        speak_text("Hi, what is your name?")
        MyText = talk()
        sophia_sql.insert_mac(mac_adress,MyText)
        speak_text("Hi {0} What can I do for you?".format(str(MyText)))
    except:
        print(Exception)
else:
    speak_text("Hi {0} What can I do for you?".format(str(sophia_sql.get_name())))

time_start = time.time()
total_sec = float('inf')
pause = 0
pause_bol = False
n = 0

while (1):
    try:
        MyText = talk()
        print(MyText)
        print(total_sec)
        print(time.time()-time_start)
        if (time.time()-time_start)>=total_sec:
                if pause_bol is False:
                    total_sec, n = sophia_fun.next_song(n)
                    time_start = time.time()
        if (check_sophia(MyText) is True):
            if "what time is" in MyText:  #Current time command = what time is
                speak_text(time.ctime())
                continue
            if "how's the weather in" in MyText:  #Current weather command = how's the weather in {city}
                speak_text(sophia_fun.current_weather(str(MyText)))
                continue
            if "play music" in MyText:   #Play music command = play music
                speak_text("Playing music")
                total_sec, n = sophia_fun.play_music()
                time_start = time.time()
                continue
            if "pause music" in MyText:   #Pause command = pause music
                sophia_fun.pause_music()
                pause = time.time()
                pause_bol = True
                continue
            if "resume music" in MyText:   #Resume command = resume music
                sophia_fun.unpause_music()
                total_sec = total_sec+(time.time()-pause)
                pause_bol = False
                continue 
            if "stop music" in MyText:    #Stop command = stop music
                sophia_fun.stop_music()
                continue
            if "play next song" in MyText:  #Next song command = play next song
                total_sec, n = sophia_fun.next_song(n)
                time_start = time.time()
                continue
            if  "play previous song" in MyText:    #Previous song command = play previous song
                total_sec, n = sophia_fun.previous_song(n)
                time_start = time.time()
                continue
            if ("shut down pc" in MyText) or ("shutdown pc" in MyText):    #Shut dow PC = shutdown pc
                speak_text("Pc will be shutted down in 5 secconds")
                i=5
                while i>0:
                    speak_text(str(i))
                    i=i-1
                    time.sleep(1)
                speak_text("Shutting down PC")
                os.system('systemctl poweroff') 
            if "thank you" in MyText:     #Thanking
                speak_text("You're welcome "+str(sophia_sql.get_name()))
                continue
            else:
                if "goodbye sophia" in MyText or "goodbye sofia" in MyText: #Turn off sophia = goodbye sophia
                    speak_text("Goodbye "+str(sophia_sql.get_name()))
                    sys.exit()
                openai.api_key = "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"
                openai_text = MyText[6:]
                openai_response = openai.Completion.create(model="text-ada-001", prompt=MyText, temperature=0, max_tokens=100)
                print(openai_response)
                speak_text(str(openai_response["choices"][0]["text"]))
                continue
        else:
            speak_text("Sorry, I dont understand")
    except Exception as e:
        print(e)
    
