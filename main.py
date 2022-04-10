import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import ThemedTk  # themes for GUi

# global variables
paused = False
muted = False

# initialising the window object
root = ThemedTk(theme="clearlooks")

# mixer
mixer.init()  # initialising the mixer

playlist = []  # all file path added in this


def browseFile():
    global file_path
    file_path = filedialog.askopenfilename()  # open the selected file
    add_to_playlist(file_path)


def add_to_playlist(filename):
    global file_path
    filename = os.path.basename(filename)
    index = 0
    songList.insert(index, filename)
    playlist.insert(index, file_path)
    index += 1


def del_song():
    selected_song = songList.curselection()
    selected_song = int(selected_song[0])
    songList.delete(selected_song)
    playlist.pop(selected_song)


def playMusic():
    global paused
    if paused:
        paused = False
        mixer.music.unpause()
        statusbar["text"] = "Music resumed"
    else:
        try:
            stopMusic()  # stopping when switching the songs in list
            time.sleep(1)  # as we have thread at sleep of 1 sec
            selected_list_song = songList.curselection()
            selected_song_index = int(selected_list_song[0])
            selected_song_path = playlist[selected_song_index]
            mixer.music.load(selected_song_path)
            mixer.music.play()
            show_details(selected_song_path)
            statusbar["text"] = f"Playing {os.path.basename(selected_song_path)}"

        except:
            tkinter.messagebox.showerror("OOPS", "Sorry! i can't play this :(")


def stopMusic():
    global paused
    if paused:
        paused = False
    mixer.music.stop()
    statusbar["text"] = "Music Stopped "


def pauseMusic():
    global paused
    paused = True
    mixer.music.pause()
    statusbar["text"] = " Music Paused"


def set_val(val):
    volume = float(val) / 100  # scale send value in string and mixer takes from 0 to 1 only
    mixer.music.set_volume(volume)


def start_count(t):
    global paused
    runtime = 0
    while runtime <= t and mixer.music.get_busy():  # .get_busy() gives 0,1
        if paused:
            continue
        else:
            mins, secs = divmod(runtime, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentTimeLabel["text"] = "Current Time" + ' - ' + timeformat
            time.sleep(1)  # takes 1 second
            runtime += 1


# function to mute and volume up the music
def muteMusic():
    global muted
    if muted:
        volumeButton.config(image=volumePhoto)
        mixer.music.set_volume(0.7)
        scale.set(70)
        muted = False
    else:
        volumeButton.config(image=mutePhoto)
        mixer.music.set_volume(0)
        scale.set(0)
        muted = True


def show_details(song):
    file_data = os.path.splitext(song)  # split the filename for extension

    if file_data[1] == ".mp3":
        audio = MP3(song)
        total_length = audio.info.length

    else:
        a = mixer.Sound(song)
        total_length = a.get_length()

    # div - total_length/60, mpd-total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    timeLabel["text"] = "Total Length" + ' - ' + timeformat

    thread = threading.Thread(target=start_count, args=(total_length,))  # to keep away interpreter being busy in loop
    thread.start()


def closeWindow():
    stopMusic()
    root.destroy()


# menubar
menubar = Menu(root)
root.config(menu=menubar)  # to config at top

# status bar
statusbar = ttk.Label(root, text="Welcome to AMP \m/", relief=SUNKEN, anchor='w', font='ariel 10 italic')
statusbar.pack(fill='x', side='bottom')

# create submenu
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='file', menu=subMenu)

subMenu.add_command(label='open', command=browseFile)
subMenu.add_command(label="Exit", command=root.destroy)

# window title,icon and size
root.title("AMP")
root.iconbitmap(r'images/amp.ico')
root.geometry('200x350')

# frames
topFrame = Frame(root)
topFrame.pack(pady=10)

middleFrame2 = Frame(root)
middleFrame2.pack(anchor="w", padx=5)

middleFrame = Frame(root)
middleFrame.pack(pady=10, anchor="w", padx=5)

bottomFrame = Frame(root)
bottomFrame.pack(pady=5, padx=5, anchor="w")

# text labels

timeLabel = ttk.Label(topFrame, text='Time --:--')
timeLabel.pack()
currentTimeLabel = ttk.Label(topFrame, text='--:--', relief=GROOVE)
currentTimeLabel.pack()

# images
playPhoto = PhotoImage(file='images/play.png')
stopPhoto = PhotoImage(file='images/stop.png')
pausePhoto = PhotoImage(file='images/pause.png')
volumePhoto = PhotoImage(file='images/volume.png')
mutePhoto = PhotoImage(file='images/mute.png')
plusPhoto = PhotoImage(file='images/plus.png')
delPhoto = PhotoImage(file='images/delete.png')

# list box for songs
songList = Listbox(middleFrame2)
songList.configure(bg="lightblue")
songList.pack(side=LEFT)

# List box buttons
addButton = ttk.Button(middleFrame2, image=plusPhoto, command=browseFile)
addButton.pack()
delButton = ttk.Button(middleFrame2, image=delPhoto, command=del_song)
delButton.pack()

# buttons
playButton = ttk.Button(middleFrame, image=playPhoto, command=playMusic)  # play button
playButton.grid(row=0, column=0)

stopButton = ttk.Button(middleFrame, image=stopPhoto, command=stopMusic)  # stop button
stopButton.grid(row=0, column=1)

pauseButton = ttk.Button(middleFrame, image=pausePhoto, command=pauseMusic)  # pause button
pauseButton.grid(row=0, column=2)

# volume control
scale = ttk.Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_val)
scale.set(60)
mixer.music.set_volume(0.6)
scale.grid(row=0, column=1)

# mute and volume in bottom frame
volumeButton = ttk.Button(bottomFrame, image=volumePhoto, command=muteMusic)  # volume button
volumeButton.grid(row=0, column=0)

# overriding cross button
root.protocol("WM_DELETE_WINDOW", closeWindow)

# to make window visible
root.mainloop()
