# Button Bar class
import tkinter as tk
from tkinter import ttk

class ButtonBar(tk.Frame):
    """ButtonBar allows creating button bars more easily by providing
       2 functions for adding buttons: add_button() and add_icon().
       For example:
         self.buttonbar.add_button("fileOpen",self.fileOpen);
        
         self.photo1 = tk.PhotoImage(file="gear.gif")
         self.buttonbar.add_icon(self.photo1,self.master.destroy)

       :param TaskerButtonBar master: parent class
    
    """
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master=master
        self.pack(side="top",anchor="w",fill=tk.X,expand=True)
        
    def add_button(self,txt,cmd):
        """
        Adds a button to the button bar

        :param str txt: button description
        :param cmd: function to call when button is clicked
        """

        i1= tk.Button(self, text=txt, command=cmd)
        i1.pack(side="left")
        return i1

    def add_icon(self,icon,cmd):
        """
        Adds an icon to the button bar

        :param Image icon: the icon to display for the button
        :param cmd: function to call when the button is clicked
        """
        i1=tk.Button(self, image=icon, command=cmd)
        i1.configure(background="white")
        i1.pack(side="left")
        return i1
