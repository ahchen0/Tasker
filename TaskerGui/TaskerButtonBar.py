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
from datetime import datetime

import ButtonBar
from spacecraft2 import spacecraft
from multicolumnlistbox import MultiListbox

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

        #Set time
        i1 = Image.open("icon/clock.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.set_time_img = ImageTk.PhotoImage(i2, master=self)
        i1 = self.buttonbar.add_icon(self.set_time_img, self.setTime)
        Tooltip(i1, text="Set time", wraplength=wraplength)

    def event_subscribe(self, obj_ref):
        self.subscribers.append(obj_ref)

    def event_publish(self, cmd):
        for sub in self.subscribers:
            sub.event_receive(cmd)

    def event_receive(self,event):
        pass


    def setTime(self):
        popup = tk.Toplevel()
        popup.title("Set Time")

        yearDir = tk.Label(popup, text = "Year:")
        yearDir.pack()
        self.year = tk.Entry(popup, width = 15, justify = "center", text = "Year")
        self.year.delete(0, tk.END)
        self.year.insert(tk.END, str(self.master.time.year))
        self.year.pack()

        monthDir = tk.Label(popup, text = "\nMonth:")
        monthDir.pack()
        self.month = tk.Entry(popup, width = 15, justify = "center", text = "Month")
        self.month.delete(0, tk.END)
        self.month.insert(tk.END, str(self.master.time.month))
        self.month.pack()

        dayDir = tk.Label(popup, text = "\nDay:")
        dayDir.pack()
        self.day = tk.Entry(popup, width = 15, justify = "center", text = "Day")
        self.day.delete(0, tk.END)
        self.day.insert(tk.END, str(self.master.time.day))
        self.day.pack()

        hourDir = tk.Label(popup, text = "\nHour:")
        hourDir.pack()
        self.hour = tk.Entry(popup, width = 15, justify = "center", text = "Hour")
        self.hour.delete(0, tk.END)
        self.hour.insert(tk.END, str(self.master.time.hour))
        self.hour.pack()

        minuteDir = tk.Label(popup, text = "\nMinute:")
        minuteDir.pack()
        self.minute = tk.Entry(popup, width = 15, justify = "center", text = "Minute")
        self.minute.delete(0, tk.END)
        self.minute.insert(tk.END, str(self.master.time.minute))
        self.minute.pack()

        secondDir = tk.Label(popup, text = "\nSecond:")
        secondDir.pack()
        self.second = tk.Entry(popup, width = 15, justify = "center", text = "Second")
        self.second.delete(0, tk.END)
        self.second.insert(tk.END, str(self.master.time.second))
        self.second.pack()

        setButton = tk.Button(popup, text = "Set", command = self.updateTime)
        setButton.pack()

    def updateTime(self):
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        hour = int(self.hour.get())
        minute = int(self.minute.get())
        second = int(self.second.get())
        self.master.time = datetime(year, month, day, hour, minute, second)
        self.master.canvas.plotter.updateAll()

    
    def addSatellite(self):
        # Read in satellite catalog
        data = []
        self.catalog = []
        file = open("satCat.txt", "r")
        lines = file.readlines()
        lineNum = 0
        while(lineNum < len(lines)):
            name = lines[lineNum]
            line1 = lines[lineNum + 1]
            line2 = lines[lineNum + 2]
            lineNum = lineNum + 3
            item = spacecraft(name, line1, line2)
            self.catalog.append(item)
            data.append(item.name)
            data.append(item.catalogNumber)
            data.append(item.intlDesignator)
 
        popup = tk.Toplevel()
        popup.title("Add satellites")
        self.listbox = MultiListbox(popup, ["Name", "Catalog Number", "Intl Designator"], height = 30)
        self.listbox.add_data(data)
        self.listbox.selectmode = tk.EXTENDED
        self.listbox.pack(fill = tk.BOTH, expand = 1)

        addButton = tk.Button(popup, text = "Add", command = self.addSatelliteToTree)
        addButton.pack()

    def addSatelliteToTree(self):
        if self.listbox.selectedRow is not None:
            self.event_publish(["TaskerButtonBar::addSatellite", self.catalog[self.listbox.selectedRow]])
            self.master.canvas.plotter.plot(sat = self.catalog[self.listbox.selectedRow])
        else:
            print("Couldn't add spacecraft. No spacecraft selected")

