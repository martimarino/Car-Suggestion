from pathlib import Path

import pyttsx3
import vlc
import random
import PySimpleGUI as sg

import os
import speech_recognition as sr
import pyjokes
import datetime

'''initialize voice recognition'''
r = sr.Recognizer()
pyttsx3.init()
voice_data = ""

'''initialize video player'''
Instance = vlc.Instance()
player = Instance.media_player_new()

'''GUI'''
sg.theme("DarkBlue")

layout = [
    [sg.Input(key='-IN-', visible=False, enable_events=True),
     sg.FileBrowse(file_types=(("MP4 Files", "*.mp4"),), visible=False)],
    [sg.Text('Choose place'),
     sg.Combo(['Sea', 'Mountain', 'City', 'Highway', 'Forest'], key='place', readonly=True),
     sg.Text('Choose temperature'),
     sg.Combo(['Low', 'Medium', 'High'], key='temperature', readonly=True),
     sg.Text('Choose scent'),
     sg.Combo(['Peaches', 'Lavender', 'Cloves', 'Mushrooms'], key='scent', readonly=True),
     sg.ReadButton('Confirm')],
    [sg.ReadButton('Speak')],
    [sg.Text('Speed: '), sg.Text('', key='speed'),
     sg.Text('Temperature: '), sg.Text('', key='temp'),
     sg.Text('Scent: '), sg.Text('', key='scent_label')],
    [sg.Graph((640, 480), (0, 0), (640, 480), key='-CANVAS-')],
    [sg.Text('Output: '), sg.Text('', key='output')]
]
window = sg.Window('Car Suggestion', layout, finalize=True, icon='./img/icon.ico')

video_panel = window['-CANVAS-'].Widget.master
# set the window id where to render VLC's video output
h = video_panel.winfo_id()
player.set_hwnd(h)


def load_video(place):

    print("PLACE:" + place)
    list = []
    for file in os.listdir('sim'):
        file_name, file_extension = os.path.splitext(file)
        print(file, file_name)
        name = file_name.split("_")
        if name[0] in place:
            print(file_name, name[0])
            list.append(file)

    if list:
        choice = random.randint(0, len(list) - 1)
        print(choice, list[choice])
        m = Instance.media_new("./sim/" + list[choice])
    else:
        m = Instance.media_new("./sim/prova.mkv")

    player.set_media(m)
    player.play()

def change_speed(value):
    if value == 1:
        window['speed'].update(str(random.randint(40, 60)) + ' km/h')
    elif value == 0.5:
        window['speed'].update(str(random.randint(20, 40)) + ' km/h')
    elif value == 0.25:
        window['speed'].update(str(random.randint(10, 20)) + ' km/h')
    elif value == 2:
        window['speed'].update(str(random.randint(60, 80)) + ' km/h')
    elif value == 4:
        window['speed'].update(str(random.randint(80, 100)) + ' km/h')

def voice_rec():
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio, language='en-US')

            if 'take me to the' in voice_data:
                place = voice_data.replace('take me to the', '')
                load_video(place)
                window['speed'].update(str(random.randint(40, 60)) + ' km/h')

                set_GUI("temperature", "medium")

                if "sea" in place:
                    set_GUI("scent", "peaches")
                if "city" in place or "highway" in place:
                    set_GUI("scent", "lavender")
                if "mountain" in place:
                    set_GUI("scent", "cloves")
                if "forest" in place:
                    set_GUI("scent", "mushrooms")
                return

            if 'pause' in voice_data:
                player.pause()
                window['output'].update('pause')
                return

            if 'slow' in voice_data or 'slower' in voice_data or 'low' in voice_data:
                slow = voice_data.replace('slow', '')
                value = player.get_rate() / 2
                player.set_rate(value)
                change_speed(value)
                window['output'].update(slow)
                return

            if 'fast' in voice_data or 'faster' in voice_data:
                fast = voice_data.replace('fast', '')
                value = player.get_rate() * 2
                player.set_rate(value)
                change_speed(value)
                window['output'].update(fast)
                return

            if 'scent' in voice_data:
                scent = voice_data.replace('scent', '')
                window['scent'].update(scent)
                window['output'].update(scent)
                return

            if 'temperature' in voice_data:
                temperature = voice_data.replace('temperature', '')
                window['temp'].update(temperature)
                return

            if 'what' and 'time' in voice_data:  # shares the current time in 24hr format
                time = datetime.datetime.now().strftime('%H:%M')
                print(time)
                window['output'].update('Current time is ' + time)
                return

            if ("joke" or "jokes") in voice_data:  # tells a joke
                joke = pyjokes.get_joke()
                print(joke)
                window['output'].update(joke)
                return
            if "stop" in voice_data or "close" in voice_data:
                window['output'].update('Video stopped')
                player.stop()

        except sr.UnknownValueError:
            print('Did not understand')
            window['output'].update('Did not understand')

def change_colors(value):

    if "peaches" in value:
        window.close()
        sg.theme("Purple")
        # window = sg.Window('Car Suggestion', layout, finalize=True, icon='./img/icon.ico')
        # window['-CANVAS-'].update(background_color='#FFCBA4')
    elif "lavender" in value:
        window['-CANVAS-'].update(background_color='#CBC3E3')
    elif "cloves" in value:
        window['-CANVAS-'].update(background_color='#654321')
    elif "mushrooms" in value:
        window['-CANVAS-'].update(background_color='#013220')


def set_GUI(element, value):

    if element == "speed":
        window['speed'].update(value)
    elif element == "scent":
        window['scent_label'].update(value)
        change_colors(value)
    elif element == "temperature":
        window['temp'].update(value)
    elif element == "color":
        change_colors(value)


def play_video(place, scent, temperature):
    load_video(place)
    window['speed'].update(str(random.randint(40, 60)) + ' km/h')
    set_GUI("scent", scent)
    set_GUI("temperature", temperature)


while True:

    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-IN-':
        video = values[event]
        if Path(video).is_file():
            m = Instance.media_new(str(video))  # Path, unicode
            player.set_media(m)
            player.play()
    if event == 'Speak':
        voice_rec()
    elif event == 'Confirm':
        print("CONFIRM")
        place = values['place'].lower()
        temperature = values['temperature'].lower()
        scent = values['scent'].lower()
        play_video(place, scent, temperature)

player.stop()
window.close()