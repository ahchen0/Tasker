#!/usr/bin/python3
## gui.py

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from GeoStarMenuBar import GeoStarMenuBar
from GeoStarButtonBar import GeoStarButtonBar
from GeoStarTreeView import GeoStarTreeView
from GeoStarCanvas import GeoStarCanvas
from PythonConsole import PythonConsole
        
def stopProg(e):
    root.destroy()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.subscribers=[]

        self.pack(fill=tk.BOTH,expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.master.title("GeoStar")
        
        self.menubar = GeoStarMenuBar(self)
        self.menubar.pack(side="top",fill=tk.X,expand=False)
 
        self.buttonbar = GeoStarButtonBar(self,size=28)
        self.buttonbar.pack(side="top",fill=tk.X,expand=False)

        self.big_paned_window = tk.PanedWindow(self,orient="vertical",showhandle=True,sashrelief=tk.RAISED)
        self.big_paned_window.pack(side="top",fill=tk.BOTH,expand=True)


        self.paned_window = tk.PanedWindow(self,orient="horizontal",showhandle=True,sashrelief=tk.RAISED)
        self.big_paned_window.add(self.paned_window)
        
        self.treeview = GeoStarTreeView(self,font_size=12)
        self.paned_window.add(self.treeview)
        self.menubar.event_subscribe(self.treeview)
        self.buttonbar.event_subscribe(self.treeview)

        self.canvas = GeoStarCanvas(self,500,500)
        self.event_subscribe(self.canvas)
        self.paned_window.bind("<Configure>",self.paned_window_resized)
        
        self.paned_window.add(self.canvas)
        self.treeview.event_subscribe(self.canvas)
        self.buttonbar.event_subscribe(self.canvas)
        self.menubar.event_subscribe(self.canvas)

        self.python_console = PythonConsole(self)
        self.big_paned_window.add(self.python_console)
        

    def event_subscribe(self, obj_ref):
        self.subscribers.append(obj_ref)
    
    def event_publish(self, cmd):
        for sub in self.subscribers:
            sub.event_receive(cmd)
    
    def event_receive(self,event):     #Event can be an array, where the event name is first
        if len(event) > 0:             #Details for the event, like filename, come later
            type = event[0]
            ## determine if its an event we care about....
        else:
            return

    def paned_window_resized(self,event):
        """
        Called when paned window is resized
        """
        ##print("app publishing window-resize event")
        self.event_publish(["GeoStarApp::paned_window_resized",event])

    
## MAIN:
if __name__ == "__main__":
    root=tk.Tk()
    App=Application(master=root)
    App.mainloop()
