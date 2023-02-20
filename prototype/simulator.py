import os
import random

import vlc
import time
import queue
import pyjokes
import pyttsx3
import datetime
import threading
from tkinter import *
import speech_recognition as sr

BUF_SIZE = 10
q = queue.Queue(BUF_SIZE)

class Simulation(threading.Thread):

    def __init__(self):
        super().__init__()
        self.media_player = None
        self.perfume = None
        self.temp = None
        self.scenario = None
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
        list = []
        for file in os.listdir('sim'):
            file_name, file_extension = os.path.splitext(file)
            print(file, file_name)
            name = file_name.split("_")
            if name[0] in place:
                print(file_name, name[0])
                list.append(file)

        print(list)

        if list:
            choice = random.randint(0, len(list) - 1)
            print(choice, list[choice])
            self.media_player = vlc.MediaPlayer("./sim/" + list[choice])
        else:
            self.media_player = vlc.MediaPlayer("./sim/prova.mkv")

        self.media_player.play()
        self.media_player.audio_set_volume(100)

    def speedup(self):
        rate = self.media_player.get_rate()*2
        self.media_player.set_rate(rate)
        return rate

    def slowdown(self):
        rate = self.media_player.get_rate()/2
        self.media_player.set_rate(rate)
        return rate

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
            command = r.recognize_google(audio, language='en-in')
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

        if 'change of scenario to' in command:
            place = command.replace('change scenario to', '')
            print(place)

            """ producer code """
            if not q.full():
                q.put(["change", place])
                print("QUEUE VUI: ", list(q.queue))

            self.narrate('change to' + place)
            return

        if 'pause' in command:
            pause = command.replace('pause', '')
            if not q.full():
                q.put(["pause", pause])

            self.narrate('pause' + pause)
            return

        if 'slow' in command or 'slower' in command or 'low' in command:
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

        if 'perfume' in command:
            perfume = command.replace('perfume', '')
            if not q.full():
                q.put(["perfume", perfume])
            self.narrate('perfume' + perfume)
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
    if c[0] == "change":
        sim.media_player.stop()
        sim.load_video(c[1])
        if  "sea" in c[1]:
            set_GUI("perfume", "peaches")
        if "city" == c[1] or "highway" == c[1]:
            set_GUI("perfume", "lavender")
        if "mountain" == c[1]:
            set_GUI("perfume", "cloves")
        if  "forest" == c[1]:
            set_GUI("perfume", "mushrooms")
        q.task_done()
    elif c[0] == "pause":
        sim.play_pause()
        q.task_done()
    elif c[0] == "slow":
        rate = sim.slowdown()
        set_GUI("speed", set_speed_label_value(rate))
        q.task_done()
    elif c[0] == "fast":
        rate = sim.speedup()
        set_GUI("speed", set_speed_label_value(rate))
        q.task_done()
    elif c[0] == "scenario":
        sim.load_video(c[1])
        set_GUI("speed", set_speed_label_value(1))   # normal speed
        set_GUI("temperature", "medium")

        if  "sea" in c[1]:
            set_GUI("perfume", "peaches")
        if "city" == c[1] or "highway" == c[1]:
            set_GUI("perfume", "lavender")
        if "mountain" == c[1]:
            set_GUI("perfume", "cloves")
        if  "forest" == c[1]:
            set_GUI("perfume", "mushrooms")
        q.task_done()

    elif c[0] == "perfume":
        print("PERFUME CASE", c[1])
        if c[1].strip() in ["peaches", "lavender", "cloves", "mushrooms"]:
            set_GUI("perfume", c[1])
            q.task_done()

    elif c[0] == "temperature":
        if c[1].strip() in ["low", "medium", "high"]:
            set_GUI("temperature", c[1])
            q.task_done()

    elif c[0] == "stop":
        sim.media_player.stop()

def set_speed_label_value(value):
    if value == 1:
        return str(random.randint(40, 60)) + ' km/h'
    elif value == 0.5:
        return str(random.randint(20, 40)) + ' km/h'
    elif value == 0.25:
        return str(random.randint(10, 20)) + ' km/h'
    elif value == 2:
        return str(random.randint(60, 80)) + ' km/h'
    elif value == 4:
        return str(random.randint(80, 100)) + ' km/h'

def change_colors(value):
    if "peaches" in value:
        root.config(background="#FFCBA4")
    elif "lavender" in value:
        root.config(background="#DCD0FF")
    elif "cloves" in value:
        root.config(background="#A75C3A")
    elif "mushrooms" in value:
        root.config(background="#D8CCC0")

def set_GUI(element, value):

    print(element, value)
    if element == "speed":
        speed.config(text=value)
    elif element == "perfume":
        print("VALUE", value)
        perfume.config(text=value)
        change_colors(value.lower())
    elif element == "temperature":
        temperature.config(text=value)
    elif element == "color":
        change_colors(value.lower())

class Consumer(threading.Thread):

    def run(self):
        """ consumer code """
        while True:
            if not q.empty():
                c = q.get()
                print("queue ")
                print(list(q.queue))
                consume_q(c)

def play_video(place, perfume, temperature):
    sim.load_video(place)
    set_GUI("speed", set_speed_label_value(1))   # normal speed
    set_GUI("perfume", perfume)
    set_GUI("temperature", temperature)

vui = VUI()
vui.daemon = True
vui.start()
time.sleep(2)
sim = Simulation()
cons = Consumer()
cons.daemon = True
cons.start()
time.sleep(2)

# Configure root params
root = Tk()
root.title("Car Suggestion")
root.geometry('500x550+300+50')
# root.resizable(False, False)
root.iconbitmap('img/logo.ico')
root.config(bg="#90EE90")

# Configure root rows and columns
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=2)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)

top_frame = Frame(root, padx=20)
center_frame = Frame(root, padx=20, bg='white')
btm_frame = Frame(root, padx=20, bg='#D3D3D3')

# top_frame
top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)
top_frame.columnconfigure(2, weight=1)
top_frame.columnconfigure(3, weight=1)
top_frame.columnconfigure(4, weight=1)
top_frame.columnconfigure(5, weight=1)

speed_lb = Label(top_frame, text='Speed: ',
                 font=('Helvetica', 12), justify='left')
speed = Label(top_frame, text='            ',
              font=('Helvetica', 12), justify='left')
perfumes_lb = Label(top_frame, text='   Perfume: ',
                  font=('Helvetica', 12), justify='left')
perfume = Label(top_frame, text='              ',
              font=('Helvetica', 12), justify='left')
temperature_lb = Label(top_frame, text="   Temp: ",
                       font=('Helvetica', 12), justify='left')
temperature = Label(top_frame, text='              ',
                    font=('Helvetica', 12), justify='left')

speed_lb.grid(row=0, column=0)
speed.grid(row=0, column=1)
perfumes_lb.grid(row=0, column=2)
perfume.grid(row=0, column=3)
temperature_lb.grid(row=0, column=4)
temperature.grid(row=0, column=5)

# center_frame
center_frame.rowconfigure(0, weight=1)
center_frame.rowconfigure(1, weight=1)
center_frame.rowconfigure(2, weight=1)
center_frame.rowconfigure(3, weight=1)
center_frame.rowconfigure(4, weight=1)
center_frame.rowconfigure(5, weight=1)
center_frame.rowconfigure(6, weight=1)
center_frame.columnconfigure(0, weight=2)
center_frame.columnconfigure(1, weight=1)
center_frame.columnconfigure(2, weight=1)

radioSimulationValue = StringVar(value="Sea")

Label(center_frame, text="Type of simulation:").grid(row=0, column=0, sticky="W")
Radiobutton(center_frame, text='Sea', value='sea', variable=radioSimulationValue).grid(row=1, column=0, sticky="W")
Radiobutton(center_frame, text='Mountain', value='mountain', variable=radioSimulationValue).grid(row=2, column=0,
                                                                                                 sticky="W")
Radiobutton(center_frame, text='City', value='city', variable=radioSimulationValue).grid(row=3, column=0, sticky="W")
Radiobutton(center_frame, text='Highway', value='highway', variable=radioSimulationValue).grid(row=4, column=0,
                                                                                               sticky="W")
Radiobutton(center_frame, text='Forest', value='forest', variable=radioSimulationValue).grid(row=5, column=0,
                                                                                             sticky="W")

radioTemperatureValue = StringVar(value="Medium")
Label(center_frame, text="Temperature:").grid(row=0, column=1, sticky="W")
Radiobutton(center_frame, text='Low', value='low', variable=radioTemperatureValue).grid(row=1, column=1,
                                                                                        sticky="W")
Radiobutton(center_frame, text='Medium', value='medium', variable=radioTemperatureValue).grid(row=2,
                                                                                              column=1,
                                                                                              sticky="W")
Radiobutton(center_frame, text='High', value='high', variable=radioTemperatureValue).grid(row=3, column=1,
                                                                                          sticky="W")

radioperfumeValue = StringVar(value="Peaches")
Label(center_frame, text="Perfume:").grid(row=0, column=2, sticky="W")
Radiobutton(center_frame, text='Peaches', value='peaches', variable=radioperfumeValue).grid(row=1,
                                                                                            column=2, sticky="W")
Radiobutton(center_frame, text='Lavender ', value='lavender', variable=radioperfumeValue).grid(row=2,
                                                                                               column=2,
                                                                                               sticky="W")
Radiobutton(center_frame, text='Cloves ', value='cloves', variable=radioperfumeValue).grid(row=3, column=2,
                                                                                           sticky="W")
Radiobutton(center_frame, text='Mushrooms', value='mushrooms', variable=radioperfumeValue).grid(row=4,
                                                                                                column=2,
                                                                                                sticky="W")

buttonConfirm = Button(
    center_frame,
    text="Confirm selection",
    command=lambda: play_video(radioSimulationValue.get(), radioperfumeValue.get(), radioTemperatureValue.get()))
buttonConfirm.grid(row=6, column=1, sticky="W")

# Configure btm_frame  rows and columns

voice_feedback = Label(btm_frame)
voice_feedback.grid(row=0, column=0, sticky=EW)

top_frame.grid(row=0, sticky=EW)
center_frame.grid(row=1, sticky=NSEW)
btm_frame.grid(row=2, sticky=EW)

root.mainloop()