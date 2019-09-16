#!/usr/bin/python3
# Advanced zoom example. Like in Google Maps.
# It zooms only a tile, but not the whole image. So the zoomed tile occupies
# constant memory and not crams it with a huge resized image for the large zooms.
#import random

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyautogui
#import random
from random import randint
import cv2
import h5py
import numpy as np
from matplotlib import pyplot as plt
from pylab import *
from tkinter import messagebox

trace = 0
plotButton = False
raster = "default"

class xy():
    def __init__(self):
        self.x=0
        self.y=0

        
class GeoStarCanvas(ttk.Frame):
    ''' Advanced zoom of the image '''
    def __init__(self, mainframe, width=500, height=500):
        ''' Initialize the main Frame '''
        ttk.Frame.__init__(self, master=mainframe)

        self.parent = mainframe
        
        # Vertical and horizontal scrollbars for canvas
        vbar = tk.Scrollbar(self, orient='vertical')
        hbar = tk.Scrollbar(self, orient='horizontal')
        
        # Create canvas and put image on it
        self.canvas_width = width
        self.canvas_height = height
        self.canvas = tk.Canvas(self, width=self.canvas_width, 
                                height=self.canvas_height, bg='black',
                                highlightthickness=0, ##scrollregion=(0,0,500,500),
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        hbar.pack(side="bottom",fill=tk.X,expand=True)
        vbar.pack(side="right",fill=tk.Y,expand=True)
        self.canvas.pack(side="top",fill=tk.BOTH,expand=True)

        vbar.configure(command=self.scroll_y)
        hbar.configure(command=self.scroll_x)
        
        # Bind events to the Canvas
        #self.canvas.bind('<Configure>', self.show_image)  # canvas is resized ####################Not sure what this does
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up

        self.canvas.bind('<Double-Button-1>', self.zoomin)
        self.canvas.bind('<Double-Button-3>', self.zoomout)

        
        self.imscale = 1.0  # scale for the canvas image
        self.delta = 1.3  # zoom/unzoom magnitude
        
        self.subscribers = []

        self.init_pct()

        self.imagemode="gray" ## gray, rgb, pct

        self.init_rgb()

        self.canvas.after(1000, lambda: self.parent.bind("<Configure>", self.on_resize_parent) )

    def init_pct(self):
        """
        create a random pct, just testing for now....
        """
        self.pct=[]
        for i in range(255):
            red = randint(0,255)
            green = randint(0,255)
            blue = randint(0,255)
            self.pct.append(red)
            self.pct.append(green)
            self.pct.append(blue)

    def init_rgb(self):
        """
        Initialize rgb arrays to all 0
        """
        self.image_data_red  =np.zeros((self.canvas_width,self.canvas_height))
        self.image_data_green=np.zeros((self.canvas_width,self.canvas_height))
        self.image_data_blue =np.zeros((self.canvas_width,self.canvas_height))

            
    def on_resize_parent(self,event):
        """
        Called when app is resized.
        """
        #print("parent event size="+str(event.width)+" X "+str(event.height))
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)
        self.show_image()
        
    def on_resize_parentx(self,event):
        """
        Called only by Panedwindow to resize in x-dir only.
        """
        ##print("parent event size="+str(event.width)+" X "+str(event.height))
        self.canvas_width = event.width
        self.canvas.config(width=self.canvas_width)
        self.show_image()
 
    def event_subscribe(self, obj_ref):
        self.subscribers.append(obj_ref)
    
    def event_publish(self, cmd):
        for sub in self.subscribers:
            sub.event_receive(cmd)
    
    def event_receive(self,event):     #Event can be an array, where the event name is first
        if len(event) > 0:             #Details for the event "like filename come later
            type = event[0]
            #print("Canvas::event_receive, type=",type)
            #messagebox.showinfo("Information","Canvas::event_receive, type="+type+", length="+str(len(event)))
            if type == "GeoStarTreeView::select":
                if len(event)>1:
                    #messagebox.showinfo("Information","Canvas::event_receive, event1="+event[1])
                    if event[1] == "raster":
                        rastername = event[2]
                        imagename  = event[3]
                        filename   = event[4]
                        self.rasterSelect(filename,imagename,rastername)
                        
            elif type == "GeoStarTreeView::raster_menu_select":
                if len(event) == 5:
                    choice = event[1]
                    rastername = event[2]
                    imagename= event[3]
                    filename = event[4]
                    self.rasterChoiceSelect(choice,filename,imagename,rastername)
                        
            elif ( type == "GeoStarButtonBar::zoomIn" or
                   type == "GeoStarMenuBar::viewZoomIn" ):
                xy.x, xy.y = pyautogui.position()
                self.zoomin(xy)
            elif( type == "GeoStarButtonBar::plot"):
                if plotButton == False:
                    self.plotPoint()
                else:
                    self.canvas.bind('<ButtonPress-1>', self.move_from)
                    self.canvas.bind('<B1-Motion>',     self.move_to)
                    self.canvas.bind('<Double-Button-1>', self.zoomin)
            elif ( type == "GeoStarButtonBar::zoomOut" or
                   type == "GeoStarMenuBar::viewZoomOut" ):
                xy.x, xy.y = pyautogui.position()
                self.zoomout(xy)
            elif( type == "GeoStarButtonBar::grayScale"):
                self.grayScale()
            elif(type == "GeoStarButtonBar::histogram"):
                self.greyscaleHistogram()
            elif(type == "GeoStarApp::paned_window_resized"):
                self.on_resize_parentx(event[1])
        else:
            return

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image

    def zoomout(self,event):
        ''' Zoom-in with double-click on mouse-btn-1 '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0

        i = min(500, 500)
        if int(i * self.imscale) < 30: return  # image is less than 30 pixels
        self.imscale /= self.delta
        scale        /= self.delta

        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()
    
    def zoomin(self,event):
        ''' Zoom-in with double-click on mouse-btn-1 '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0
        
        i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
        if i < self.imscale: return  # 1 pixel is bigger than the visible area
        self.imscale *= self.delta
        scale *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()
        
    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(500, 500)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()
    
    def fileSelect(self, filename):
        #print("HERE")
        self.filename=filename
        f = h5py.File(filename, 'r')
        dset = f['key']
        data = np.array(dset[:,:,:])
        file = 'test.jpg'
        cv2.imwrite(file, data)
        self.image = Image.open(file)  # open image
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle(0, 0, 500, 500, width=0)
        self.show_image()

    def rasterSelect(self,filename,imagename,rastername):
        ## for now, just show the selected raster:
        ## later need to be fancier.....
        #messagebox.showinfo("Information","GeoStarCanvas::rasterSelect: inputs= "+filename+", "+imagename+", "+rastername)
        f = h5py.File(filename, 'r')
        rasterpath = "/"+imagename+"/"+rastername
        dset=f[rasterpath]
        data = np.array(dset[:,:])
        #messagebox.showinfo("Information","GeoStarCanvas::rasterSelect: data.shape= "+str(data.shape[0])+", "+str(data.shape[1]) )
        self.image = Image.fromarray(data)
        self.image = self.image.convert('L') # converts to grayscale
        self.image = self.image.crop((0,0,500,500))
        self.container = self.canvas.create_rectangle(0, 0, 500, 500, width=0)
        #self.greyscaleHistogram(rastername)
        global raster
        raster = rastername
        #print(rastername, raster)
        self.show_image()

    def rasterChoiceSelect(self,choice,filename,imagename,rastername):
        ## for now, just show the selected raster:
        ## later need to be fancier.....
        #messagebox.showinfo("Information","GeoStarCanvas::rasterChoiceSelect: inputs= "+choice+", "+filename+", "+imagename+", "+rastername)
        if choice == "gray":
            self.rasterGraySelect(filename,imagename,rastername)
        elif choice == "pct":
            self.rasterPCTSelect(filename,imagename,rastername)
        elif choice == "red":
            self.rasterRGBSelect(choice,filename,imagename,rastername)
        elif choice == "green":
            self.rasterRGBSelect(choice,filename,imagename,rastername)
        elif choice == "blue":
            self.rasterRGBSelect(choice,filename,imagename,rastername)
        
    def rasterGraySelect(self,filename,imagename,rastername):
        self.init_rgb()
        f = h5py.File(filename, 'r')
        rasterpath = "/"+imagename+"/"+rastername
        dset=f[rasterpath]
        data = np.array(dset[:,:])
        #messagebox.showinfo("Information","GeoStarCanvas::rasterSelect: data.shape= "+str(data.shape[0])+", "+str(data.shape[1]) )
        #print("GeoStarCanvas::rasterSelect: data.shape= "+str(data.shape[0])+", "+str(data.shape[1]) )
        self.image = Image.fromarray(data)
        self.image = self.image.convert('L') # converts to grayscale
        self.image = self.image.crop((0,0,self.canvas_width,self.canvas_height))
        self.container = self.canvas.create_rectangle(0,0,self.canvas_width,self.canvas_height)
        #self.greyscaleHistogram(rastername)
        global raster
        raster = rastername
        #print(rastername, raster)
        self.imagemode="gray"
        self.show_image()
       
    def rasterPCTSelect(self,filename,imagename,rastername):
        self.init_rgb()
        f = h5py.File(filename, 'r')
        rasterpath = "/"+imagename+"/"+rastername
        dset=f[rasterpath]
        data = np.array(dset[:,:])
        #messagebox.showinfo("Information","GeoStarCanvas::rasterSelect: data.shape= "+str(data.shape[0])+", "+str(data.shape[1]) )
        self.image = Image.fromarray(data)
        self.image = self.image.convert('L') # converts to grayscale
        self.image = self.image.crop((0,0,self.canvas_width,self.canvas_height))
        self.image.putpalette(self.pct)
        self.container = self.canvas.create_rectangle(0,0,self.canvas_width,self.canvas_height)
        #self.greyscaleHistogram(rastername)
        global raster
        raster = rastername
        #print(rastername, raster)
        self.imagemode="pct"
        self.show_image()
       
    def rasterRGBSelect(self,choice,filename,imagename,rastername):
        if self.imagemode != "rgb":
            self.init_rgb()
        f = h5py.File(filename, 'r')
        rasterpath = "/"+imagename+"/"+rastername
        dset=f[rasterpath]
        data = np.array(dset[:,:])
        if choice == "red":
            self.image_data_red = data
        elif choice == "green":
            self.image_data_green = data
        elif choice == "blue":
            self.image_data_blue = data
        #messagebox.showinfo("Information","GeoStarCanvas::rasterSelect: data.shape= "+str(data.shape[0])+", "+str(data.shape[1]) )
        self.imageR = Image.fromarray(self.image_data_red,mode='L')
        #self.imageR = self.imageR.convert('L') # converts to grayscale
        self.imageR = self.imageR.crop((0,0,self.canvas_width,self.canvas_height))
        
        self.imageG = Image.fromarray(self.image_data_green,mode='L')
        #self.imageG = self.imageG.convert('L') # converts to grayscale
        self.imageG = self.imageG.crop((0,0,self.canvas_width,self.canvas_height))
        
        self.imageB = Image.fromarray(self.image_data_blue,mode='L')
        #self.imageB = self.imageB.convert('L') # converts to grayscale
        self.imageB = self.imageB.crop((0,0,self.canvas_width,self.canvas_height))

        self.image = Image.merge("RGB",[self.imageR, self.imageG, self.imageB])
        
        self.container = self.canvas.create_rectangle(0,0,self.canvas_width,self.canvas_height)
        #self.greyscaleHistogram(rastername)
        global raster
        raster = rastername
        #print(rastername, raster)
        self.imagemode="rgb"
        self.show_image()

    def getRed(self, redVal):
        return '#%02x%02x%02x' % (redVal, 0, 0)
    
    def getGreen(self, greenVal):
        return '#%02x%02x%02x' % (0, greenVal, 0)
    
    def getBlue(self, blueVal):
        return '#%02x%02x%02x' % (0, 0, blueVal)

    def rgbHistogram(self, image):
        # Get the color histogram of the image
        histogram = image.histogram()
        for i, value in enumerate(image.histogram()):
            print(i, value)
        # Take only the Red counts
        l1 = histogram[0:256]
        # Take only the Blue counts
        l2 = histogram[256:512]
        # Take only the Green counts
        l3 = histogram[512:768]
        
        plt.figure(0)
        # R histogram
        for i in range(0, 256):
            plt.bar(i, l1[i], color = self.getRed(i), edgecolor=self.getRed(i), alpha=0.3)
        # G histogram
        plt.figure(1)
        for i in range(0, 256):
            plt.bar(i, l2[i], color = self.getGreen(i), edgecolor=self.getGreen(i),alpha=0.3)
        # B histogram
        plt.figure(2)
        for i in range(0, 256):
            plt.bar(i, l3[i], color = self.getBlue(i), edgecolor=self.getBlue(i),alpha=0.3)
        plt.show()
    
    def greyscaleHistogram(self):
        print("Generating greyscale histogram for", raster)
        histogram = self.image.histogram()
        plt.title("Greyscale Histogram of " + raster)
        plt.hist(histogram, 256, [0, 256])
        plt.show()

    def plotPoint(self):
        # xy.x, xy.y = pyautogui.position()
        # event = xy
        # x = self.canvas.canvasx(event.x)
        # y = self.canvas.canvasy(event.y)

        # print(pyautogui.position())

        # x0 = self.canvas.canvasx(x)
        # y0 = self.canvas.canvasy(y)
        # x1 = x0 + 10
        # y1 = y0 + 10
        # color = 'yellow'
        # self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        plotButton == True
        self.canvas.bind('<ButtonPress-1>', self.onStart)   
        self.canvas.bind('<B1-Motion>',     self.onGrow)     
        self.canvas.bind('<Double-1>',      self.onClear)     
        self.canvas.bind('<ButtonPress-3>', self.onMove)     
        self.drawn  = None
        self.kinds = [self.canvas.create_oval, self.canvas.create_rectangle]

    def onStart(self, event):
        self.shape = self.kinds[0]
        self.kinds = self.kinds[1:] + self.kinds[:1]      
        self.start = event
        self.drawn = None
    def onGrow(self, event):                           
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = self.shape(self.start.x, self.start.y, event.x, event.y, fill = 'yellow', tag = 'shape')
        if trace: print(objectId)
        self.drawn = objectId
    def onClear(self, event):
        event.widget.delete('shape')                     
    def onMove(self, event):
        if self.drawn:                                   
            if trace: print(self.drawn)
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            canvas.move(self.drawn, diffX, diffY)
            self.start = event


    def grayScale(self):
        # self.filename=filename
        # self.image = Image.open(filename)  # open image
        self.image = self.image.convert('L') # converts to grayscale
        # self.container = self.canvas.create_rectangle(0, 0, 500, 500, width=0)
        self.show_image()

    def show_image(self, event=None):
        ''' Show image on the Canvas '''

        if not hasattr(self,'image'):
            self.image = Image.new("L",(self.canvas_width,self.canvas_height) )  # create black image
        # Put image into container rectangle and use it to set proper coordinates to the image
        if not hasattr(self,'container'):
            self.container = self.canvas.create_rectangle(0, 0, self.canvas_width,self.canvas_height, width=0)

        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.canvas_width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.canvas_height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
