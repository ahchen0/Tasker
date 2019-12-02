#!/usr/bin/python3
## gui.py

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from TaskerMenuBar import TaskerMenuBar
from TaskerButtonBar import TaskerButtonBar
from TaskerTreeView import TaskerTreeView
from TaskerCanvas import TaskerCanvas
from PythonConsole import PythonConsole
from TaskerMap import TaskerMap, BrowserFrame, NavigationBar
from satCatScraper import Scraper
from TaskerStatusBar import TaskerStatusBar
from datetime import datetime, timezone
        
def stopProg(e):
    """
    Destroys the root
    """
    root.destroy()


class Application(tk.Frame):
    """
    Main application class for the Tasker

    :ivar Tk master: Parent class of application. Should be the tkinter root
    :ivar subscribers: List of subscribers
    :ivar TaskerMenuBar menubar: Menu bar of GUI
    :ivar TaskerButtonBar buttonbar: Button bar of GUI
    :ivar TaskerTreeView treeview: Satellite and point list of GUI
    :ivar TaskerCanvas canvas: Map canvas of GUI
    :ivar datetime time: The current time plotted in on the map
    :ivar TaskerStatusBar statusbar: The status bar of the GUI. Displays the current time plotted
    :param Tk master: Parent class of TaskerGui. Usually the root.
    """

    def __init__(self, master=None):
        scraper = Scraper()
        super().__init__(master)
        self.master = master
        self.subscribers=[]

        self.pack(fill=tk.BOTH,expand=True)

        self.create_widgets()

    def create_widgets(self):
        """
        Creates all GUI components.
        """

        self.master.title("Tasker")
        
        self.menubar = TaskerMenuBar(self)
        self.menubar.pack(side="top",fill=tk.X,expand=False)
 
        self.buttonbar = TaskerButtonBar(self,size=28)
        self.buttonbar.pack(side="top",fill=tk.X,expand=False)
        
        self.treeview = TaskerTreeView(self,font_size=12, width=300)
        self.treeview.pack(side="left", fill=tk.Y, expand=False)
        self.menubar.event_subscribe(self.treeview)
        self.buttonbar.event_subscribe(self.treeview)

        self.canvas = TaskerCanvas(self,500,500)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)
        self.event_subscribe(self.canvas)

        self.time = datetime.now()
        self.statusbar = TaskerStatusBar(self)
        self.statusbar.pack(side="bottom", fill=tk.X, expand = False)
        self.event_subscribe(self.statusbar)

        self.treeview.event_subscribe(self.canvas)
        self.buttonbar.event_subscribe(self.canvas)
        self.menubar.event_subscribe(self.canvas)

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
        if len(event) > 0:
            type = event[0]
            ## determine if its an event we care about....
        else:
            return

    def paned_window_resized(self,event):
        """
        Called when paned window is resized
        """
        # print("app publishing window-resize event")
        self.event_publish(["TaskerApp::paned_window_resized",event])
        # self.map.on_mainframe_configure(event.width, event.height)


    
## MAIN:
if __name__ == "__main__":
    root=tk.Tk()
    App=Application(master=root)
    App.mainloop()
