# GeoStar Button Bar class
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

class GeoStarButtonBar(tk.Frame):
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
        i1 = self.buttonbar.add_icon(self.add_img,self.fileOpen)
        Tooltip(i1, text='Create a new file', wraplength=wraplength)

        #Open existing file
        i1 = Image.open("icon/folder.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.folder_img = ImageTk.PhotoImage(i2, master=self)
        i1 = self.buttonbar.add_icon(self.folder_img,self.fileOpen)
        Tooltip(i1, text='Open exising file', wraplength=wraplength)

        #Zoom in
        i1 = Image.open("icon/zoom-in.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.zoomIn_img = ImageTk.PhotoImage(i2, master=self)
        i1=self.buttonbar.add_icon(self.zoomIn_img,self.zoomIn)
        Tooltip(i1, text='Zoom-in', wraplength=wraplength)

        #Zoom out
        i1 = Image.open("icon/zoom-out.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.zoomOut_img = ImageTk.PhotoImage(i2, master=self)
        i1=self.buttonbar.add_icon(self.zoomOut_img,self.zoomOut)
        Tooltip(i1, text='Zoom-out', wraplength=wraplength)

        #Pan
        i1 = Image.open("icon/move-arrows.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.pan_img = ImageTk.PhotoImage(i2, master=self)
        i1=self.buttonbar.add_icon(self.pan_img,self.undo)
        Tooltip(i1, text='Pan', wraplength=wraplength)

        #Undo
        i1 = Image.open("icon/undo.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.undo_img = ImageTk.PhotoImage(i2, master=self)
        i1=self.buttonbar.add_icon(self.undo_img,self.undo)
        Tooltip(i1, text='Undo', wraplength=wraplength)

        #Redo
        i1 = Image.open("icon/redo.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.redo_img = ImageTk.PhotoImage(i2, master=self)
        i1=self.buttonbar.add_icon(self.redo_img,self.redo)
        Tooltip(i1, text='Redo', wraplength=wraplength)

        #Draw histogram
        i1 = Image.open("icon/histogram.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.histogram_img = ImageTk.PhotoImage(i2, master=self)
        i1=self.buttonbar.add_icon(self.histogram_img,self.createHistogram)
        Tooltip(i1, text='Histogram', wraplength=wraplength)

        #Plot on canvas
        i1 = Image.open("icon/target.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.plot_img = ImageTk.PhotoImage(i2, master=self)
        i1=self.buttonbar.add_icon(self.plot_img,self.plot)
        Tooltip(i1, text='Plot on canvas', wraplength=wraplength)

        #Settings
        i1 = Image.open("icon/settings-work-tool.png")
        i2 = ImageOps.fit(i1,(int(self.size),int(self.size)))
        self.settings_img = ImageTk.PhotoImage(i2, master=self)
        i1=self.buttonbar.add_icon(self.settings_img,self.settings)
        Tooltip(i1, text='Edit Settings', wraplength=wraplength)

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

    def fileCreate(self):
        self.event_publish(["GeoStarButtonBar::fileCreate"])
    
    def fileOpen(self):
        name = askopenfilename(initialdir=".",
                           filetypes =(("HDF5 Files", "*.h5"),("All Files","*.*")),
                           title = "Choose a file."
        )
        if(len(name)>0):
            ##messagebox.showinfo("Information","chosen filename= "+name)
            self.event_publish(["GeoStarButtonBar::fileOpen",name])
    
    def zoomIn(self):
        self.event_publish(["GeoStarButtonBar::viewZoomIn"])
    
    def zoomOut(self):
        self.event_publish(["GeoStarButtonBar::viewZoomOut"])

    def redo(self):
        self.event_publish(["GeoStarButtonBar::redo"])

    def undo(self):
        self.event_publish(["GeoStarButtonBar::undo"])

    def createHistogram(self):
        self.event_publish(["GeoStarButtonBar::histogram"])

    def histogram(self):
        isMask = messagebox.askyesno("Masking", "Mask image before creating histogram?")
        if isMask == True:
            print("Creating mask...")
            #create mask
            maskEntry = tk.Toplevel()
            maskEntry.title("Masking")
            tk.Label(maskEntry, text=("Enter top-left and bottom-right coordinates of the mask")).grid(row=0)
            tk.Label(maskEntry, text=("Top Left x")).grid(row=1, sticky=tk.W)
            tk.Label(maskEntry, text=("Top Left y")).grid(row=1, column=2, sticky=tk.W)
            tk.Label(maskEntry, text=("Bottom Right x")).grid(row=2, sticky=tk.W)
            tk.Label(maskEntry, text=("Bottom Right y")).grid(row=2, column=2, sticky=tk.W)
            tlx = tk.Entry(maskEntry).grid(row=1, column=1, sticky=tk.W)
            tly = tk.Entry(maskEntry).grid(row=1, column=3, sticky=tk.W)
            brx = tk.Entry(maskEntry).grid(row=2, column=1, sticky=tk.W)
            bry = tk.Entry(maskEntry).grid(row=2, column=3, sticky=tk.W)

            okButton = tk.Button(maskEntry, text=("OK"), command= lambda: self.create_mask(tlx.get(), tly.get(), brx.get(), bry.get())).grid(row=3, sticky=tk.W)
            cancelButton = tk.Button(maskEntry, text=("Cancel"), command=maskEntry.destroy).grid(row=3, column=1, sticky=tk.W)
        else:
            graphType = tk.Toplevel()
            graphType.title("Graph Type")
            tk.Label(graphType, text=("Choose a graph type")).grid(row=0)
            var = tk.StringVar(graphType)
            # default option
            var.set("Greyscale")
            option = tk.OptionMenu(graphType, var, "Greyscale", "RGB").grid(row=1)
            button = tk.Button(graphType, text="Ok", command= lambda: self.selectGraphType(var.get())).grid(row=2)

    def selectGraphType(self, type):
        print("Graph type selected: ", type)
        if type == "Greyscale":
            self.create_greyscale_graph()
        else:
            self.create_bgr_graph()

    def create_mask(self, tlx, tly, brx, bry):
        name = askopenfilename(initialdir=".",
                           filetypes =(("JPG File", "*.jpg"),("All Files","*.*")),
                           title = "Choose a file."
        )
        if(len(name)>0):
            ##messagebox.showinfo("Information","chosen filename= "+name)
            img = cv2.imread(name, 0)
            mask = np.zeros(img.shape, np.uint8)
            cv2.rectangle(mask, (int(tlx), int(tly)), (int(brx), int(bry)), (255, 255, 255), -1)
            masked_img = cv2.bitwise_and(img, img, mask=mask)
            
            hist_full = cv2.calcHist([img],[0],None,[256],[0,256])
            hist_mask = cv2.calcHist([img],[0],mask,[256],[0,256])

            plt.subplot(221), plt.imshow(img, 'gray')
            plt.subplot(222), plt.imshow(mask,'gray')
            plt.subplot(223), plt.imshow(masked_img, 'gray')
            plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask)
            plt.xlim([0,256])
            plt.show()

    def plot(self):
        self.event_publish(["GeoStarButtonBar::plot"])

    def settings(self):
        self.event_publish(["GeoStarButtonBar::settings"])

    def create_greyscale_graph(self):
        print("greyscale graph")
        name = askopenfilename(initialdir=".",
                           filetypes =(("HDF5 File", ".h5"),("All Files","*.*")),
                           title = "Choose a file."
        )
        if(len(name)>0):
            ##messagebox.showinfo("Information","chosen filename= "+name)
            img = cv2.imread(name, 0)
            plt.hist(img.ravel(), 256, [0, 256])
            plt.title('Greyscale Histogram of '+name)
            plt.show()
    
    def create_bgr_graph(self):
        name = askopenfilename(initialdir=".",
                           filetypes =(("JPG File", "*.jpg"),("All Files","*.*")),
                           title = "Choose a file."
        )
        if(len(name)>0):
            img = cv2.imread(name)
            color = ('b','g','r')
            for i,col in enumerate(color):
                histr = cv2.calcHist([img],[i],None,[256],[0,256])
                plt.plot(histr,color = col)
                plt.xlim([0,256])
            plt.show()
