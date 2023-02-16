import queue
from tkinter import *
import threading
import pyttsx3
import datetime
import pyjokes
import speech_recognition as sr
import vlc
import os
import time

BUF_SIZE = 10
q = queue.Queue(BUF_SIZE)

class Simulation(threading.Thread):
    sea = ["https://www.youtube.com/watch?v=JHAcW9cU0mY",
           "https://www.youtube.com/watch?v=-Tm4H4CrKT0",
           "https://www.youtube.com/watch?v=wFN_QaTw1Bo"]
    mountain = ["https://www.youtube.com/watch?v=eNhPu4Yf4s8",
                "https://www.youtube.com/watch?v=cJpyQ9f1pQU&list=RDCMUCoTedxE3WwpDUGW8P6a3T6Q&index=5",
                "https://www.youtube.com/watch?v=cJHGKSz_CDw&list=RDCMUCoTedxE3WwpDUGW8P6a3T6Q&index=15"]

    def __init__(self):
        super().__init__()
        self.scent = None
        self.temp = None
        self.scenario = None
        self.color_light = None
        self.status = ""
        self.mediaplayer = vlc.MediaPlayer()

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
            print(file)
            if place in file:
                self.media_player = vlc.MediaPlayer("./sim/" + file)
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
            self.run_patel()

    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # This line adds female voice with indian accent.

        self.engine.say("Hi!")
        self.engine.say("How can I help?")
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

            # scenario = ''
            # if ("sea" or "beach") in place:
            #     scenario = random.choice(sea)
            # elif "mountain" in place:
            #     scenario = random.choice(mountain)

            """ producer code """
            if not q.full():
                q.put(["scenario", place])
                print("QUEUE VUI: ", list(q.queue))

            self.narrate('simulating' + place)

            return
        if 'speed' in command:
            speed = command.replace('speed', '')
            self.narrate('speed' + speed)
            if not q.full():
                q.put(["speed", speed])

        if 'scent' in command:
            scent = command.replace('scent', '')
            self.narrate('scent' + scent)
            if not q.full():
                q.put(["scent", scent])

        if 'temperature' in command:
            temperature = command.replace('temperature', '')
            self.narrate('temperature' + temperature)
            if not q.full():
                q.put(["temperature", temperature])

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
        if "stop" in command:
            if not q.full():
                q.put(["stop", "stop"])
        else:
            return


def consume_q(c):
    print("CONSUME")
    voice_feedback.config(text=c[0] + c[1])
    match c[0]:
        case "scenario":
            sim.load_video(c[1])
            q.task_done()
        case "speed":
            speed.config(text=c[1])
            q.task_done()
        case "scent":
            speed.config(text=c[1])
            q.task_done()
        case "temperature":
            speed.config(text=c[1])
            q.task_done()
        case "stop":
            sim.media_player.stop()


class Consumer(threading.Thread):

    def run(self):
        """ consumer code """
        while True:
            if not q.empty():
                c = q.get()
                print("queue ")
                print(list(q.queue))
                consume_q(c)


def play_pause():
    """ pauses and plays """
    sim.play_pause()
    if play_pause_btn.cget['image'] == pause_img:
        play_pause_btn.config(image=start_img)
    else:
        play_pause_btn.config(image=pause_img)


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
root.geometry('900x700+300+50')
root.resizable(False, False)
root.iconbitmap('img/logo.ico')

# Configure root rows and columns
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=2)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)

top_frame = Frame(root, padx=7, bg='green')
center_frame = Frame(root, padx=7, bg='yellow')
btm_frame = Frame(root, padx=7, bg='red')

# top_frame
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)

speed_lb = Label(top_frame, text='Actual Speed: ', padx=20,
                 font=('Helvetica', 16), justify='left')
speed = Label(top_frame, text='              ', padx=20,
              font=('Helvetica', 16), justify='left')
scents_lb = Label(top_frame, text='Scent: ', padx=20,
                  font=('Helvetica', 16), justify='left')
scent = Label(top_frame, text='               ', padx=20,
              font=('Helvetica', 16), justify='left')
temperature_lb = Label(top_frame, text="Playing: ", padx=20,
                       font=('Helvetica', 16), justify='left')
temperature = Label(top_frame, text='               ', padx=20,
                    font=('Helvetica', 16), justify='left')

speed_lb.grid(row=0, column=0)
speed.grid(row=0, column=1)
scents_lb.grid(row=0, column=2)
scent.grid(row=0, column=3)
temperature_lb.grid(row=0, column=4)
temperature.grid(row=0, column=5)

# center_frame
center_frame.rowconfigure(0, weight=1)
center_frame.columnconfigure(0, weight=3)
center_frame.columnconfigure(1, weight=1)
center_frame.rowconfigure(1, weight=1)
center_frame.rowconfigure(2, weight=1)
center_frame.rowconfigure(3, weight=1)
center_frame.rowconfigure(4, weight=1)
center_frame.rowconfigure(5, weight=1)

radioSimulationValue = StringVar(value="Sea")

Label(center_frame, text="Type of simulation").grid(row=0, column=5)
Radiobutton(center_frame, text='Sea', value='sea', variable=radioSimulationValue).grid(row=1, column=5)
Radiobutton(center_frame, text='Mountain', value='mountain', variable=radioSimulationValue).grid(row=2,
                                                                                                 column=5)
Radiobutton(center_frame, text='City', value='city', variable=radioSimulationValue).grid(row=3, column=5)
Radiobutton(center_frame, text='Highway', value='highway', variable=radioSimulationValue).grid(row=4, column=5)
Radiobutton(center_frame, text='Forest', value='forest', variable=radioSimulationValue).grid(row=5, column=5)

radioTemperatureValue = StringVar(value="Medium")
labelTemp = Label(center_frame, text="Temperature").grid(row=0, column=6)
rt1 = Radiobutton(center_frame, text='Low', value='low', variable=radioTemperatureValue).grid(row=1, column=6)
rt2 = Radiobutton(center_frame, text='Medium', value='medium', variable=radioTemperatureValue).grid(row=2,
                                                                                                    column=6)
rt3 = Radiobutton(center_frame, text='High', value='high', variable=radioTemperatureValue).grid(row=3, column=6)

radioScentValue = StringVar(value="Peaches")
labelSim = Label(center_frame, text="Scent").grid(row=0, column=7)
rsc1 = Radiobutton(center_frame, text='Peaches', value='peaches', variable=radioScentValue).grid(row=1,
                                                                                                 column=7)
rsc2 = Radiobutton(center_frame, text='Lavender ', value='lavender', variable=radioScentValue).grid(row=2,
                                                                                                    column=7)
rsc3 = Radiobutton(center_frame, text='Cloves ', value='cloves', variable=radioScentValue).grid(row=3, column=7)
rsc4 = Radiobutton(center_frame, text='Mushrooms', value='mushrooms', variable=radioScentValue).grid(row=4,
                                                                                                     column=7)

buttonConfirm = Button(
    center_frame,
    text="Confirm selection",
    command=lambda: sim.load_video(radioSimulationValue.get()))
buttonConfirm.grid(row=6, column=6)

voice_feedback = Label(center_frame, background='cyan')
voice_feedback.grid(row=0, column=0, columnspan=5, sticky=NSEW)

str = Label(center_frame, text='......', padx=20, font=('Helvetica', 16), justify='left')
str.grid(row=0, column=9)

# Configure btm_frame  rows and columns
start_img = PhotoImage(file=f"img/play.png")
pause_img = PhotoImage(file=f"img/pause.png")
play_pause_btn = Button(master=btm_frame, image=start_img, borderwidth=0, highlightthickness=0,
                        relief="flat",
                        # command=lambda: threading.Thread(target=play_pause).start())
                        command=play_pause)
slow_img = PhotoImage(file=f"img/slow.png")
slow_btn = Button(master=btm_frame, image=slow_img, borderwidth=0, relief="flat",
                  command=sim.slowdown)
fast_img = PhotoImage(file=f"img/fast.png")
fast_btn = Button(master=btm_frame, image=fast_img, borderwidth=0, relief="flat",
                  command=sim.speedup)
load_img = PhotoImage(file=f"img/load.png")
load_btn = Button(master=btm_frame, image=load_img, borderwidth=0, highlightthickness=0, relief="flat",
                  command=lambda: sim.load_video("sim/prova.mkv"))

load_btn.grid(row=0, column=0, sticky=EW)
slow_btn.grid(row=0, column=1, sticky=EW)
play_pause_btn.grid(row=0, column=2, sticky=EW)
fast_btn.grid(row=0, column=4, sticky=EW)

top_frame.grid(row=0, sticky=EW)
center_frame.grid(row=1, sticky=NSEW)
btm_frame.grid(row=2, sticky=EW)

root.mainloop()