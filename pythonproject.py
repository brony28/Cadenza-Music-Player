import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import ttk
from ttkthemes import themed_tk as tk
import time
import threading
import pyaudio
import numpy as np
from tkinter.colorchooser import askcolor


# BackGround to the root window...incase u need it
def background():  # Background Colour

    (triple,color) = askcolor()

    if color:

       root.config(background=color)


playlist = []  # contains the full path + file name

# Gives the fliename of the selected song
def browse_file():
	global filename_path
	filename_path = filedialog.askopenfilename()
	print(filename_path)
	addplaylist(filename_path)

# Displays the filename in the listbox
def addplaylist(filename):
	filename = os.path.basename(filename)
	index = 0
	listbox.insert(index, filename)  # contains the file name
	playlist.insert(index, filename_path)
	print(playlist)
	index += 1

# Deletes the filename from the listbox
def del_file():
	selected_song = listbox.curselection()  # Gives the song which is selected
	selected_song = int(selected_song[0])
	listbox.delete(selected_song)
	playlist.pop(selected_song)




# Audio visualizer : Added just for fun
def visualfun():
	CHUNK = 2 ** 11
	RATE = 44100

	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
					frames_per_buffer=CHUNK)

	# for i in range(int(10*44100/1024)): #go for a few seconds
	while (True):
		data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
		peak = np.average(np.abs(data)) * 2
		bars = "#" * int(50 * peak / 2 ** 16)
		# print("%04d %05d %s"%(i,peak,bars))
		print("%s" % bars)

	stream.stop_stream()
	stream.close()
	p.terminate()


# Displays the Develeopers name
def about_us():
	tkinter.messagebox.showinfo('Devs', 'Ritson \nRony \nNevin \nNachiketh')  # (title of box,Information)

# Displays the Develeopers conmtact details
def contact_us():
	tkinter.messagebox.showinfo('Gmail:', 'Ritson Mathews <ritsonmathews@gmail.com> \nRony <ronybenny2812@gmail.com> \nNevin <nevinjoseph847@gmail.com> \nNachiketh ')  # (title of box,Information)




# DETAILS OF THE SELECTED MUSIC,: MP3 OR WAV
def show_details(play_song):
	text2['text'] = "Playing Now..." + '  ' + os.path.basename(play_song)
	filetype = os.path.splitext(play_song)
	if filetype[1] == '.mp3':
		audio = MP3(play_song)
		total_length = audio.info.length
	else:
		a = mixer.Sound(play_song)  # Only works for WAV file....
		total_length = a.get_length()

	# print(total_length)
	mins, secs = divmod(total_length, 60)  # div-totallength/60 and mod-totallength%60
	mins = round(mins)
	secs = round(secs)
	timeformat = '{:02d}:{:02d}'.format(mins, secs)
	# print(timeformat)
	lengthlabel['text'] = "Total Length : " + timeformat
	# the whole block of codes works for .wav files

	t1 = threading.Thread(target=start_count, args=(total_length,))  # See video no 20 from min 12
	t1.start()


# GIVES THE MUSIC TIME COUNTER
def start_count(c):
	global paused
	current_time = 0
	# mixer.music.get_busy(): Return a FALSE value when we press STOP BUTTON and music stops playing
	while current_time <= c and mixer.music.get_busy():  # For decreasing counter # Remove x=0 & while c and mixer.music.get_busy():
		if paused:
			continue
		else:
			mins, secs = divmod(current_time, 60)  # div-totallength/60 and mod-totallength%60
			mins = round(mins)
			secs = round(secs)
			timeformat = '{:02d}:{:02d}'.format(mins, secs)
			currenttimelabel['text'] = "Current Time : " + timeformat
			time.sleep(1)
			current_time += 1  # c -= 1

# EXECUTES on PLAY button click
def play_but():
	global paused
	if paused:
		mixer.music.unpause()
		statusbar['text'] = "Music resumed"
		paused = FALSE
	else:
		try:
			stop_but()
			time.sleep(1)
			selected_song = listbox.curselection()  # Gives the song which is selected
			selected_song = int(selected_song[0])
			print(selected_song)

			play_it = playlist[selected_song]
			print(play_it)
			# mixer.music.load(filename_path)
			mixer.music.load(play_it)
			mixer.music.play()
			print("Music will get loaded")
			# statusbar['text']="Playing music"+' '+filename_path (shows the entire file path)
			statusbar['text'] = "Playing music" + '  ' + os.path.basename(play_it)
			show_details(play_it)
		except:
			print("Select the file")
			tkinter.messagebox.showerror('Error', 'Select the file')  # (title

# EXECUTES on STOP button click
def stop_but():
	mixer.music.stop()
	print("Music stopped")
	statusbar['text'] = "Music stopped"


# EXECUTES on PAUSE button click
paused = FALSE
def pause_but():
	global paused
	paused = TRUE
	mixer.music.pause()
	statusbar['text'] = "Music paused"

# EXECUTES on REWIND button click
def rewind_but():
	play_but()
	statusbar['text'] = "Music rewinded"

# EXECUTES on VOLUME bar
def set_volume(val):
	volume = float(val) / 100
	mixer.music.set_volume(volume)

# EXECUTES on MUTE/SPEAKER button click
muted = FALSE
def mute_but():
	global muted
	if muted:  # Unmute the music
		mixer.music.set_volume(0.5)
		aud_volume.configure(image=speakeraudio)
		scale.set(50)
		statusbar['text'] = "Music unmuted"
		muted = FALSE

	else:  # Mute the music
		mixer.music.set_volume(0)
		aud_volume.configure(image=muteaudio)
		scale.set(0)
		statusbar['text'] = "Music muted"
		muted = TRUE

# EXECUTES on clicking CROSS button
def on_closing():
	tkinter.messagebox.showinfo('Prank', "You have been pranked..thiss window will not close")
	stop_but()
	root.destroy()

mixer.init()  # initialising the mixer


# MAIN FRAME START
# MUSIC BOX GEOMETRIC VALUES
root = tk.ThemedTk()
root.geometry('700x400')# specifies the window size
root.title("Cadenza RN^2")
root.iconbitmap(r'icons/headphone.ico')  # r: raw string : used to enter a location
root.get_themes()  # Returns a list of all themes that can be set
root.set_theme("radiance")  # Sets an available theme


# DISPLAY THE DEFAULT LINE
text1 = ttk.Label(root,
				  text='Cadenza Player',font='Verdana 20 bold',relief=RAISED, anchor=N)  # Creates a label widget. Parameters: (windowname,text which is to be written)
text1.pack(side=TOP, fill=X,pady=10)  # displays text(label) widget on the window
# pady=10 : gives space to the Y axis Label


# STATUS BAR
statusbar = ttk.Label(root, text="Welcome to Music player", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

# DEVS NAME BAR
label1 = ttk.Label(root, text="Devs: Ritson Rony Nevin Nachiketh", relief=SUNKEN, anchor=E, font='Times 10 bold')
label1.pack(side=BOTTOM, fill=X)

# TOP BAR MENU
menubar = Menu(root)  # creates empty top menu bar
root.config(menu=menubar)  # configures the menu bar..like fixing the position of bar,adding sub menus in the bar

# FILE MENU
submenu = Menu(menubar, tearoff=0)  # check video 8
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Audio visualizer ",command=visualfun)
submenu.add_command(label="BgColor ",command=background)
submenu.add_command(label="Exit", command=root.destroy)

# COLLECTION MENU
submenu = Menu(menubar, tearoff=0)  # check video 8
menubar.add_cascade(label="Collection", menu=submenu)
submenu.add_command(label="Classic")
submenu.add_command(label="Pop")
submenu.add_command(label="Relaxing")

# HELP MENU
submenu = Menu(menubar, tearoff=0)  # check video 8
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=about_us)
submenu.add_command(label="Contact Us", command=contact_us)
submenu.add_command(label="Version")

# LEFT FRAME
leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=20)

# PLAYLIST BAR
playlistbar = ttk.Label(leftframe, text="PLayList ", relief=GROOVE, font='Times 10 italic')
playlistbar.pack(pady=10)

# MUSIC LIST BOX
listbox = Listbox(leftframe)
listbox.pack()

# ADD MUSIC BUTTON
addbutton = ttk.Button(leftframe, text='Add >', command=browse_file)
addbutton.pack(side=LEFT)

# DELETE MUSIC BUTTON
delbutton = ttk.Button(leftframe, text='Delete <', command=del_file)
delbutton.pack(side=LEFT)

# LEFT FRAME
rightframe = Frame(root)
# rightframe.config(background='orange')
rightframe.pack(padx=20)

# INSIDE RIGHT FRAME , We have 3 sub frame : topframe, middleframe and bottomframe
# TOP FRAME
topframe = Frame(rightframe)
# topframe.config(background='green')
topframe.pack()

# DISPLAY THE MUSIC NAME AT THE TOP
text2 = ttk.Label(topframe)  # Creates a label widget. Parameters: (windowname,text which is to be written)
text2.pack(side=TOP)

# DISPLAY THE TOTAL TIME OF THE SONG
lengthlabel = ttk.Label(topframe, text="Total Length : --:--",
						font='Arial 10 bold')  # Creates a label widget. Parameters: (windowname,text which is to be written)
lengthlabel.pack(pady=10)

# DISPLAY THE REAL LIVE TIME OF THE SONG
currenttimelabel = ttk.Label(topframe, text="Current Time : --:--", relief=GROOVE, font='Arial 10 italic')
currenttimelabel.pack(pady=10)

# MIDDLE FRAME
middleframe = Frame(rightframe)  # FOr play,stop,pause buttons
# middleframe.config(background='green')
middleframe.pack(padx=10, pady=10)

# BOTTOMFRAME
bottomframe = Frame(rightframe)
#bottomframe.config(background='green')
bottomframe.pack()

# PLAY BUTTON
playaudio = PhotoImage(file='icons/play.png')
aud = ttk.Button(middleframe, image=playaudio, command=play_but)
aud.grid(row=0, column=0, padx=10)

# STOP BUTTON
stopaudio = PhotoImage(file='icons/stop.png')
audstop = ttk.Button(middleframe, image=stopaudio, command=stop_but)
audstop.grid(row=0, column=1, padx=10)

# PAUSE BUTTON
pauseaudio = PhotoImage(file='icons/pause.png')
audpause = ttk.Button(middleframe, image=pauseaudio, command=pause_but)
audpause.grid(row=0, column=2, padx=10)



# REWIND BUTTON ##FOr rewind,mute buttons,volume scale
rewindaudio = PhotoImage(file='icons/rewind.png')
audrewind = ttk.Button(bottomframe, image=rewindaudio, command=rewind_but)
audrewind.grid(row=0, column=0, padx=10)

# MUTE & SPEAKER BUTTON
muteaudio = PhotoImage(file='icons/mute.png')
speakeraudio = PhotoImage(file='icons/speaker.png')
aud_volume = ttk.Button(bottomframe, image=speakeraudio, command=mute_but)
aud_volume.grid(row=0, column=1, padx=10)

# VOLUME
scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL,
				  command=set_volume)  # default orientation is vertical
scale.set(50)
mixer.music.set_volume(0.5)
scale.grid(row=0, column=2, pady=10)


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

