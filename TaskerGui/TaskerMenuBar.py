# Tasker Menu Bar class
import tkinter as tk
from tkinter import ttk
import math
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import webbrowser
from PIL import ImageTk, Image, ImageDraw
import PIL
from datetime import datetime, timedelta
from spacecraft2 import spacecraft
from multicolumnlistbox import MultiListbox

import MenuBar

class TaskerMenuBar(tk.Frame):
    """Creates the menubar for use in the Tasker GUI.
       Builds each of the menu items, and attaches functions to each.
    """
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.subscribers = []
        self.menubar = MenuBar.MenuBar(self)
        self.master.master.config(menu=self.menubar.menubar)

        file_menu = ["File", "Add Satellite", self.addSatellite, "Add Point", self.addPoint, "Quit", self.master.master.destroy]
        self.menubar.file=self.menubar.add_item(file_menu)

        edit_menu = ["Tools", "Scheduler", self.scheduler]
        self.menubar.edit=self.menubar.add_item(edit_menu)

        help_menu = ["Help", "Version", self.helpVersion, "Documentation", self.helpDocumentation]
        self.menubar.edit=self.menubar.add_item(help_menu)

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

    # Popup for adding points to the map
    def addPoint(self):
        popup = tk.Toplevel()
        popup.title("Add Point")

        pointNameDir = tk.Label(popup, text = "Enter Name")
        pointNameDir.pack()
        pointStartName = "Point " + str(len(self.master.treeview.pointList) + 1)
        self.pointName = tk.Entry(popup, width = 20, justify = "center", text = pointStartName)
        self.pointName.delete(0, tk.END)
        self.pointName.insert(tk.END, pointStartName)
        self.pointName.pack()

        latDir = tk.Label(popup, text = "Enter Latitude")
        latDir.pack()
        self.lat = tk.Entry(popup, width = 20, justify = "center", text = "0")
        self.lat.delete(0, tk.END)
        self.lat.insert(tk.END, "0")
        self.lat.pack()

        lonDir = tk.Label(popup, text = "Enter Longitude")
        lonDir.pack()
        self.lon = tk.Entry(popup, width = 20, justify = "center", text = "0")
        self.lon.delete(0, tk.END)
        self.lon.insert(tk.END, "0")
        self.lon.pack()

    def addPointToTree(self):
        pass # START HERE


    def event_subscribe(self, obj_ref):
        self.subscribers.append(obj_ref)

    def event_publish(self, cmd):
        for sub in self.subscribers:
            sub.event_receive(cmd)

    def event_receive(self,event):
        pass

    def helpVersion(self):
        messagebox.showinfo("Version","Tasker GUI Version 0.0.1")

    def helpDocumentation(self):
        webbrowser.open("gui_help.html",new=1)

    """ Popup for scheduler. Allows user to search for when a satellite is over selected
    coordinates within a range of time"""
    def scheduler(self):
        satList = []
        
        for sat in self.master.treeview.satList:
            satList.append(sat.name)

        if(len(satList) == 0):
            satList.append("No Satellites in Tree")

        popup = tk.Toplevel()
        popup.title("Scheduler")

        satDir = tk.Label(popup, text = "Satellite:")
        satDir.pack()
        self.satVar = tk.StringVar(popup)
        self.satVar.set(satList[0])
        satSelect = tk.OptionMenu(popup, self.satVar, *satList)
        satSelect.pack()

        latDir = tk.Label(popup, text = "\nLatitude (deg):")
        latDir.pack()
        self.lat = tk.Entry(popup, width = 20, justify = "center", text = "Latitude")
        self.lat.delete(0, tk.END)
        self.lat.insert(tk.END, str(0))
        self.lat.pack()

        longDir = tk.Label(popup, text = "\nLongitude (deg):")
        longDir.pack()
        self.long = tk.Entry(popup, width = 20, justify = "center", text = "Longitude")
        self.long.delete(0, tk.END)
        self.long.insert(tk.END, str(0))
        self.long.pack()

        timeStartDir = tk.Label(popup, text = "\nSearch Range Start\n(Format: YYYY:MM:DD:HH:MM:SS)")
        timeStartDir.pack()
        timeStartString = self.time2String(self.master.time)
        self.timeStart = tk.Entry(popup, width = 20, justify = "center", text = timeStartString)
        self.timeStart.delete(0, tk.END)
        self.timeStart.insert(tk.END, timeStartString)
        self.timeStart.pack()

        timeEndDir = tk.Label(popup, text = "\nSearch Range End\n(Format: YYYY:MM:DD:HH:MM:SS)")
        timeEndDir.pack()
        timeEndString = self.time2String(self.master.time + timedelta(days = 1))
        self.timeEnd = tk.Entry(popup, width = 20, justify = "center", text = timeEndString)
        self.timeEnd.delete(0, tk.END)
        self.timeEnd.insert(tk.END, timeEndString)
        self.timeEnd.pack()

        toleranceDir = tk.Label(popup, text = "\nTolerance (km):")
        toleranceDir.pack()
        self.tolerance = tk.Entry(popup, width = 20, justify = "center", text = "Tolerance")
        self.tolerance.delete(0, tk.END)
        self.tolerance.insert(tk.END, "1000")
        self.tolerance.pack()

        searchButton = tk.Button(popup, text = "Search", command = self.search)
        searchButton.pack()

    """ Performs the scheduler search function when the search button is pressed"""
    def search(self):
        if(self.satVar.get() == "No Satellites in Tree"):
            print("None selected")
            return

        timeStart = self.string2Time(self.timeStart.get())
        timeEnd = self.string2Time(self.timeEnd.get())

        # Search satList for spacecraft object
        for sat in self.master.treeview.satList:
            if(sat.name == self.satVar.get()):
                thisSat = sat

        time = self.master.canvas.plotter.search(thisSat, float(self.lat.get()), float(self.long.get()), 
                                            timeStart, timeEnd, float(self.tolerance.get()))

        

        if time is None:
            errorPopup = tk.Toplevel()
            errorPopup.title("No solution")
            errorMessage = tk.Label(errorPopup, \
                text = "No solution found for the given satellite and time range\nTry changing the time range or satellite")
            errorMessage.pack()
            return

        self.master.time = time
        self.master.canvas.plotter.updateAll()
        
    """ Converts a time in datetime format to a string"""
    def time2String(self, time):
        year = str(time.year)

        if(time.month < 10):
            month = "0" + str(time.month)
        else:
            month = str(time.month)

        if(time.day < 10):
            day = "0" + str(time.day)
        else:
            day = str(time.day)

        if(time.hour < 10):
            hour = "0" + str(time.hour)
        else:
            hour = str(time.hour)

        if(time.minute < 10):
            minute = "0" + str(time.minute)
        else:
            minute = str(time.minute)

        if(time.second < 10):
            second = "0" + str(time.second)
        else:
            second = str(time.second)

        return year + ":" + month + ":" + day + ":" + hour + ":" + minute + ":" + second

    """ Converts a time in string format to a datetime """
    def string2Time(self, timeString):
        time= []
        timeComponent = ""
        for i in timeString:
            if(i == ":"):
                time.append(int(timeComponent))
                timeComponent = ""
            else:
                timeComponent = timeComponent + i
        time.append(int(timeComponent))

        return datetime(time[0], time[1], time[2], time[3], time[4], time[5])