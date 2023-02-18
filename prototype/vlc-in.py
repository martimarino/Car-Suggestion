from pathlib import Path

import pyttsx3
import vlc
import random
import PySimpleGUI as sg

import os
from fuzzywuzzy import fuzz
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
    [sg.Text('Choose place'), sg.Combo(['Sea', 'Mountain', 'City', 'Highway', 'Forest'], key='place'),
     sg.Text('Choose temperature'), sg.Combo(['Low', 'Medium', 'High'], key='temperature'),
     sg.Text('Choose scent'),
     sg.Combo(['Peaches', 'Lavender', 'Cloves', 'Mushrooms'], key='scent'),
     sg.ReadButton('Confirm')],
    [sg.ReadButton('Speak')],
    [sg.Text('Speed: '), sg.Text('', key='speed'),
     sg.Text('Temperature: '), sg.Text('', key='temp'),
     sg.Text('Scent: '), sg.Text('', key='scent')],
    [sg.Graph((640, 480), (0, 0), (640, 480), key='-CANVAS-')],
    [sg.Text('Output: '), sg.Text('', key='output')]
]
window = sg.Window('Car Suggestion', layout, finalize=True, icon='./img/icon.ico')

video_panel = window['-CANVAS-'].Widget.master
# set the window id where to render VLC's video output
h = video_panel.winfo_id()
player.set_hwnd(h)


def load_video(place):
    # for file in os.listdir('sim'):
    #     # if place in file:
    #     ratio = fuzz.ratio(place.lower(), file.lower())
    #     print(file, ratio)
    #
    #     if ratio > 50:
    #         m = Instance.media_new('./sim/' + file)  # Path, unicode
    #     else:
    #         m = Instance.media_new('./sim/sea.mp4')  # Path, unicode
    #     player.set_media(m)
    #     player.play()

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
        media_player = vlc.MediaPlayer("./sim/" + list[choice])
    else:
        media_player = vlc.MediaPlayer("./sim/prova.mkv")

    media_player.play()
    media_player.audio_set_volume(100)

def voice_rec():
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio, language='en-US')

            if 'take me to the' in voice_data:
                place = voice_data.replace('take me to the', '')
                m = Instance.media_new('./sim/sea.mp4')  # Path, unicode
                player.set_media(m)
                player.play()
                print(place)
                window['speed'].update(str(random.randint(40, 60)) + ' km/h')
                return

            if 'pause' in voice_data:
                player.pause()
                window['output'].update('pause')
                return

            if 'slow' in voice_data or 'slower' in voice_data:
                slow = voice_data.replace('slow', '')
                player.set_rate(player.get_rate() / 2)

                window['output'].update(slow)
                return

            if 'fast' in voice_data or 'faster' in voice_data:
                fast = voice_data.replace('fast', '')
                player.set_rate(player.get_rate() * 2)
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


def set_GUI(element, value):
    match element:
        case "speed":
            window['speed'].update(value)
        case "scent":
            print("VALUE", value)
            window['scent'].update(value)
            #change_colors(value.lower())
        case "temperature":
            window['temperature'].update(value)
        case "color":
            print("color")
            #change_colors(value.lower())


def play_video(place, scent, temperature):
    load_video(place)
    set_GUI("speed", "normal")
    set_GUI("scent", scent.lower())
    set_GUI("temperature", temperature.lower())


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
        place = values['place']
        temperature = values['temperature']
        scent = values['scent']
        play_video(place, temperature, scent)

player.stop()
window.close()