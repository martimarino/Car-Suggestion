import threading
from time import sleep
from tkinter import *

import VUI
import simulation


class GUI(threading.Thread):

    def __init__(self, comm):
        super().__init__()
        self.temperature = None
        self.scent = None
        self.speed = None
        self.play_pause_btn = None
        self.pause_img = None
        self.start_img = None
        self.temperature = None
        self.lower_frame = None
        self.voice_feedback = None  # output
        self.sim = simulation.Simulation()
        #self.sim.media_player.video_set_mouse_input(True)
        self.sim.start()
        self.command = comm
        self.vui = VUI.VUI(self.command)

    def consumer(self):
        """ consumer code """
        while True:
            if not self.command.empty():
                c = self.command.get()
                print("queue ")
                print(list(self.command.queue))
                self.consume_command(c)
            sleep(5)

    def consume_command(self, c):
        print("CONSUME")
        self.voice_feedback.config(text=c[0] + c[1])
        match c[0]:
            case "scenario":
                self.sim.load_video(c[1])
                self.command.task_done()
            case "speed":
                self.speed.config(text=c[1])
                self.command.task_done()
            case "scent":
                self.speed.config(text=c[1])
                self.command.task_done()
            case "temperature":
                self.speed.config(text=c[1])
                self.command.task_done()

    def play_pause(self):
        """ pauses and plays """
        self.sim.play_pause()
        if self.play_pause_btn.cget['image'] == self.pause_img:
            self.play_pause_btn.config(image=self.start_img)
        else:
            self.play_pause_btn.config(image=self.pause_img)

    def play_video(self, place, temperature, scent):

        self.scent.config(text=scent.get())
        self.speed.config(text="Medium")
        print("temp: " + temperature.get())
        if temperature.get() == "low":
            print("LOW")
            self.temperature.config(background="white")
        elif temperature.get() == "medium":
            print("MEDIUM")
            self.temperature.config(background="yellow")
        else:
            print("HIGH")
            self.temperature.config(background="red")
        self.sim.load_video(place.get())
    def run(self):

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
        self.speed = Label(top_frame, text='              ', padx=20,
                      font=('Helvetica', 16), justify='left')
        scents_lb = Label(top_frame, text='Scent: ', padx=20,
                          font=('Helvetica', 16), justify='left')
        self.scent = Label(top_frame, text='               ', padx=20,
                      font=('Helvetica', 16), justify='left')
        temperature_lb = Label(top_frame, text="Playing: ", padx=20,
                         font=('Helvetica', 16), justify='left')
        self.temperature = Label(top_frame, text='               ', padx=20,
                     font=('Helvetica', 16), justify='left')

        speed_lb.grid(row=0, column=0)
        self.speed.grid(row=0, column=1)
        scents_lb.grid(row=0, column=2)
        self.scent.grid(row=0, column=3)
        temperature_lb.grid(row=0, column=4)
        self.temperature.grid(row=0, column=5)

        # center_frame
        center_frame.rowconfigure(0, weight=1)
        center_frame.columnconfigure(0, weight=3)
        center_frame.columnconfigure(1, weight=1)
        center_frame.rowconfigure(1, weight=1)
        center_frame.rowconfigure(2, weight=1)
        center_frame.rowconfigure(3, weight=1)
        center_frame.rowconfigure(4, weight=1)
        center_frame.rowconfigure(5, weight=1)

        radioSimulationValue = StringVar(value="sea")

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
            command=lambda: self.play_video(radioSimulationValue, radioTemperatureValue, radioScentValue))
        buttonConfirm.grid(row=6, column=6)

        self.voice_feedback = Label(center_frame, background='cyan')
        self.voice_feedback.grid(row=0, column=0, columnspan=5, sticky=NSEW)

        str = Label(center_frame, text='......', padx=20, font=('Helvetica', 16), justify='left')
        str.grid(row=0, column=9)

        # Configure btm_frame  rows and columns
        self.start_img = PhotoImage(file=f"img/play.png")
        self.pause_img = PhotoImage(file=f"img/pause.png")
        self.play_pause_btn = Button(master=btm_frame, image=self.start_img, borderwidth=0, highlightthickness=0,
                                     relief="flat",
                                     # command=lambda: threading.Thread(target=self.play_pause).start())
                                     command=self.play_pause)
        slow_img = PhotoImage(file=f"img/slow.png")
        slow_btn = Button(master=btm_frame, image=slow_img, borderwidth=0, relief="flat",
                          command=self.sim.slowdown)
        fast_img = PhotoImage(file=f"img/fast.png")
        fast_btn = Button(master=btm_frame, image=fast_img, borderwidth=0, relief="flat",
                          command=self.sim.speedup)
        load_img = PhotoImage(file=f"img/load.png")
        load_btn = Button(master=btm_frame, image=load_img, borderwidth=0, highlightthickness=0, relief="flat",
                          command=lambda: self.sim.load_video("sim/prova.mkv"))
        voice_img = PhotoImage(file=f"img/003-microphone.png")
        voice_btn = Button(btm_frame, image=voice_img, borderwidth=0, highlightthickness=0, relief="flat",
                           command=lambda: threading.Thread(target=self.vui.start()))
        consumer_btn = Button(btm_frame, image=voice_img, borderwidth=0, highlightthickness=0, relief="flat",
                           command = lambda: threading.Thread(target=self.consumer()).start())
        #threading.Thread(target=self.vui.start())
        #threading.Thread(target=self.consumer()).start()


        load_btn.grid(row=0, column=0, sticky=EW)
        slow_btn.grid(row=0, column=1, sticky=EW)
        self.play_pause_btn.grid(row=0, column=2, sticky=EW)
        fast_btn.grid(row=0, column=4, sticky=EW)
        voice_btn.grid(row=0, column=5, sticky=EW)

        top_frame.grid(row=0, sticky=EW)
        center_frame.grid(row=1, sticky=NSEW)
        btm_frame.grid(row=2, sticky=EW)

        self.temperature = btm_frame

        root.mainloop()


def main():  # stuff to run always here such as class/def
    pass


if __name__ == "__main__":  # stuff only to run when not called via 'import' here
    main()
