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

    def event_subscribe(self, obj_ref):
        self.subscribers.append(obj_ref)

    def event_publish(self, cmd):
        for sub in self.subscribers:
            sub.event_receive(cmd)

    def event_receive(self,event):
        pass


    """
    def addSatellite(self):
        # Read in satellite catalog
        data = []
        with open("satCat.txt", "r") as file:
            for line in file:
                item = spacecraft(line)
                data.append(item.intlDesignator)
                data.append(item.catalogNumber)
                data.append(item.name)
                data.append(item.source)
                data.append(item.launchDate)
                data.append(item.launchSite)
                data.append(item.decayDate)

        popup = tk.Toplevel()
        popup.title("Add satellites")
        # listbox = tk.Listbox(popup, width = 132, selectmode = tk.EXTENDED)
        listbox = MultiListbox(popup, ["Intl Designator", "Catalog Number", "Name", "Source", "Launch Date", \
                                        "Launch Site", "Decay Date"], height = 30)
        listbox.add_data(data)
        listbox.selectmode = tk.EXTENDED
        listbox.pack()
    """

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
            self.master.canvas.plotter.plot(satName = self.catalog[self.listbox.selectedRow].name)
        else:
            print("Couldn't add spacecraft. No spacecraft selected")

