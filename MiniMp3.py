import Tkinter
import tkFileDialog
import traceback
from win32com.client import Dispatch
import sys, thread
import tkMessageBox
import time
import os.path
from Queue import Queue
from threading import Thread
from functools import partial
from multiprocessing.pool import Pool

class media_dl:
	def _init_(self, root):
		self.root = root
		menu = Tkinter.Menu(self.root)
		#Tkinter.Button(self.root, text = 'shit', width = 5).pack()
		#Tkinter.Menu part
		submenu = Tkinter.Menu(menu, tearoff = 0)
		submenu.add_command(label = 'Open file', command = self.open_file)
		menu.add_cascade(label = 'File', menu = submenu)
		submenu = Tkinter.Menu(menu, tearoff = 0)
		submenu.add_command(label = 'Author', command = self.info)
		submenu.add_command(label = 'Demo', command = self.demo)
		menu.add_cascade(label = 'Info', menu = submenu)
		self.root.config(menu = menu)

		#frame_up
		frame_up = Tkinter.Frame( self.root, bd = 5)
		self.playList = Tkinter.Text(frame_up, width = 40, height = 5)
		self.playList.bind("<KeyPress>", lambda e: "break")
		self.playList.pack(side = Tkinter.LEFT)
		frame_up.place( x=10, y = 0)

		#frame_down
		frame_down = Tkinter.Frame(self.root, bd = 5)
		global wordsList
		wordsList = Tkinter.Text(frame_down, width = 40, height = 20)
		wordsList.pack(side = Tkinter.LEFT)
		frame_down.place( x=10, y = 100)
		
		#power
		self.wmp = Dispatch('WMPlayer.OCX')

		#button
		b1 = Tkinter.Button(self.root, text = "Previous", width = 10, height = 1, command = self.previous)
		b2 = Tkinter.Button(self.root, text = "Play", width = 10, height = 1, command = self.play)
		b3 = Tkinter.Button(self.root, text = "Next", width = 10, height = 1, command = self.next)
		b4 = Tkinter.Button(self.root, text = "Pause", width = 10, height = 1, command = self.pause)
		b5 = Tkinter.Button(self.root, text = "Stop", width = 10, height = 1, command = self.stop)
		b6 = Tkinter.Button(self.root, text = "Exit", width = 10, height = 1, command = self.ex)
		b1.place(x = 385, y = 130)
		b2.place(x = 385, y = 170)
		b3.place(x = 385, y = 210)
		b4.place(x = 385, y = 250)
		b5.place(x = 385, y = 290)
		b6.place(x = 385, y = 330)

		#Scale
		self.volume = Tkinter.IntVar()
		scale = Tkinter.Scale(self.root, variable = self.volume, orient = Tkinter.HORIZONTAL, length = 315, command = self.vol)
		scale.set(50)
		scale.place(x = 20, y = 430)

		self.root.minsize(500, 500)
		self.root.mainloop()

	def open_file(self):
		global cfile,fullname,name
		cfile = tkFileDialog.askopenfilename(title = "Python Music Player", filetypes = [("MP3","*.mp3"),("WMA","*.wma"),("WAV","*.wav")])
		fullname = os.path.basename(cfile)
		name = os.path.splitext(fullname)[0]
		if cfile:
			media = self.wmp.newMedia(cfile)
			self.wmp.currentPlaylist.appendItem(media)
			self.playList.insert(Tkinter.END, name + '\n')

	def play(self):
		self.wmp.controls.play()
		cfile = self.wmp.currentMedia.getItemInfo('sourceURL')
		#self.words(cfile)
		thread.start_new_thread( self.words, (cfile,) )

	def pause(self):
		self.wmp.controls.pause()

	def stop(self):
		self.wmp.controls.stop()

	def next(self):
		self.wmp.controls.next()
		wordsList.delete(0.0,Tkinter.END)
		cfile = self.wmp.currentMedia.getItemInfo('sourceURL')
		#print (cfile)
		self.words(cfile)
		#print "Next"

	def previous(self):
		self.wmp.controls.previous()

	def mainloop(self):
		self.root.minsize(500, 500)
		self.root.mainloop()

	def info(self):
		tkMessageBox.showinfo("my author", "I am made by DL")

	def vol(self, none):
		self.wmp.settings.Volume = self.volume.get()

	def ex(self):
		sys.exit()

	def demo(self):
		file = "demo.mp3"
		if file:
			filename = os.path.splitext(file)[0] 
			media = self.wmp.newMedia(file)
			self.playList.insert(Tkinter.END, file + '\n')
			self.wmp.currentPlaylist.appendItem(media)
			self.wmp.controls.play()
			self.words(filename)
		else: self.playList.insert(Tkinter.END, 'None!')

	def words(self,file):
		fullname = os.path.basename(file)
		name = os.path.splitext(fullname)[0]
		'''f =  open('%s.txt'%name,'r')
		for each in f:
			self.wordsList.insert(Tkinter.END, each + '\n')
		f.close()'''
		a=[]
		b=[]
		c=[]
		d=[]
		with open (u'%s.txt'%name,'r') as lrc:
			for line in lrc:
				wtime = int(line[1:3])*6000+int(line[4:6])*100+int(line[7:9])
				#print(line[1:3],line[4:6],line[7:9])
				a.append(wtime)
				words = line[10:]
				b.append(words)
			for j in range(len(a)):
				eval = a[j]-a[j-1]
				c.append(eval)
				#print('c is %s'%c[j])
				d = c[1:]
				#print('d is %s'%d)
			for i in range(len(d)):
				time.sleep(d[i]/100)
				#self.wordsList.clear()
				#timer = threading.Timer(d[i]/100, self.insert(b[i]))
				#timer.start()
				wordsList.delete(1.0,2.0)
				wordsList.insert(Tkinter.END, b[i] + '\n')
				wordsList.tag_config(b[i], foreground="green")
				#print(b[i])
	#def insert(self,words):
		#self.wordsList.insert(Tkinter.END, words + '\n')

def runmp3():
	root = Tkinter.Tk()
	root.title("DL music player")
	root.iconbitmap("warning")
	media = media_dl()
	media._init_(root)
	#with Pool(2) as p:
		#p.map(runmp3,media.words(cfile))

runmp3()
'''class test(Thread):
	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue
	def run(self):
		while True:
			# Get the work from the queue and expand the tuple
			cfile = self.queue.get()
			#download_link(directory, link)
			self.queue.task_done()

def main():
	runmp3()
	queue = Queue()
	for x in range(4):
		t = test(queue)
		# Setting daemon to True will let the main thread exit even though the workers are blocking
		t.daemon = True
		t.start()
		# Put the tasks into the queue as a tuple
		queue.put(words,(cfile))
		print(cfile)
		# Causes the main thread to wait for the queue to finish processing all the tasks
		queue.join()'''