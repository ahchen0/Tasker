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
    """
    Creates the buttonbar for use in the Tasker GUI.
    Builds each of the button items, and attaches functions to each.

    :ivar Application master: Parent application of the menu bar
    :ivar subscribers: List of subscribers
    :ivar ButtonBar buttonbar: The tkinter buttonbar
    :param Application master: The parent application of the button bar
    :param int size: The size of the button bar
    """
    def __init__(self, master = None, size=32):
        tk.Frame.__init__(self, master)
        self.master = master
        self.size=size
        self.subscribers = []
        self.buttonbar = ButtonBar.ButtonBar(self)
        wraplength=200

        #Set time
        i1 = Image.open("icon/clock.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.set_time_img = ImageTk.PhotoImage(i2, master=self)
        i1 = self.buttonbar.add_icon(self.set_time_img, self.setTime)
        Tooltip(i1, text="Set time", wraplength=wraplength)

        #Zoom in
        i1 = Image.open("icon/zoom-in.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.zoom_in_img = ImageTk.PhotoImage(i2, master=self)
        i1 = self.buttonbar.add_icon(self.zoom_in_img, self.zoomIn)
        Tooltip(i1, text="Zoom in", wraplength=wraplength)
        self.zoomInEnabled = False

        #Zoom out
        i1 = Image.open("icon/zoom-out.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.zoom_out_img = ImageTk.PhotoImage(i2, master=self)
        i1 = self.buttonbar.add_icon(self.zoom_out_img, self.zoomOut)
        Tooltip(i1, text="Zoom out", wraplength=wraplength)
        self.zoomOutEnabled = False

        #Exit
        i1 = Image.open("icon/error.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.exit_img = ImageTk.PhotoImage(i2, master=self)
        i1=self.buttonbar.add_icon(self.exit_img,self.master.master.destroy)
        Tooltip(i1, text='Exit', wraplength=wraplength)

    def event_subscribe(self, obj_ref):
        """
        Subscribes obj_ref to the TaskerGui.

        :param obj_ref: object to be subscribed to TaskerGui
        """
        self.subscribers.append(obj_ref)

    def event_publish(self, cmd):
        """
        Publishes an event to all subscribers

        :param str cmd: Command to be published
        """

        for sub in self.subscribers:
            sub.event_receive(cmd)

    def event_receive(self,event):
        """
        Receives an event from a subscription

        :param event: The event received from a subscription
        """

        pass

    def zoomIn(self):
        """
        Called when the zoomIn button is clicked
        """
        if not self.zoomInEnabled:
            if(self.zoomOutEnabled):
                self.master.canvas.disableZoomOut()
                self.zoomOutEnabled = False
            self.master.canvas.enableZoomIn()
            self.zoomInEnabled = True
        else:
            self.master.canvas.disableZoomIn()
            self.zoomInEnabled = False

    def zoomOut(self):
        """
        Called when the zoomOut button is clicked
        """
        if not self.zoomOutEnabled:
            if(self.zoomInEnabled):
                self.master.canvas.disableZoomIn()
                self.zoomInEnabled = False
            self.master.canvas.enableZoomOut()
            self.zoomOutEnabled = True
        else:
            self.master.canvas.disableZoomOut()
            self.zoomOutEnabled = False

    def setTime(self):
        """
        Creates the setTime popup
        """
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
        """
        Changes the currently plotted time to the time selected by the user in the setTime popup
        """
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        hour = int(self.hour.get())
        minute = int(self.minute.get())
        second = int(self.second.get())
        self.master.time = datetime(year, month, day, hour, minute, second)
        self.master.statusbar.update(self.master.time)
        self.master.canvas.plotter.updateAll()

