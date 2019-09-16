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

import MenuBar

class TaskerTreeView(tk.Frame):
        """
        Creates the Treeview for use in the Tasker GUI.
        """
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
                self.subscribers.append(obj_ref)

        def event_publish(self, cmd):
                for sub in self.subscribers:
                        sub.event_receive(cmd)

        def event_receive(self,event):
                if len(event) > 0:
                        type = event[0]
                        if ( type == "TaskerMenuBar::fileOpen" or
                                 type == "TaskerButtonBar::fileOpen" ):
                           if len(event)>1:
                                   filename = event[1]
                                   self.fileOpen(filename)
                else:
                        return

        def fileOpen(self,filename):
                ## need to open the hdf5 file and determine structure.
                self.openFiles.append(filename)

                
                wht_command={"name": self.raster_menu_select, "image":self.wht_square ,
                             "text":"blank" ,"choice":"blank"}
                gry_command={"name": self.raster_menu_select, "image":self.gry_square ,
                             "text":"gray" ,"choice":"gray"}
                red_command={"name": self.raster_menu_select, "image":self.red_square ,
                             "text":"red" ,"choice":"red"}
                grn_command={"name": self.raster_menu_select, "image":self.grn_square ,
                             "text":"green" ,"choice":"green"}
                blu_command={"name": self.raster_menu_select, "image":self.blu_square ,
                             "text":"blue" ,"choice":"blue"}
                pct_command={"name": self.raster_menu_select, "image":self.pct_square ,
                             "text":"pct" ,"choice":"pct"}
                raster_options={}
                raster_options["type"]="raster"
                ## menubuton defaults to image-only, even if text is supplied
                raster_options["menubutton-options"] = {"anchor":"nw", "image":self.wht_square, "text":"blank", "padx":0, "pady":0}
                raster_options["menu-options"] = {"tearoff": 0}
                raster_options["menu-items"]   = [{"image":self.wht_square, "label":"don't display",
                                    "compound": tk.LEFT, "command": wht_command},
                                   {"image":self.gry_square, "label":"display as grayscale",
                                    "compound": tk.LEFT, "command": gry_command},
                                   {"image":self.red_square, "label":"display in red chnl",
                                    "compound": tk.LEFT, "command": red_command},
                                   {"image":self.grn_square, "label":"display in green chnl",
                                    "compound": tk.LEFT, "command": grn_command},
                                   {"image":self.blu_square, "label":"display in blue chnl",
                                    "compound": tk.LEFT, "command": blu_command},
                                   {"image":self.pct_square, "label":"display in pseudo-color",
                                    "compound": tk.LEFT, "command": pct_command}
                                   ]

                file_options={}
                file_options["menu-options"] =  {"tearoff": 0}
                ## not sure why I have to do this, but its only invoking ONE method, thelast one specified,
                ## so I am making that method do difft things basedon the value of choice.
                #file_options["menu-items"] =  [ {"label":"", "command": self.fileMenu, "choice":"nothing"},
                #                                  {"label":"close", "command": self.fileMenu, "choice":"close"},
                #                                ]
                file_options["menu-items"] =  [ {"label":"close", "command": self.fileMenu, "choice":"close"}, ]

                f = h5py.File(filename,'r')
                if f.attrs['object_type'].decode('UTF-8') == "geostar::hdf5":
                        #print("==== opening a HDF5 file. ====")
                        #print("geostartreeview:: inserting at top level, filename="+filename)
                        f_id = self.treeview.insert('','end',values=(["text",filename,file_options],), hidden="file")
                        for item_name_h5, image in f.items():
                                # debug: print(ch, image)
                                if image.attrs['object_type'].decode('UTF-8') == 'geostar::image':
                                        ## images
                                        #print("geostartreeview:: inserting an image under f_id="+str(f_id))
                                        image_id = self.treeview.insert(f_id,'end',
                                                                        values=(["image",self.image_icon], ["text",item_name_h5],),
                                                                        hidden="image")
                                        self.ids.append(image_id)
                                        for image_item_name_h5, raster in image.items():
                                                if raster.attrs['object_type'].decode('UTF-8') == 'geostar::raster':
                                                        ## rasters
                                                        #print("geostartreeview:: inserting a raster under image_id="+str(image_id))
                                                        raster_id = self.treeview.insert(image_id,'end',
                                                                                         values=(["menu",raster_options],["text",image_item_name_h5],),
                                                                                         hidden="raster" )

                                                        self.ids.append(raster_id)
                                                else:
                                                        print("it's not a raster.")
                                else:
                                        print("it's not an image.")
                else:
                        print(f.attrs['object_type'].decode('UTF-8'))
                        print("it's not a HDF5 file.")





        ########################################################################
        def fileMenu(self,  choice=None, iid=None):
                """
                """
                if iid is None:
                        return
                #print("fileMenu: iid="+iid+", choice="+str(choice))
                if choice == "close":
                        file_name   = self.item_text(self.treeview.item(iid,option="values"))
                        self.treeview.delete_item(iid)
                        self.event_publish(["TaskerTreeView::fileClose",file_name])
                        print("event published:"+"TaskerTreeView::fileClose, filename="+file_name)
                
        ########################################################################
        def raster_menu_select(self, selfmb=None, iid=None, image=None, choice=None):
                """
                """
                if selfmb is None:
                        return
                if image is not None:
                        selfmb.config(image=image)
                if choice is not None:
                        selfmb.config(text=choice)

                #print("=======================")
                #print("raster_menu-select START: iid=: "+str(iid)+",  choice="+str(choice))


                ## must enforce selection rules here:
                ## 1. if blank a raster, fine, we're done, no other raster need be updated.
                ## 2. if choose a raster for gray, all other rasters must be set to blank
                ## 3. if choose r, blank any other rasters that are set to r, gray or pct
                ## 4. same with g or b
                ## 5. if choose pct, all other rasters must be set to blank
                ## process: get list of menu-buttons
                ##          iterate through all of them, changing their state as needed
                ##          produce events when change state
                if choice == "blank":
                        ##generate event and done:
                        print("blank event...")
                        return
        
                menus = self.treeview.menus()
                #print("raster_menu-select1: # of menus: "+str(len(menus)))

                for menu in menus:
                        text = menu.config("text")[4]
                        ## these new attributes are created by TreeViewPlus 
                        thetype = menu.node_type
                        theiid  = menu.node_iid

                        ## ignore menus that are not related to rasters, for now.....
                        if thetype != "raster":
                                break
            
                        #print("raster_menu_select3: iid="+str(iid)+",  theiid="+theiid+",  text="+str(text))
                        if theiid != iid:
                                raster_name = self.item_text(self.treeview.item(theiid,option="values"))
                                parent = self.treeview.parent(theiid)
                                image_name  = self.item_text(self.treeview.item(parent,option="values"))
                                parent = self.treeview.parent(parent)
                                file_name   = self.item_text(self.treeview.item(parent,option="values"))
                                
                                if choice == "gray" or choice =="pct":
                                        menu.config(image=self.wht_square)
                                        menu.config(text="raster:"+theiid+":blank")
                                        ## generate event....
                                        #print("updated "+theiid+" to blank")
                                        self.event_publish(["TaskerTreeView::state","raster::blank",raster_name, image_name, file_name])
                    
                                elif choice =="red":
                                        if text=="red" or text=="gray" or text=="pct":
                                                menu.config(image=self.wht_square)
                                                menu.config(text="raster:"+theiid+":blank")
                                                ## generate event....
                                                #print("updated "+theiid+" to blank")
                                                self.event_publish(["TaskerTreeView::state","raster::blank",raster_name, image_name, file_name])
                                elif choice =="green":
                                        if text=="green" or text=="gray" or text=="pct":
                                                menu.config(image=self.wht_square)
                                                menu.config(text="raster:"+theiid+":blank")
                                                ## generate event....
                                                #print("updated "+theiid+" to blank")
                                                self.event_publish(["TaskerTreeView::state","raster::blank",raster_name, image_name, file_name])
                                elif choice =="blue":
                                        if text=="blue" or text=="gray" or text=="pct":
                                                menu.config(image=self.wht_square)
                                                menu.config(text="raster:"+theiid+":blank")
                                                ## generate event....
                                                #print("updated "+theiid+" to blank")
                                                self.event_publish(["TaskerTreeView::state","raster::blank",raster_name, image_name, file_name])
                    
                ## finally, generate the event for the state change for the current raster:
                ## should generate an event here, but for now just print.
                #print("raster_menu_select4: iid="+str(iid))
                #print("raster_menu_select5: choice="+str(choice))
                raster_name = self.item_text(self.treeview.item(iid,option="values"))
                parent = self.treeview.parent(iid)
                image_name  = self.item_text(self.treeview.item(parent,option="values"))
                parent = self.treeview.parent(parent)
                file_name   = self.item_text(self.treeview.item(parent,option="values"))
                self.event_publish(["TaskerTreeView::raster_menu_select",choice,raster_name, image_name, file_name])
                print("event published:"+"TaskerTreeView::raster_menu_select"+", "+choice+", "+raster_name+", "+ image_name+", "+ file_name)
                return

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
