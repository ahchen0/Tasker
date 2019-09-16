# Menu Bar class
import tkinter as tk
from tkinter import ttk

class MenuBar(tk.Frame):
    """MenuBar allows creating menubars more easily by providing 
       an "add_item" method that take a simple list to define one
       menu-bar heading.
       For example:
       file_menu = ["File", "Open", self.fileOpen, "quit", self.master.destroy]
       self.menubar.item1=self.menubar.add_item(file_menu)

       This can be called as often as needed to create all the items 
       in a menubar.
    """
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.menubar = tk.Menu()

    def add_item(self,thelist):
        item = tk.Menu(self.menubar, tearoff=0)
        for i in range(1,len(thelist),2):
            item.add_command(label=thelist[i], command=thelist[i+1])
        self.menubar.add_cascade(label=thelist[0], menu=item)
        return item

