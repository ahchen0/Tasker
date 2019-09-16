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

        file_menu = ["File", "New", self.fileNew, "Open", self.fileOpen,
                     "Quit", self.master.master.destroy]
        self.menubar.file=self.menubar.add_item(file_menu)

        edit_menu = ["Edit", "Undo", self.editUndo, "Redo", self.editRedo,
                     "Cut", self.editCut, "Copy", self.editCopy, "Paste", self.editPaste, "Draw", self.editDraw, "Edit Color Values", self.editColorValues]
        self.menubar.edit=self.menubar.add_item(edit_menu)

        view_menu = ["View", "Zoom In", self.viewZoomin, "Zoom Out", self.viewZoomout,
                     "Pan", self.viewPan, "Inverted Colors", self.viewInverted]
        self.menubar.view=self.menubar.add_item(view_menu)

        help_menu = ["Help", "Version", self.helpVersion, "Documentation", self.helpDocumentation]
        self.menubar.edit=self.menubar.add_item(help_menu)


    def event_subscribe(self, obj_ref):
        self.subscribers.append(obj_ref)

    def event_publish(self, cmd):
        for sub in self.subscribers:
            sub.event_receive(cmd)

    def event_receive(self,event):
        pass

    def fileNew(self):
        pass

    def fileOpen(self):
        name = askopenfilename(initialdir=".",
                           filetypes =(("HDF5 Files", "*.h5"),("All Files","*.*")),
                           title = "Choose a file."
        )
        if(len(name)>0):
            ##messagebox.showinfo("Information","chosen filename= "+name)
            self.event_publish(["TaskerMenuBar::fileOpen",name])

    def editUndo(self):
        pass

    def editRedo(self):
        pass

    def editCopy(self):
        pass

    def editCut(self):
        pass

    def editPaste(self):
        pass

    def editColorValues(self):
        t = tk.Toplevel(self)
        secondWin=editImageValues(t)

    def viewZoomin(self):
        self.event_publish(["TaskerMenuBar::viewZoomIn"])

    def viewZoomout(self):
        self.event_publish(["TaskerMenuBar::viewZoomOut"])

    def viewPan(self):
        self.event_publish(["TaskerMenuBar::viewPan"])

    def viewInverted(self):
        self.event_publish(["TaskerMenuBar::viewInverted"])

    def helpVersion(self):
        messagebox.showinfo("Version","Tasker GUI Version 0.0.1")

    def helpDocumentation(self):
        webbrowser.open("gui_help.html",new=1)


#added drawing window.
    def editDraw(self):
        """
        self.event_publish(["TaskerMenuBar::editDraw"])
        width = 200
        height = 200
        center = height//2
        white = (255, 255, 255)
        green = (0,128,0)
        def paint(event):
            # python_green = "#476042"
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
            cv.create_oval(x1, y1, x2, y2, fill="black",width=5)
            draw.line([x1, y1, x2, y2],fill="black",width=5)
        image1 = PIL.Image.new("RGB", (width, height), white)
        draw = ImageDraw.Draw(image1)
        """
        pass

class editImageValues(tk.Frame):
    def __init__(self, master):
        self.master=master
        button1=ttk.Button(self.master,text="f(x)=x",command=self.linearColor)
        button1.pack()
        button2=ttk.Button(self.master,text="f(x)=x^2",command=self.quadraColor)
        button2.pack()
        button3=ttk.Button(self.master,text="f(x)=x^1/2",command=self.sqrtColor)
        button3.pack()
        button4=ttk.Button(self.master,text="f(x)=logx",command=self.logColor)
        button4.pack()

    def linearColor(self):
        arr = []
        for i in range(256):
            arr.append(i)
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(arr,arr)
        canvas = FigureCanvasTkAgg(f,master=self.master)
        canvas.show()
        canvas.get_tk_widget().pack()
        canvas.draw()
        self.event_publish()


    def quadraColor(self):
        arr = []
        arr2 = []
        for i in range(256):
            arr.append(i)
            arr2.append(i*i)
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(arr,arr2)
        canvas = FigureCanvasTkAgg(f,master=self.master)
        canvas.show()
        canvas.get_tk_widget().pack()
        canvas.draw()
        self.event_publish()
        self.event_publish()

    def sqrtColor(self):
        arr = []
        arr2 = []
        for i in range(256):
            arr.append(i)
            arr2.append(math.sqrt(i))
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(arr,arr2)
        canvas = FigureCanvasTkAgg(f,master=self.master)
        canvas.show()
        canvas.get_tk_widget().pack()
        canvas.draw()
        self.event_publish()
        self.event_publish()
"""
    def logColor(self):
        arr = []
        arr2 = []
        for i in range(256):
            arr.append(i)
            b=math.log(i,2)
            b=math.floor(b)
            arr2.append()
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(arr,arr2)
        canvas = FigureCanvasTkAgg(f,master=self.master)
        canvas.show()
        canvas.get_tk_widget().pack()
        canvas.draw()
        self.event_publish()
        self.event_publish()
        """
