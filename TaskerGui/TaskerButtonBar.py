# Tasker Button Bar class
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox, simpledialog
import cv2
import numpy as np
from matplotlib import pyplot as plt
from Tooltip import Tooltip
from PIL import Image, ImageTk, ImageOps


import ButtonBar

class TaskerButtonBar(tk.Frame):
	def __init__(self, master = None, size=32):
		tk.Frame.__init__(self, master)
		self.master = master
		self.size=size
		self.subscribers = []
		self.buttonbar = ButtonBar.ButtonBar(self)
		wraplength=200

		#Buttons start here
		#Create new file, not implemented, doing the same thing as open file
		i1 = Image.open("icon/add-file.png")
		i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
		self.add_img = ImageTk.PhotoImage(i2, master=self)
		i1 = self.buttonbar.add_icon(self.add_img,self.addSatellite)
		Tooltip(i1, text='Create a new file', wraplength=wraplength)

		#Exit
		i1 = Image.open("icon/error.png")
		i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
		self.exit_img = ImageTk.PhotoImage(i2, master=self)
		i1=self.buttonbar.add_icon(self.exit_img,self.master.master.destroy)
		Tooltip(i1, text='Exit', wraplength=wraplength)

	def event_subscribe(self, obj_ref):
		self.subscribers.append(obj_ref)

	def event_publish(self, cmd):
		for sub in self.subscribers:
			sub.event_receive(cmd)

	def event_receive(self,event):
		pass

	def addSatellite(self):
		popup = tk.Toplevel()
		popup.title("Add satellites")
		listbox = tk.Listbox(popup)

		with open("satCat.txt") as file:
			for line in file:
				listbox.insert(tk.END, line)
		listbox.pack()
