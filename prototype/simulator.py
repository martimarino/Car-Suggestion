import os
import vlc
import time
import queue
import pyjokes
import pyttsx3
import datetime
import threading
from tkinter import *
import speech_recognition as sr
from fuzzywuzzy import fuzz

BUF_SIZE = 10
q = queue.Queue(BUF_SIZE)


class Simulation(threading.Thread):

    def __init__(self):
        super().__init__()
        self.media_player = None
        self.scent = None
        self.temp = None
        self.scenario = None
        self.color_light = None
        self.status = ""

    def choose_video(self):
        # .......
        return

    def play_pause(self):
        """ pauses and plays """
        if self.status == "pause":
            self.media_player.play()
            self.status = "play"
            return
        if self.status == "play":
            self.media_player.pause()
            self.status = "pause"
            return

    def load_video(self, place):
        self.status = "play"
        for file in os.listdir('sim'):
            #if place in file:
            ratio = fuzz.ratio(place.lower(), file.lower())
            print(file, ratio)

            if ratio > 50:
                print("HERE!")
                self.media_player = vlc.MediaPlayer("./sim/" + file)
                break
            else:
                self.media_player = vlc.MediaPlayer("./sim/prova.mkv")

        self.media_player.play()
        self.media_player.audio_set_volume(100)

    def speedup(self):
        self.media_player.set_rate(2)

    def slowdown(self):
        self.media_player.set_rate(0.5)

    def run(self):
        return


class VUI(threading.Thread):

    def run(self):
        while True:
            self.run_ada()

    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # This line adds female voice with indian accent.

        # self.engine.say("Hi!")
        # self.engine.say("How can I help?")
        self.engine.runAndWait()

    def narrate(self, text):
        """This function narrates the commands that was taken."""
        self.engine.say(text)
        q.put(["Command received: ", text])
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
            self.run_ada()
        return command.lower()

    def run_ada(self):
        """invokes ada and takes command, identifies specific words and makes ada do things"""
        command = self.take_command()
        print('User Command: ' + command)

        """Plays song or things on youtube"""
        if 'take me to the' in command:
            print('--------------- 1 -----------')
            place = command.replace('take me to the', '')
            print(place)

            """ producer code """
            if not q.full():
                q.put(["scenario", place])
                print("QUEUE VUI: ", list(q.queue))

            self.narrate('simulating' + place)
            return

        if 'pause' in command:
            pause = command.replace('pause', '')
            if not q.full():
                q.put(["pause", pause])

            self.narrate('pause' + pause)
            return

        if 'slow' in command or 'slower' in command:
            slow = command.replace('slow', '')
            if not q.full():
                q.put(["slow", slow])

            self.narrate('slow' + slow)
            return

        if 'fast' in command or 'faster' in command:
            fast = command.replace('fast', '')
            if not q.full():
                q.put(["fast", fast])

            self.narrate('fast' + fast)
            return

        if 'speed' in command:
            speed = command.replace('speed', '')
            if not q.full():
                q.put(["speed", speed])
            self.narrate('speed' + speed)
            return

        if 'scent' in command:
            scent = command.replace('scent', '')
            if not q.full():
                q.put(["scent", scent])
            self.narrate('scent' + scent)
            return

        if 'temperature' in command:
            temperature = command.replace('temperature', '')
            if not q.full():
                q.put(["temperature", temperature])
            self.narrate('temperature' + temperature)
            return

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
        if "stop" in command or "close" in command:
            if not q.full():
                q.put(["stop", "stop"])
        else:
            return


def consume_q(c):
    print("CONSUME", c)
    voice_feedback.config(text=c[0] + c[1])
    match c[0]:
        case "pause":
            sim.play_pause()
            q.task_done()
        case "slow":
            sim.slowdown()
            q.task_done()
        case "fast":
            sim.speedup()
            q.task_done()
        case "scenario":
            sim.load_video(c[1])
            q.task_done()
        case "speed":
            set_GUI("speed", c[1])
            q.task_done()
        case "scent":
            set_GUI("scent", c[1])
            q.task_done()
        case "temperature":
            set_GUI("temperature", c[1])
            q.task_done()
        case "stop":
            sim.media_player.stop()

def set_GUI(element, value):

    match element:
        case "speed":
            speed.config(text=value)
        case "scent":
            scent.config(text=value)
        case "temperature":
            temperature.config(text=value)
            if value == "high" or value == "High":
                root.config(background="red")
                center_frame.config(background="red")
            elif value == "medium" or value == "Medium":
                root.config(background="orange")
                center_frame.config(background="red")
            elif value == "low" or value == "Low":
                root.config(background="yellow")
                center_frame.config(background="red")

class Consumer(threading.Thread):

    def run(self):
        """ consumer code """
        while True:
            if not q.empty():
                c = q.get()
                print("queue ")
                print(list(q.queue))
                consume_q(c)

def play_video(place, scent, temperature):
    sim.load_video(place)
    set_GUI("speed", "normal")
    set_GUI("scent", scent)
    set_GUI("temperature", temperature)

vui = VUI()
vui.start()
time.sleep(2)
sim = Simulation()
cons = Consumer()
cons.start()
time.sleep(2)

# Configure root params
root = Tk()
root.title("Car Suggestion")
root.geometry('410x600+300+50')
root.resizable(False, False)
root.iconbitmap('img/logo.ico')

# Configure root rows and columns
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=2)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)

top_frame = Frame(root, padx=20)
center_frame = Frame(root, padx=20, bg='#90EE90')
btm_frame = Frame(root, padx=20, bg='#D3D3D3')

# top_frame
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)

speed_lb = Label(top_frame, text='Speed: ',
                 font=('Helvetica', 12), justify='left')
speed = Label(top_frame, text='', padx=20,
              font=('Helvetica', 12), justify='left')
scents_lb = Label(top_frame, text='Scent: ', padx=20,
                  font=('Helvetica', 12), justify='left')
scent = Label(top_frame, text='', padx=20,
              font=('Helvetica', 12), justify='left')
temperature_lb = Label(top_frame, text="Temp: ", padx=20,
                       font=('Helvetica', 12), justify='left')
temperature = Label(top_frame, text='', padx=20,
                    font=('Helvetica', 12), justify='left')

speed_lb.grid(row=0, column=0)
speed.grid(row=0, column=1)
scents_lb.grid(row=0, column=2)
scent.grid(row=0, column=3)
temperature_lb.grid(row=0, column=4)
temperature.grid(row=0, column=5)

# center_frame
center_frame.rowconfigure(0, weight=1)
center_frame.columnconfigure(0, weight=2)
center_frame.columnconfigure(1, weight=1)
center_frame.columnconfigure(2, weight=1)
center_frame.columnconfigure(3, weight=1)
center_frame.rowconfigure(1, weight=1)
center_frame.rowconfigure(2, weight=1)
center_frame.rowconfigure(3, weight=1)
center_frame.rowconfigure(4, weight=1)

radioSimulationValue = StringVar(value="Sea")

Label(center_frame, text="Type of simulation").grid(row=0, column=0)
Radiobutton(center_frame, text='Sea', value='sea', variable=radioSimulationValue).grid(row=1, column=0)
Radiobutton(center_frame, text='Mountain', value='mountain', variable=radioSimulationValue).grid(row=2,
                                                                                                 column=0)
Radiobutton(center_frame, text='City', value='city', variable=radioSimulationValue).grid(row=3, column=0)
Radiobutton(center_frame, text='Highway', value='highway', variable=radioSimulationValue).grid(row=4, column=0)
Radiobutton(center_frame, text='Forest', value='forest', variable=radioSimulationValue).grid(row=5, column=0)

radioTemperatureValue = StringVar(value="Medium")
labelTemp = Label(center_frame, text="Temperature").grid(row=0, column=1)
rt1 = Radiobutton(center_frame, text='Low', value='low', variable=radioTemperatureValue).grid(row=1, column=1)
rt2 = Radiobutton(center_frame, text='Medium', value='medium', variable=radioTemperatureValue).grid(row=2,
                                                                                                    column=1)
rt3 = Radiobutton(center_frame, text='High', value='high', variable=radioTemperatureValue).grid(row=3, column=1)

radioScentValue = StringVar(value="Peaches")
labelSim = Label(center_frame, text="Scent").grid(row=0, column=2)
rsc1 = Radiobutton(center_frame, text='Peaches', value='peaches', variable=radioScentValue).grid(row=1,
                                                                                                 column=2)
rsc2 = Radiobutton(center_frame, text='Lavender ', value='lavender', variable=radioScentValue).grid(row=2,
                                                                                                    column=2)
rsc3 = Radiobutton(center_frame, text='Cloves ', value='cloves', variable=radioScentValue).grid(row=3, column=2)
rsc4 = Radiobutton(center_frame, text='Mushrooms', value='mushrooms', variable=radioScentValue).grid(row=4,
                                                                                                     column=2)

buttonConfirm = Button(
    center_frame,
    text="Confirm selection",
    command=lambda: play_video(radioSimulationValue.get(), radioScentValue.get(), radioTemperatureValue.get()))
buttonConfirm.grid(row=6, column=1)

# Configure btm_frame  rows and columns

voice_feedback = Label(btm_frame)
voice_feedback.grid(row=0, column=0, sticky=EW)

top_frame.grid(row=0, sticky=EW)
center_frame.grid(row=1, sticky=NSEW)
btm_frame.grid(row=2, sticky=EW)

root.mainloop()