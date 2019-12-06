# Tasker treeview class
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import h5py
import matplotlib.pyplot as plt
from tkinter import PhotoImage
from TreeViewPlus import TreeViewPlus
from PIL import Image, ImageTk, ImageOps
from TaskerPoint import Point

import MenuBar

class TaskerTreeView(tk.Frame):
        """
        Creates the Treeview for use in the Tasker GUI.

        :ivar spacecraft[] satList: List of satellites plotted
        :ivar Point[] pointList: List of points plotted
        :ivar masterList: List of satellites and points plotted
        :param Application master: The parent application of the treeview
        :param int width: the width of the tree view
        :param int height: the height of the tree view
        :param strfont_name: the font used for the text in the tree
        :param int font_size: the font size used for the text in the tree
        :param str font_color: the font color used for the text in the tree
        :param str indicator_foreground: the indicator foreground color
        :param str background: the background color
        """

        satList = []
        pointList = []
        masterList = []

        def __init__(self, master, width=500, height=500,
                                  font_name="Times", font_size=12, font_color="black",
                                  indicator_foreground="black", background="white"):
                tk.Frame.__init__(self, master)
                self.master = master
                self.subscribers = []
                self.openFiles = []
                self.ids = []

                self.width=width
                self.height=height
                self.font_name = font_name
                self.font_size=font_size
                self.font_color=font_color
                self.indicator_foreground=indicator_foreground
                self.background=background
                self.treeview = TreeViewPlus(self,  width=self.width, height=self.height,
                                             font_name=self.font_name,
                                             font_size=self.font_size,
                                             font_color=self.font_color,
                                             indicator_foreground=self.indicator_foreground,
                                             background=self.background)
                self.treeview.pack(side="left",fill=tk.BOTH,expand=True)

                self.treeview.bind('<<TreeviewSelect>>',self.select)
                ##self.treeview.bind('<<TreeviewMenuSelect>>',self.menu_select)

                self.red_square = ImageTk.PhotoImage(Image.new("RGB",(self.font_size,self.font_size),color="red"), master=self)
                self.grn_square = ImageTk.PhotoImage(Image.new("RGB",(self.font_size,self.font_size),color="green"), master=self)
                self.blu_square = ImageTk.PhotoImage(Image.new("RGB",(self.font_size,self.font_size),color="blue"), master=self)
                self.gry_square = ImageTk.PhotoImage(Image.new("RGB",(self.font_size,self.font_size),color="gray"), master=self)
                self.pct_square = ImageTk.PhotoImage(self.create_pct_square(self.font_size), master=self)
                self.wht_square = ImageTk.PhotoImage(self.create_white_square(self.font_size), master=self)

                i1  = self.create_image_icon()
                i2 = ImageOps.fit(i1,(int(1.5*self.font_size),int(1.5*self.font_size)))
                self.image_icon = ImageTk.PhotoImage(i2, master=self)
                #self.image_icon = ImageTk.PhotoImage(i1, master=self)




        #########################################################################
        def create_image_icon(self):
                """
                creates a new square image (140X140) that looks like 3 layers 
                of RGB.
                """
                newimdata = []
                red = (255, 0, 0, 255)
                grn = (0, 255, 0, 255)
                blu = (0, 0, 255, 255)
                tra = (0, 0, 0, 0)
                slope =7./4.

                for line in range(140):
                        for pixel in range(140):
                                newimdata.append(tra)

                
                ## blue box:
                for line in range(40):
                        line1=60+line
                        for pixel in range(140):
                                index = line1*140+pixel
                                if pixel >= -slope*(line1-60)+70 and pixel <= slope*(line1-60)+70:
                                        newimdata[index] = blu
                for line in range(40):
                        line1=60+40+line
                        for pixel in range(140):
                                index = line1*140+pixel
                                if pixel >= slope*(line1-60)-70 and pixel <= -slope*(line1-60)+210:
                                        newimdata[index] = blu
                
                ## green box:
                for line in range(40):
                        line1=30+line
                        for pixel in range(140):
                                index = line1*140+pixel
                                if pixel >= -slope*(line1-30)+70 and pixel <= slope*(line1-30)+70:
                                        newimdata[index] = grn
                for line in range(40):
                        line1=30+40+line
                        for pixel in range(140):
                                index = line1*140+pixel
                                if pixel >= slope*(line1-30)-70 and pixel <= -slope*(line1-30)+210:
                                        newimdata[index] = grn
                
                ## red box:
                for line in range(40):
                        for pixel in range(140):
                                index = line*140+pixel
                                if pixel >= -slope*line+70 and pixel <= slope*line+70:
                                        newimdata[index] = red
                for line in range(40):
                        line1=40+line
                        for pixel in range(140):
                                index = line1*140+pixel
                                if pixel >= slope*line1-70 and pixel <= -slope*line1+210:
                                        newimdata[index] = red


                newim = Image.new("RGBA",(140,140))
                newim.putdata(newimdata)
                return newim
                

                
                

        #########################################################################
        def create_pct_square(self,size):
                """
                creates a new square image of a variety of colors, and returns it.
                """
                newimdata = []
                red = (255, 0, 0)
                grn = (0, 255, 0)
                blu = (0, 0, 255)
    
                i = size/3
            
                for line in range(size):
                        iline = line%i
                        for pixel in range(size):
                                ipix = pixel%i
                                if line <i:
                                        if pixel < i:
                                                newimdata.append(red)
                                        elif pixel > 2*i:
                                                newimdata.append(blu)
                                        else:
                                                newimdata.append(grn)
                                elif line > 2*i:
                                        if pixel < i:
                                                newimdata.append(blu)
                                        elif pixel > 2*i:
                                                newimdata.append(grn)
                                        else:
                                                newimdata.append(red)
                                else:
                                        if pixel < i == 0:
                                                newimdata.append(grn)
                                        elif pixel > 2*i:
                                                newimdata.append(red)
                                        else:
                                                newimdata.append(blu)
                                    
                newim = Image.new("RGB",(size,size))
                newim.putdata(newimdata)
                return newim
    
        #########################################################################
        def create_white_square(self,size):
                """
                creates a new image, all white with a black border, and returns it.
                """
                newimdata = []
                black = (0, 0, 0)
                white = (255, 255, 255)
                
                for line in range(size):
                        for pixel in range(size):
                                if line == 0 or line == size-1 or pixel==0 or pixel == size-1:
                                        newimdata.append(black)
                                else:
                                        newimdata.append(white)
                                
                newim = Image.new("RGB",(size,size))
                newim.putdata(newimdata)
                return newim




                
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
                        if ( type == "TaskerMenuBar::addSatellite" or
                                 type == "TaskerButtonBar::addSatellite" ):
                           if len(event)>1:
                                   filename = event[1]
                                   self.addSatellite(filename)
                else:
                        return

        def addSatellite(self, satellite):
                """
                Adds a satellite to the tree

                :param satellite satellite: Satellite to be added to the tree
                """
                self.satList.append(satellite)
                self.masterList.append(satellite)
                file_options={}
                file_options["menu-options"] =  {"tearoff": 0}
                ## not sure why I have to do this, but its only invoking ONE method, thelast one specified,
                ## so I am making that method do difft things basedon the value of choice.
                #file_options["menu-items"] =  [ {"label":"", "command": self.fileMenu, "choice":"nothing"},
                #                                  {"label":"close", "command": self.fileMenu, "choice":"close"},
                #                                ]
                file_options["menu-items"] =  [ {"label":"close", "command": self.fileMenu, "choice":"close"}, ]
                f_id = self.treeview.insert('','end',values=(["text",satellite.name,file_options],), hidden="file")
                self.treeview.insert(f_id, 'end', values =(["text", "Catalog Num: " + satellite.catalogNumber],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Intl Designator: " + satellite.intlDesignator],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Epoch Year: " + satellite.epochYear],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Epoch Day: " + satellite.epochDay],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "1st Deriv Mean Motion: " + satellite.firstDerivativeOfMeanMotion],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "2nd Deriv Mean Motion: " + satellite.secondDerivativeOfMeanMotion],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Drag Term: " + satellite.dragTerm],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Ephemeris Type: " + satellite.ephemerisType],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Element Set Number: " + satellite.elementSetNumber],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Inclination: " + satellite.inclination],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "R.A.A.N.: " + satellite.raan],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Eccentricity: 0." + satellite.eccentricity],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Arg of Perigee: " + satellite.argumentOfPerigee],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Mean Anomaly: " + satellite.meanAnomaly],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Mean Motion: " + satellite.meanMotion],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Rev Num at Epoch: " + satellite.revolutionNumberAtEpoch],), hidden = "image")

        def addPoint(self, point):
                """
                Adds a point to the tree

                :param Point point: Point to be added to the tree
                """
                self.masterList.append(point)
                self.pointList.append(point)
                file_options={}
                file_options["menu-options"] =  {"tearoff": 0}
                file_options["menu-items"] =  [ {"label":"close", "command": self.fileMenu, "choice":"close"}, ]
                f_id = self.treeview.insert('','end',values=(["text",point.name,file_options],), hidden="file")
                self.treeview.insert(f_id, 'end', values =(["text", "Latitude: " + str(point.lat)],), hidden = "image")
                self.treeview.insert(f_id, 'end', values =(["text", "Longitude: " + str(point.lon)],), hidden = "image")

        ########################################################################
        def fileMenu(self,  choice=None, iid=None):
                """
                Creates the file menu

                :param choice
                :param iid
                """
                if iid is None:
                        return
                #print("fileMenu: iid="+iid+", choice="+str(choice))
                if choice == "close":
                        file_name   = self.item_text(self.treeview.item(iid,option="values"))
                        self.treeview.delete_item(iid)
                        self.event_publish(["TaskerTreeView::fileClose",file_name])
                        print("event published:"+"TaskerTreeView::fileClose, filename="+file_name)

                        # Remove satellite from satList
                        for sat in self.satList:
                                if sat.name == file_name:
                                        self.satList.remove(sat)
                        # Remove point from pointList
                        for point in self.pointList:
                                if point.name == file_name:
                                        self.pointList.remove(point)
                        # Remove from masterList
                        for obj in self.masterList:
                                if obj.name == file_name:
                                        self.masterList.remove(obj)
                        self.master.canvas.plotter.updateAll()
                        

        def item_text(self,item):
                """
                Given a tuple of values, return the text contents, or an empty string
                """
                if item is None:
                        return ""
                for entry in item:
                        if entry[0]=="text":
                                return entry[1]
                return ""
                        
        def select(self,args):
                """
                When the item's text is clicked on with mouse button 1.
                """
                sel_id = self.treeview.selection()[0]
                item = self.treeview.item(sel_id,option="values")
                hidden = self.treeview.item(sel_id,option="hidden")
                #print("geostar-treeview:: select: selection="+str(sel_id)+", "+str(hidden)+", "+str(item))
                print("geostar-treeview:: select: selection="+str(sel_id)+", "+str(hidden))
                return
