import threading
import pyttsx3
import datetime
import pyjokes
import random
import speech_recognition as sr

class VUI(threading.Thread):

    def run(self):
        while True:
            self.run_patel()

    def __init__(self, comm):
        super().__init__()
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # This line adds female voice with indian accent.

        self.engine.say("Hi!")
        self.engine.say("How can I help?")
        self.engine.runAndWait()
        self.command = comm

    def narrate(self, text):
        """This function narrates the commands that was taken."""
        self.engine.say(text)
        self.command.put(["Command received: ", text])
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

            #scenario = ''
            # if ("sea" or "beach") in place:
            #     scenario = random.choice(sea)
            # elif "mountain" in place:
            #     scenario = random.choice(mountain)

            print("producer")
            """ producer code """
            if not self.command.full():
                self.command.put(["scenario", place])
                print("QUEUE VUI: ")
                print(list(self.command.queue))

            self.narrate('simulating' + place)

            return
        if 'speed' in command:
            speed = command.replace('speed', '')
            self.narrate('speed' + speed)
            if not self.command.full():
                self.command.put(["speed", speed])

        if 'scent' in command:
            scent = command.replace('scent', '')
            self.narrate('scent' + scent)
            if not self.command.full():
                self.command.put(["scent", scent])

        if 'temperature' in command:
            temperature = command.replace('temperature', '')
            self.narrate('temperature' + temperature)
            if not self.command.full():
                self.command.put(["temperature", temperature])

        if 'what' and 'time' in command:  # shares the current time in 24hr format
            print('--------------- 2 -----------')
            time = datetime.datetime.now().strftime('%H:%M')
            print(time)
            self.narrate('Current time is ' + time)
            return

        if ("joke" or "jokes") in command:  # tells a joke
            print('--------------- 4 -----------' + command)
            joke = pyjokes.get_joke()
            print(joke)
            self.narrate(joke)
            return
        if "bye" in command:
            self.narrate("Bye bye")
            quit()
        else:
            return