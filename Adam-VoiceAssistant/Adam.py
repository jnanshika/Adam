from __future__ import print_function
from random import random
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import ctypes           #foreign func lib that allows to add c compatible datatype allows fun to call in DLLS or shared library
import winshell         #for accessing special folders
from playsound import playsound
import subprocess
import pyjokes
import smtplib 
import requests
import json
import time
from selenium import webdriver
from time import sleep
import config  #python file storing details
import wolframalpha

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from twilio.rest import  Client
import pywhatkit


engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

def speak(text):
    engine.say(text)
    print(text)
    engine.runAndWait()

speak("Loading Adam, your AI personal assistant")

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source, phrase_time_limit=10)    #set the time limit of listening 

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"User said: {statement}\n")

        except Exception as e:
            speak("Please say that again")
            #statement = takeCommand()
            return "None"
        return statement


def note(statement):
    date= datetime.datetime.now()
    file_name= str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(statement) 

    subprocess.Popen(["notepad.exe", file_name])

def send_email(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    server.login(config.email, config.password)      #config is the file name storing details
    server.sendmail(config.email, to, content)
    server.close()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
def google_calender():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # try:
        service = build('calendar', 'v3', credentials=creds)
        return service

def calender_events(num,service):
    speak("Hey hope you're doing good. Here are the events for today")

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(f'Getting the upcoming {num} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=num, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start, event['summary'])
        events_today = (event['summary'])
        start_time = str(start.split("T")[1].split("-")[0])
        if int(start_time.split(':')[0]) < 12:
            start_time = start_time + "am"
        else:
            start_time = str(int(start_time.split(":")[0]) - 12)
            start_time = start_time + "pm"
        speak(f'{events_today} at {start_time}')



if __name__=='__main__':
    wishMe()
    speak("How may I help you?")
    while True:
        try:

            statement = takeCommand().lower()

            if 'wikipedia' in statement:
                speak('Searching Wikipedia...')
                statement =statement.replace("wikipedia", "")
                results = wikipedia.summary(statement, sentences=3)
                speak("According to Wikipedia")
                speak(results)

            if "goodbye" in statement or "ok bye" in statement or "stop" in statement or "exit" in statement:
                speak('your personal assistant Adam is shutting down,Good bye')
                exit()         

            #elif 'news' in statement:
                #news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
                #speak('Here are some headlines from the Times of India,Happy reading')

            #Open Applications
            
            elif "open" in statement:
                if "chrome" in statement.lower():
                    speak ("Opening Google Chrome")
                    os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs")

    
                elif "youtube" in statement:
                    speak ("Opening Youtube")
                    webbrowser.open_new_tab("https://youtube.com/")
                
                elif "google" in statement:
                    speak ("Opening Google")
                    webbrowser.open_new_tab("https://google.com")

                elif "stack overflow" in statement:
                    speak ("Opening StackOverFlow")
                    webbrowser.open("https://stackoverflow.com/")

                elif "spotify" in statement:
                    speak ("Opening Spotify")
                    webbrowser.open_new_tab("https://open.spotify.com/")

                elif 'gmail' in statement:
                    webbrowser.open_new_tab("gmail.com")
                    speak("Google Mail open now")
#notepad
                elif 'notepad' in statement:
                    speak ("Opening notepad...")
                    os.startfile(r"")

                elif "vs code" in statement or "visual studio code" in statement:
                    speak ("Opening Visual Studio Code")
                    os.startfile(r"C:\Users\windows 10\AppData\Local\Programs\Microsoft VS Code\Code.exe")
                    #adding an r because python doesn't allow string with \

                elif "teams" in statement or "ms teams" in statement:
                    speak("Opening Microsoft Teams")
# the path doesn't work 
                    os.startfile(r"C:\Users\windows 10\AppData\Local\Microsoft\Teams\Update.exe --processStart' Teams.exe'")
                else:
                    speak ("Application not available")

            # Q n A
            elif 'time' in statement:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}")

            elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
                speak("I was built by You")

            elif "eat something" in statement:
                speak("Have some tandoori momos")

            elif "sad" in statement:
                speak("you probably just need to eat your favourite food and you will be fine")
                
            elif "who are you" in statement or "define yourself" in statement or "what can you do" in statement:
                speak("Hey, I'm an Adam. Your Assistant. I am here to make your life easier. You can command me to perform various tasks")
                
            elif "your name" in statement:
                speak("My name is Adam")

            elif "who am i" in statement:
                speak("You're probably a human")

            elif "why do you exist" in statement or "why did you come" in statement:
                speak("It's a secret")

            elif "how are you" in statement:
                speak("I am fine, thank you")
                speak("How are you?")
            
            elif "thank you" in statement:
                speak("Happy to help!!!")

            elif "fine" in statement or "good" in statement:
                speak("It's good to know that you are fine")

            elif "joke" in statement or "jokes" in statement:
                joke = pyjokes.get_joke()
                speak(joke)


            
       

            #searching on youtube and google
            
            elif "youtube" in statement:
                ind = statement.split().index("youtube")
                search = statement.split()[ind + 1:]
                webbrowser. open(
                    "http://www.youtube.com/results?search_query=" +
                    "+".join(search)
                )
                speak ("Opening" + str(search) + "on youtube")

            #elif 'search' in statement:
            #   statement = statement.replace("search", "")
            #   webbrowser.open_new_tab(statement)


            elif "search" in statement:
                ind = statement.split().index("search")
                search = statement.split()[ind + 1:]
                webbrowser. open(
                    "http://www.google.com/search?q=" +
                    "+".join(search)
                )
                speak ("Searching" + str(search) + "on google")

            elif "google" in statement:
                ind = statement.split().index("google")
                search = statement.split()[ind + 1:]
                webbrowser. open(
                    "http://www.google.com/search?q=" +
                    "+".join(search)
                )
                speak ("Searching" + str(search) + "on google")

            # Working with our OS i.e make changes on our desktop

            elif "change background" in statement or "change wallpaper" in statement:
                img= r"E:\Wallpaper"
                list_img= os.listdir(img)
                imgChoice = random.choice(list_img)
                randomImg = os.path.join(img, imgChoice)
                SPI_SETDESKWALLPAPER = 20 
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, randomImg, 0)
                speak ("Background changed successfully")

            elif "play music" in statement or "play song" in statement or "play music on desktop" in statement:
                speak("Here you go...")
                music_dir = r"C:\Users\windows 10\Music"
                songs = os.listdir(music_dir)
                print(songs)
                random = os.startfile(os.path.join(music_dir, songs[0]))
                

            elif "play video" in statement:
                song = statement.replace('play', '')
                speak('playing ' + song)
                pywhatkit.playonyt(song)

            elif "empty recycle bin" in statement:
                winshell.recycle_bin().empty(
                    confirm= True, show_progress= False, sound= True
                )
                speak ("Recycle bin emptied")

            elif "note" in statement or "remember this " in statement:
                speak ("What would you like me to write down?")
                note_text = takeCommand()
                note(note_text)
                speak ("I have make a Note of it!")


            elif "mail" in statement or "email" in statement or "gmail" in statement:
                try:
                    speak ("What should I say?")
                    content= takeCommand()
                    #speak("Whom should I sent it to?")
                    to= "jainanshika095@gmail.com"
                    send_email (to, content)
                    speak ("Email has been sent")
                except Exception as e:
                    print(e)
                    speak ("I'm not able to send the email")
#same as above
            #elif "email to computer" in statement or "gmail to computer" in statement:
            #    try:
            #        speak("What should I say?")
            #        content = takeCommand()
            #        speak("whom should i send")
            #        to = input("Enter to address: ")
            #        send_email (to, content)
            #    except Exception as e:
            #        print(e)
            #        speak("I am not able to send this email !!!")

        #Working with API's

            elif "where is" in statement:
                ind= statement.lower().split().index("is")
                location = statement.split()[ind + 1:]
                url = "https://www.google.com/maps/place/" +"".join(location)
                speak ("This is where" + str(location) + "is.")
                webbrowser.open(url)

            elif "weather" in statement:
                key = "1757ecb126f225b68d1a01f35014bd04" 
                weather_url = "https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&"
                ind = statement.split().index("in")
                location = statement.split()[ind + 1:]
                location = "".join(location)
                url= weather_url+ "appid=" + {key} + "&q" + location
                js = requests.get(url).json()
                if js["cod"] != "404":
                    weather = js["main"]
                    temperature = weather["temp"]
                    temperature = temperature - 273.15
                    humidity = weather ["humidity"]
                    desc = js["weather"][0]["description"]
                    weather_response = "The temperature in Celcius is " + str (temperature) + "The humidity is" + str (humidity) + "and weather description is " + str(desc)
                    speak(weather_response)
                else:
                    speak ("City not found")

            elif "news" in statement or "news headlines" in statement:
                url = ("https://newsapi.org/v2/top-headlines?country=in&apiKey=3fecfd7bfaef429cb793f011965c942c")
                try:
                    response = requests.get(url)
                except:
                    speak ("Please check your connections")

                news = json.loads(response.text)

                for new in news ["articles"]:
                    speak(str(new["title"]))
                    sleep(1)
                    engine.runAndWait()
                        

            # WOLFRAMAPLHA
            elif "calculate" in statement:
                app_id = "5KJV4T-UE4E7WA96X"
                client = wolframalpha.Client('5KJV4T-UE4E7WA96X')
                ind = statement.lower().split().index("calculate")
                statement = statement.split()[ind + 1:]
                res = client.query(" ".join(statement))
                answer = next(res.results).text
                speak("The answer is : " + answer)

            elif "what is" in statement or "who is" in statement:
                search = statement.replace("what is", "")
                lookfor = wikipedia.summary(search, 1)
                speak(lookfor)
                #app_id = "5KJV4T-UE4E7WA96X"
                #client = wolframalpha.Client('5KJV4T-UE4E7WA96X')
                #ind = statement.lower().split().index("is")
                #statement = statement.split()[ind + 1:]
                #res = client.query(" ".join(statement))
                #answer = next(res.results).text
                #speak("The answer is: \n" + answer)
                

            #TWILIO
            elif "send message" in statement or "send a message" in statement:
                account_sid= "AC80e54c94f13bed74b9742a632f16e38c"
                auth_token = "357173c52fcfbee06bf0766f8c01490f"
                client = Client(account_sid, auth_token)
                speak("What should I say?")
                message = client.messages.create(
                    body= takeCommand(), from_="", to=""
                )
                print(message.sid)
                speak("Message sent successfully")

        # SHUT DOWN /SLEEP

            elif "log off" in statement or "sign out" in statement:
                speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                subprocess.call(["shutdown", "/l"])

            elif "don't listen" in statement or "stop listening" in statement or " do not listen" in statement:
                speak("for how many seconds do you want me to sleep")
                a= int(takeCommand())
                time.sleep(a)
                speak (str(a) + "seconds completed. Now you can ask me anything!")

            elif "exit" in statement or "quit" in statement:
                exit()
            


        except:
            print("")