import threading

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random

import video_player

sea = ["https://www.youtube.com/watch?v=JHAcW9cU0mY",
        "https://www.youtube.com/watch?v=-Tm4H4CrKT0",
        "https://www.youtube.com/watch?v=wFN_QaTw1Bo"]
mountain = ["https://www.youtube.com/watch?v=eNhPu4Yf4s8",
            "https://www.youtube.com/watch?v=cJpyQ9f1pQU&list=RDCMUCoTedxE3WwpDUGW8P6a3T6Q&index=5",
            "https://www.youtube.com/watch?v=cJHGKSz_CDw&list=RDCMUCoTedxE3WwpDUGW8P6a3T6Q&index=15"]


class SR(threading.Thread):

    def run(self):
        while (True):
            self.run_patel()


    def __init__(self):
        super().__init__()
        listener = sr.Recognizer()
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id) # This line adds female voice with indian accent. had to add the indian(english) voice to microsoft, export it from registry detector and modify the file by opening it with text editor.

        self.engine.say("Hi!")
        self.engine.say("How can I help?")
        self.engine.runAndWait()


    def narrate(self, text):
        """This function narrates the commands that was taken."""
        self.engine.say(text)
        self.engine.runAndWait()


    def take_command(self):
        print('--------------- take command -----------')
        command = ''
        """This functions takes commands"""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(' I am ready for your next command')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print('You said: ' + command + '/n')

        except sr.UnknownValueError:
            self.run_patel()
        return command.lower()


    def run_patel(self):
        """invokes patel and takes command, identifies specific words and makes patel do things"""
        command = self.take_command()
        print('User Command: ' + command)

        """Plays song or things on youtube"""
        if 'take me to the' in command:
            print('--------------- 1 -----------')
            place = command.replace('take me to the', '')
            print(place)
            self.narrate('simulating' + place)
            link = ''
            if ("sea" or "beach") in place:
                link = random.choice(sea)
            elif ("mountain" in place):
                link = random.choice(mountain)



            video = video_player.Player().start()
            # pywhatkit.playonyt(link)
            return
        if 'play' and 'on youtube' in command:
            print('--------------- 1 -----------')
            song = command.replace('play', '').replace('on youtube', '')
            self.narrate('playing' + song)
            pywhatkit.playonyt(song)
            return
        if 'what' and 'time' in command:  # shares the current time in 24hr format
            print('--------------- 2 -----------')
            time = datetime.datetime.now().strftime('%H:%M')
            print(time)
            self.narrate('Current time is ' + time)
            return
        if 'tell me about' in command:  # finds the information from wikipedia
            print('--------------- 3 -----------')
            person = command.replace('tell me about ', '')
            try:
                info = wikipedia.summary(person, 1)
                print(info)
                self.narrate(info)
                return
            except wikipedia.DisambiguationError as e:
                self.engine.say(person + "not found")
                self.run_patel()
            except wikipedia.exceptions.PageError as e:
                self.engine.say(person + "not found")
                self.run_patel()

        if ("joke" or "jokes") in command:  # tells a joke
            print('--------------- 4 -----------' + command)
            joke = pyjokes.get_joke()
            print(joke)
            self.narrate(joke)
            return
        if ("bye" in command):
            self.narrate("Bye bye")
            quit()
        else:
            return