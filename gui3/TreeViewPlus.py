# GeoStar treeview class
#
# by Leland Pierce, June 2019

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import h5py
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from tkinter import PhotoImage
import collections


import os
from PIL import Image, ImageTk, ImageOps
from ttkwidgets.utilities import get_assets_directory

IM_OPEN = os.path.join(get_assets_directory(), "open.png")      # These three checkbox icons were isolated from
IM_CLOSED = os.path.join(get_assets_directory(), "closed.png")  # Checkbox States.svg (https://commons.wikimedia.org/wiki/File:Checkbox_States.svg?uselang=en)


from OrderedTree import OrderedTree

debug=False

##
## follows documentation of TreeView from:
## http://infohost.nmt.edu/~shipman/soft/tkinter/web/ttk-Treeview.html

class TreeViewPlus(tk.Frame):
        """Creates the Treeview for use in the GeoStar GUI.
           This is a complete rewrite of the tk/ttk treeview widget which
           does not suit our needs. What follows is the documentation for ttk.TreeView
           as provided at:
           http://infohost.nmt.edu/~shipman/soft/tkinter/web/ttk-Treeview.html

 The purpose of the ttk.Treeview widget is to present a hierarchical
 structure so that the user can use mouse actions to reveal or hide
 any part of the structure.

The association with the term “tree” is due to programming practice:
tree structures are a commonplace in program design. Strictly
speaking, the hierarchy shown in a Treeview widget is a forest: there
is no one root, just a collection of top-level nodes, each of which
may contain second-level nodes, each of which may contain third-level
nodes, and so on.

You may have encountered this particular presentation as a way of
browsing a directory or folder hierarchy. The entire hierarchy is
displayed like an indented outline, where each directory is on a
separate line, and the subdirectories of each directory are displayed
underneath that line, indented:

The user can click on the icon for a directory to collapse (close) it,
hiding all of the items in it. They can also click again on the icon
to expand (open) it, so that the items in the directory or folder are
shown.

The Treeview widget generalizes this concept so that you can use it to
display any hierarchical structure, and the reader can collapse or
expand subtrees of this structure with the mouse.

First, some definitions:

item

    One of the entities being displayed in the widget. For a file
    browser, an item might be either a directory or a file.

    Each item is associated with a textual label, and may also be
    associated with an image.

iid

    Every item in the tree has a unique identifier string called the
    iid. You can supply the iid values yourself, or you can let ttk
    generate them.

child

    The items directly below a given item in a hierarchy. A directory,
    for example, may have two kinds of children: files and
    subdirectories.

parent

    For a given item, if it is at the top of the hierarchy it is said
    to have no parent; if it is not at the top level, the parent is
    the item that contains it.

ancestor

    The ancestors of an item include its parent, its parent's parent,
    and so on up to the top level of the tree.

visible

    Top-level items are always visible. Otherwise, an item is visible
    only if all its ancestors are expanded.

descendant

    The descendants of an item include its children, its childrens'
    children, and so on. Another way of saying this is that the
    subtree of an item includes all its descendants.

tag

    Your program can associate one or more tag strings with each
    item. You can use these tags to control the appearance of an
    item. For example, you could tag directories with the tag 'd' and
    files with the tag 'f', and then specify that items with tag 'd'
    use a boldface font.

    You may also associate events with tags, so that certain events
    will cause certain handlers to be called for all items that have
    that tag. For example, you could set up a file browser so that
    when a user clicks on a directory, the browser updated its
    contents to reflect the current file structure.

Your Treeview widget will be structured with multiple columns. The
first column, which we'll call the icon column, displays the icons
that collapse or expand items. In the remaining columns, you may
display whatever information you like.

For example, a simple file browser widget might use two columns, with
the directory icons in the first column and the directory or file name
in the second columns. Or you might wish to display file sizes,
permissions, and other related data in additional columns.

The operations of the Treeview widget even allow you to use it as a
tree editor. Your program can remove an entire subtree from its
location in the main tree and then attach it later at an entirely
different point.

Here is the general procedure for setting up a Treeview widget.

    Create the widget with the ttk.Treeview constructor. Use the
    columns keyword argument to specify the number of columns to be
    displayed and to assign symbolic names to each column.

    Use the .column() and .heading() methods to set up column headings
    (if you want them) and configure column properties such as size
    and stretchability.

    Starting with the top-level entries, use the .insert() method to
    populate the tree. Each call to this method adds one item to the
    tree. Use the open keyword argument of this method to specify
    whether the item is initially expanded or collapsed.

    If you want to supply the iid value for this item, use the iid
    keyword argument. If you omit this argument, ttk will make one up
    and return it as the result of the .insert() method call.

    Use the values keyword argument of this method to specify what
    should appear in each column of this item when it is visible.
        """
        def __init__(self, master, columns=[], width=500, height=500, background="white",
                     font_name="Times", font_size=12, font_color="black",
                     indicator_foreground="black"):
                """ docs from:
                http://infohost.nmt.edu/~shipman/soft/tkinter/web/ttk-Treeview.html
 
To create a Treeview widget within a given parent widget:

    w = ttk.Treeview(parent, option=value, ...)

The constructor returns the new Treeview widget. Its options include:
class_ 	
You may provide a widget class name when you create this widget. This
name may be used to customize the widget's appearance; see Section 27,
“Standardizing appearance”. Once the widget is created, the widget
class name cannot be changed.

columns 	
A sequence of column identifier strings. These strings are used
internally to identify the columns within the widget. The icon column,
whose identifier is always '#0', contains the collapse/expand icons
and is always the first column.

The columns you specify with the columns argument are in addition to
the icon column.

For example, if you specified columns=('Name', 'Size'), three columns
would appear in the widget: first the icon column, then two more
columns whose internal identifiers are 'Name' and 'Size'.  

cursor 
Use this option to specify the appearance of the mouse cursor when it is
over the widget; see Section 5.8, “Cursors”. The default value (an
empty string) specifies that the cursor is inherited from the parent
widget.

displaycolumns 	
Selects which columns are actually displayed and determines the order
of their presentation. Values may be:

    '#all' to select all columns and display them in the order defined
    by the columns argument.

    A list of column numbers (integer positions, counting from 0) or
    column identifiers from the columns argument.

    For example, suppose you specify columns=('Name', 'Size',
    'Date'). This means each call to the .insert() method will require
    an argument values=(name, size, date) to supply the values that
    will be displayed. Let's call this sequence the logical column
    sequence.

    Further suppose that in the constructor you specify
    columns=(2,0). The physical column sequence, the columns that will
    actually appear in the widget, will be three: the icon column will
    be first, followed by the date column (index 2 in the logical
    column sequence), followed by the name column (logical column
    index 0). The size column will not appear.

    You could get the same effect by specifying column identifiers
    instead of logical column positions: columns=('Date', 'Name').

height 	
The desired height of the widget, in rows.

padding 	
Use this argument to place extra space around the contents inside the
widget. You may provide either a single dimension or a sequence of up
to four dimensions, interpreted according to this table:

Values given	Left	Top	Right	Bottom
a	        a	a	a	a
a b	        a	b	a	b
a b c	        a	c	b	c
a b c d	        a	b	c	d

selectmode 	
This option controls what the user is allowed to select with the mouse. Values can be:
selectmode='browse' 	The user may select only one item at a time.
selectmode='extended' 	The user may select multiple items at once.
selectmode='none' 	The user cannot select items with the mouse.

show 	
To suppress the labels at the top of each column, specify show='tree'. 
The default is to show the column labels.

style 	
Use this option to specify a custom widget style name; see Section 47,
“Customizing and creating ttk themes and styles”.

takefocus 	
Use this option to specify whether a widget is visited during focus
traversal; see Section 53, “Focus: routing keyboard input”. Specify
takefocus=True if you want the visit to accept focus; specify
takefocus=False if the widget is not to accept focus. The default
value is an empty string; by default, ttk.Treeview widgets do get
focus.

font_name
one of "Times", "Helvetica", "Courier"

font_size
in points. 12 is typical.

font_color:
either a name, like "black", "green", etc
or a hexadecimal rgb triple, like "#000000" for black, "#ffffff" for white,
   "#ff0000" for green
                """
                tk.Frame.__init__(self, master)
                self.master = master
                self.subscribers = []
                self.openFiles = []
                self.background = background
                self.canvas_width = width
                self.canvas_height = height
                self.iid_prefix="itemid"
                self.next_iid = 0

                self.font_name = font_name
                self.font_size= font_size
                self.font_color = font_color
                self.line_skip=0.75*self.font_size
                self.x_indent =self.font_size*2
                self.y_spacing=self.font_size+self.line_skip
                self.x_border = 12
                self.y_border = 6
                self.line_number=0


                self.theselection = []
                self.mbcount =-1
                self.mb=[]
                
                self.indicator_foreground=indicator_foreground

                ## originals are 9X9.
                ## here we scale it to fit the specified font_size:
                i1 = Image.open(IM_OPEN)
                i2 = self.set_indicator_foreground(i1,indicator_foreground)
                i3 = ImageOps.fit(i2,(self.font_size,self.font_size))
                self.im_open = ImageTk.PhotoImage(i3, master=self)
                ##i3 = ImageOps.fit(i1,(self.font_size,self.font_size))
                ##self.im_open = ImageTk.PhotoImage(i3, master=self)
                
                i1 = Image.open(IM_CLOSED)
                i2 = self.set_indicator_foreground(i1,indicator_foreground)
                i3 = ImageOps.fit(i2,(self.font_size,self.font_size))
                self.im_closed = ImageTk.PhotoImage(i3, master=self)
                ##i2 = ImageOps.fit(i1,(self.font_size,self.font_size))
                ##self.im_closed = ImageTk.PhotoImage(i2, master=self)

                ## need a blank image of the same size:
                i2=Image.new("RGB",(self.font_size,self.font_size),background)
                self.im_blank = ImageTk.PhotoImage(i2, master=self)


                
                # Vertical and horizontal scrollbars for canvas
                vbar = tk.Scrollbar(self, orient='vertical')
                hbar = tk.Scrollbar(self, orient='horizontal')
            
                # Create canvas
                #self.canvas = tk.Canvas(self, width=self.canvas_width,
                #                         height=self.canvas_height, bg=self.background,
                #                         highlightthickness=0, scrollregion=(0,0,self.canvas_width,self.canvas_height),
                #                         xscrollcommand=hbar.set, yscrollcommand=vbar.set)
                self.canvas = tk.Canvas(self, width=self.canvas_width,
                                         height=self.canvas_height, bg=self.background,
                                         highlightthickness=0, 
                                         xscrollcommand=hbar.set, yscrollcommand=vbar.set)

                hbar.pack(side="bottom",fill=tk.X,expand=False)
                vbar.pack(side="right",fill=tk.Y,expand=False)
                self.canvas.pack(side="top",fill="both",expand=True)

                vbar.configure(command=self.scroll_y)
                hbar.configure(command=self.scroll_x)

                ## set up the columns
                ## 1. names
                if len(columns)==0:
                        self.columns=["control","icon+text"]
                else:
                        self.columns=["control",] + columns
                self.ncolumns=len(columns)
                self.column_config=[]
                self.valid_anchors=[tk.NW, tk.N, tk.NE, tk.W, tk.CENTER, tk.E, tk.SW, tk.S, tk.SE]
                ## 2. set default column configuration:
                for num, column_name in enumerate(self.columns):
                        self.column_config.append({}) ## append an empty dict.
                        ## fill the dict:
                        self.column_config[num]["anchor"] = tk.CENTER
                        self.column_config[num]["id"] =  self.columns[num]
                        ## widths are in pixels;
                        self.column_config[num]["minwidth"] =  20
                        ## stretch: width is adjusted when widget is resized.
                        self.column_config[num]["stretch"] =  True
                        ## widths are in pixels;
                        self.column_config[num]["width"] =  200

                ## set up the items tree:
                self.items=OrderedTree()
                self.tree_root = self.items.create_node(identifier="root")

                ## make the canvas be draggable to change size.
                self.canvas.bind("<Configure>", self.on_resize)

        #########################################################################
        def on_resize(self,event):
                """
                Make the widget so that it can be resized with a mouse-drag.
                """
                self.canvas_width = event.width
                self.canvas_height = event.height
                # resize the canvas
                ##print("new size: "+str(event.width)+"X"+str(event.height))
                self.canvas.config(width=self.canvas_width, height=self.canvas_height)
                ##self.canvas.config(scrollregion=(0,0,self.canvas_width,self.canvas_height))

                

        #########################################################################
        def set_indicator_foreground(self,image,newcolor):
                """
                sets all black pixels in the passed-in image to the indicated newcolor.
                returns a new image.
                Supposed to be used to change the color of the open/close indicator.
                """
                newimdata = []
                blackcolor = (0,0,0,255)

                ##print("input color::"+str(newcolor))

                if type(newcolor) is not str and isinstance(newcolor, collections.Sequence):
                        ## add a 4th value if only 3:
                        ## assume a max-255-based tuple.
                        usecolor2=[newcolor[0],newcolor[1],newcolor[2]]
                        if len(usecolor2)==3:
                                usecolor2.append(255)
                        usecolor=(usecolor2[0], usecolor2[1], usecolor2[2], usecolor2[3])
                        ##print("1 use color::"+str(usecolor))
                else:
                        if newcolor[0] == "#":
                                h=newcolor.lstrip('#')
                                usecolor=tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                        else:
                                ## assume a string like "red":
                                usecolor1 = mcolors.to_rgba(newcolor)
                                usecolor2=[]
                                for val in usecolor1:
                                        usecolor2.append(int(255*val))
                                usecolor=(usecolor2[0], usecolor2[1], usecolor2[2], usecolor2[3])
                        ##print("2 use color::"+str(usecolor))
                        
                for color in image.getdata():
                        ##print("color:: "+str(color))
                        if color == blackcolor:
                                newimdata.append( usecolor )
                        else:
                                newimdata.append( color )
                newim = Image.new(image.mode,image.size)
                newim.putdata(newimdata)
                return newim

        #########################################################################
        def insert(self, parent, index, iid=None, **kw):
            ## parent: string: To insert a new top-level item, make this argument an empty string.
            ##                 To insert a new item as a child of an existing item, make this
            ##                    argument the parent item's iid.
            ## index: string or int: This argument specifies the position among this parent's
            ##                       children where you want the new item to be added.
            ##                       For example, to insert the item as the new first child,
            ##                       use a value of zero; to insert it after the parent's first
            ##                       child, use a value of 1; and so on.
            ##                       To add the new item as the last child of the parent,
            ##                       make this argument's value 'end'.
            ## iid: string:    optional.
            ##                 You may supply an iid for the item as a string value.
            ##                 If you don't supply an iid, one will be generated automatically
            ##                 and returned by the method.
            #######################
            ## keyword parameters: (specify in a dict)
            ## open: logical: Specifies whether this item will be open initially.
            ##                If you supply open=False, this item will be closed.
            ##                If you supply open=True, the item's children will be visible whenever
            ##                   the item itself is visible.
            ##                The default value is False.
            ## tags: string:  You may supply one or more tag strings to be associated with this item.
            ##                The value may be either a single string or a sequence of strings.
            ## values: array: This argument supplies the data items to be displayed in each column
            ##                of the item. The values are supplied in logical column order.
            ##                If too few values are supplied, the remaining columns will be blank
            ##                in this item; if too many values are supplied, the extras will be
            ##                discarded.
            ##                Each item in the array is a 2-item array.
            ##                This array provides a way to specify a variety of widgets to be included
            ##                in this column.
            ##                arrays are:    "image": followed by an image variable
            ##                               "text":  followed by a string
            ##                               "radio": followed by string giving the variable-name
            ##                                        associated with the radio button
            ##                               "check": followed by string giving the variable-value
            ##                                        associated with the check button
            ##                               "menu":  followed by a varb name giving an existing
            ##                                        pop-up menu widget.
            ##                
            ## image: object: You may display an image just to the right of the icon for this item's
            ##                row by providing an image=I argument, where I is an image created by the
            ##                PIL PhotoImage() method, for example. This will appear in column 1,
            ##                to the left of the text specified by the text keyword, and will supercede
            ##                anything specified for col1 using the values keyword.
            ## text: string:  You may supply text to be displayed just to the right of the icon,
            ##                and also to the right of the image if provided. This will appear in
            ##                column 1, to the right of the image specified by the image keyword,
            ##                if provided, and will supercede anything specified for col1 using the
            ##                values keyword.
            ## hidden: string: Any data you need, but don't want to be displayed.
            #######################
            ## Returns: iid string.
            #######################
            ## error-check:

            ## iid:
            if iid is None:
                iid = self.iid_prefix + str(self.next_iid)
                self.next_iid+=1

            ## create the dict that is the value for an item in the list:
            value = {}
            value["iid"]=iid
            ## defaults:
            value["open"]=False
            value["tags"]=["",]
            value["values"]=[]
            value["image"]=None
            value["text"]=None
            value["hidden"]=None
            ## over-write defaults with user-specified values:
            for key, val in kw.items():
                if key.lower() == "open":
                    if val:
                        value["open"]=True
                    else:
                        value["open"]=False
                elif key.lower() == "tags":
                    value["tags"] = val
                elif key.lower() == "values":
                    value["values"] = val
                elif key.lower() == "image":
                    value["image"] = val
                elif key.lower() == "text":
                    value["text"] = val
                elif key.lower() == "hidden":
                    value["hidden"] = val

            if parent=="":
                    parent="root"

            if parent is None:
                    #print("TreeViewPlus::insert: parent is none")
                    return

            #print("TreeviewPlus::insert: parent="+parent)
            parent_node = self.items.get_node(parent)
            if parent_node is None:
                    #print("TreeViewPlus::insert: parent_node is None")
                    return
            children = parent_node.value["children"]

            #print("TreeViewPlus::insert: children.size="+str(children.size))
            ## special case:
            ## parent has no children:
            if children.size == 0:
                ## ignore index and just add new node as first child:
                #print("TreeViewPlus::insert: add new node as first child")
                self.items.create_node(identifier=iid, parent=parent, data=value)
            else:
                ## general case:
                ## check validity of index:
                try:
                    iindex = int(index)
                except:
                    iindex = -1
                if index == "end":
                    #print("TreeViewPlus::insert: add new node as last child")
                    self.items.create_node(identifier=iid, parent=parent, data=value)
                elif iindex < 0:
                    return False
                elif iindex > children.size-1:
                    return False
                else:
                    #print("TreeViewPlus:insert: calling create_node_before, index="+str(iindex))
                    self.items.create_node_before(iindex, identifier=iid, parent=parent, data=value)
            #print("TreeViewPlus::insert: calling PAINT")
            self.paint()
            return iid

        #########################################################################
        def item(self,item_id,option=None, **kw):
                """
                Query or modify the options for the specified item.
                Refer to the .insert() method above for the names of the item options. 

                If no options or keywords are given, a dict with options/values 
                for the item is returned. 
                If option is specified, then the value for that option is returned. 
                Otherwise, sets the options to the corresponding values as given by kw, 
                   and returns True.
                Returns None if can't find the item_id

                """

                #print("TreeViewPlus:: item:: item_id="+str(item_id) )
                
                node  =self.items.get_node(item_id)
                if node is None:
                        #print("TreeViewPlus:: item:: returning None")
                        return None

                ## 1. return value for given option:
                if option:
                        ##print("TreeViewPlus:: item:: doing option not none")
                        if "data" in node.value:
                                d = node.value["data"]
                                if d is not None:
                                        if option in d:
                                                return d[option]

                ## 2. reset options based on keywords
                if kw:
                        ##print("TreeViewPlus:: item:: doing kw not none")
                        ## init value dict:
                        try:
                                value=node.value["data"]
                        except:
                                return None
                                
                        for key, val in kw.items():
                                if key.lower() == "open":
                                        if val:
                                                value["open"]=True
                                        else:
                                                value["open"]=False
                                elif key.lower() == "tags":
                                        value["tags"] = val
                                elif key.lower() == "values":
                                        value["values"] = val
                                elif key.lower() == "image":
                                        value["image"] = val
                                elif key.lower() == "text":
                                        value["text"] = val
                                elif key.lower() == "iid":
                                        value["iid"] = val
                                elif key.lower() == "hidden":
                                        value["hidden"] = val
                        # reset value:
                        node.value["data"] = value
                        self.paint()
                        return True

                ## 3. return dict of options.values:
                #print("doing no args at all")
                ##print("TreeViewPlus:: item:: doing no args")
                ##print("TreeViewPlus:: item:: node.value="+str(node.value))
                ##print("TreeViewPlus:: item:: node.value[data]="+str(node.value["data"]))
                try:
                        return node.value["data"]
                except:
                        return None

                return None
                                
        #########################################################################
        def index(self,item_id):
                """
                Returns the integer index of item within its parent’s list of children.
                returns -1 if not found. index=0 is the first item.
                """
                node  =self.items.get_node(item_id)
                if node is None:
                        return -1
                myindex=0
                while node:
                        node = node.previous
                        myindex += 1
                return myindex-1
                
        #########################################################################
        def parent(self,item_id=None):
                """
                Returns the ID of the parent of item, 
                or an empty string if the item is at the top level of the hierarchy, 
                or is not found.
                """
                node = self.items.get_node(item_id)
                if node is None:
                        return ''

                parent_node = node.value["parent"]
                if parent_node is None:
                        return ''
                
                try:
                        id = parent_node.value["identifier"]
                except:
                        id=''
                return id

        #########################################################################
        def next(self,item_id=None):
                """
                Returns the identifier of item’s next sibling, 
                or an empty string if item is the last child of its parent, 
                or item is not found.
                """
                node = self.items.get_node(item_id)
                if node is None:
                        return ''

                node = node.next
                if node is None:
                        return ''

                try:
                        id = node.value["identifier"]
                except:
                        id=''
                return id
 
        #########################################################################
        def prev(self,item_id=None):
                """
                Returns the identifier of item’s previous sibling, 
                or an empty string if item is the first child of its parent, 
                or if not found.
                """
                node = self.items.get_node(item_id)
                if node is None:
                        return ''

                node = node.previous
                if node is None:
                        return ''

                try:
                        id = node.value["identifier"]
                except:
                        id=''
                return id
                         
        #########################################################################
        def get_children(self,item_id=None):
                """
                returns list of strings of item_ids that are children of the
                item specified by the string item_id
                If item_id not specified, returns children of root node.
                If there are no children, retuns an empty list
                """
                if item_id is None:
                        node = self.items.get_node("root")
                else:
                        node  =self.items.get_node(item_id)

                if node is None:
                        return []
                
                children = node.value["children"]
                if children is None:
                        return []

                if children.size==0:
                        return []
                else:
                        ret = []
                        try:
                                node = children.first
                        except:
                                node=None
                        while node:
                                try:
                                        ret.append(node.value["identifier"])
                                except:
                                        pass
                                node = node.next
                        return ret
                
                return []
                
        #########################################################################
        def exists(self,item_id):
                """
                returns True if the specified item (specified by the item_id string)
                is present.
                returns False otherwise.
                """
                return self.items.identifier_exists(item_id)
        
        #########################################################################
        def delete_item(self,item_id):
                """
                deletes an item in the tree as specified by the string item_id.
                returns True on success, False otherwise
                Does not delete the root item
                """
                if item_id == "root":
                        return False

                n=self.items.remove_node(item_id)

                self.paint()

                if n>0:
                        return True
                else:
                        return False

        #########################################################################
        def delete(self,item_ids):
                """
                deletes items in the tree as specified by the list of strings in item_ids.
                returns True on success, False otherwise
                Does not delete the root item
                """
                ret = True
                if type(item_ids) is not str and isinstance(item_ids, collections.Sequence):
                        for item in item_ids:
                                if not self.delete_item(item):
                                        ret = False
                else:
                        if not self.delete_item(item_ids):
                                ret = False
                        
                return ret

        #########################################################################
        def column(self, column_id, option=None, **kw):
            ## is column_id valid?
            column_number=-1
            if column_id.startswith("#"):
                column_number = int(column_id.split("#")[1])
            else:
                for num, column_name in enumerate(self.columns):
                    if column_name == column_id:
                        column_number = num
            if column_number <0 or column_number>self.ncolumns-1:
                return False ## invalid column_id
            #print("TreeViewPlus::column: column-number="+str(column_number))

            ## set values of config params based on kw:
            for key, value in kw.items():
                if key.lower() == "anchor":
                    if value in self.valid_anchors:
                        self.column_config[column_number]["anchor"]=value
                elif key.lower() == "minwidth":
                    ivalue = int(value)
                    if ivalue >0 and ivalue < self.canvas.winfo_screenwidth():
                        self.column_config[column_number]["minwidth"]=ivalue
                elif key.lower() == "width":
                    ivalue = int(value)
                    if ivalue >0 and ivalue < tk.winfo_screenwidth():
                        self.column_config[column_number]["width"]=ivalue
                elif key.lower() == "stretch":
                    if value:
                        self.column_config[column_number]["stretch"]=True
                    else:
                        self.column_config[column_number]["stretch"]=False

            ## deal with option param:
            ## returns value of the specified option (string)
            if option is None:
                print("TreeViewPlus::column: option is None")
                if len(kw) == 0:
                    print("TreeViewPlus::column: kw is None")
                    return self.column_config[column_number]
                else:
                    print("TreeViewPlus::column: kw is NOT-None")
                    return True
            else:
                if option.lower() == "anchor":
                    return self.column_config[column_number]["anchor"]
                elif option.lower() == "minwidth":
                    return self.column_config[column_number]["minwidth"]
                elif option.lower() == "width":
                    return self.column_config[column_number]["width"]
                elif option.lower() == "stretch":
                    return self.column_config[column_number]["stretch"]

        ##########################################################################
        def paint(self):
                """
                re-draws the canvas associated with this widget.
                """
                self.canvas.delete("all")
                self.line_number=0
                ## go through the tree and print stuff
                ## (incomplete for now...)
                ## the first value: -1 is the indent-level
                self.paint_item("root",-1)
                
        ##################################################################
        def paint_item(self,nodeid,indent):
                """
                nodeid is a string that gives the current node to paint.
                indent is the indent-level, an integer from 0->whatever.
                """
                if nodeid==None:
                   return
                if nodeid=="":
                   return

                node=self.items.get_node(nodeid)
                if debug:
                        print("@@@@@@@@@@@@@@@@@@@@@ input: indent="+str(indent)+",  line#="+str(self.line_number))


                ##determine if item is open or closed
                open_item = False
                if node.value["identifier"] == "root":
                        open_item = True
                if debug:
                        print("AAA node.value[identifier]="+node.value["identifier"])
                if "data" in node.value:
                        if node.value["data"] and "open" in node.value["data"]:
                                open_item = node.value["data"]["open"]
                                if debug:
                                        print("AAA node.value[data][open]="+str(node.value["data"]["open"]))

                if debug:
                        if open_item:
                                print("AAA paint_item:: OPEN: node.value[identifier]="+node.value["identifier"])
                        else:
                                print("AAA paint_item:: CLOSED: node.value[identifier]="+node.value["identifier"])

                
                if node.value["data"]:
                        if debug:
                                print("TreeViewPlus::paint_item: node.value['data'] is:")
                                print(node.value["data"])
                        # 1. put icon for open/closed:
                        children = node.value["children"]
                        nchildren=children.size
                        xwidth=0
                        if nchildren > 0:
                                options={}
                                options["anchor"]="nw"
                                options["tags"]="indicator"
                                if open_item:
                                        options["image"]=self.im_open
                                        xwidth = self.im_open.width()
                                else:
                                        options["image"]=self.im_closed
                                        xwidth = self.im_closed.width()
                                if debug:
                                        print("paint_item:: added an open/close image, xwidth="+str(xwidth))
                                        print("paint_item:: added an open/close image, id="+node.value["identifier"])
                                x=indent*self.x_indent+self.x_border
                                x-=0.1*self.x_indent
                                y=self.line_number*self.y_spacing+self.y_border
                                y+= 0.5*self.y_spacing
                                id=self.canvas.create_image(x,y,options)

                                def handler(event, self=self, id=node.value["identifier"]):
                                        return self.toggle_open_close(event, id)
                                self.canvas.tag_bind(id,'<Button-1>', handler)

                                if debug:
                                        print("paint_item:: created toggle binding for id="+str(id))
                        else:
                                options={}
                                options["anchor"]="nw"
                                options["tags"]="iid="+node.value["identifier"]
                                options["image"]=self.im_blank
                                xwidth = self.im_blank.width()
                                x=indent*self.x_indent+self.x_border
                                x-=0.1*self.x_indent
                                y=self.line_number*self.y_spacing+self.y_border
                                y+= 0.5*self.y_spacing
                                id=self.canvas.create_image(x,y,options)
                                
                                
                        # 2. Display values
                        xwidth2=0
                        for value in node.value["data"]["values"]:
                                if debug:
                                        print("TreeViewPlus::paint_item: value="+str(value))
                                if value[0]=="text":
                                        text = value[1]
                                        options={}
                                        options["anchor"]="nw"
                                        options["font"]=(self.font_name, self.font_size)
                                        options["fill"]=self.font_color
                                        options["text"]=text
                                        options["tags"]="text"
                                        x=indent*self.x_indent+self.x_border+xwidth+xwidth2
                                        y=self.line_number*self.y_spacing+self.y_border
                                        id=self.canvas.create_text(x,y,options)
                                        bb=self.canvas.bbox(id)
                                        xwidth2 += bb[2]-bb[0]

                                        if debug:
                                                print("AAA value="+str(value))
                                        if len(value) == 2:
                                                ## add to selection when text is clicked
                                                def handler_add(event, self=self, id=node.value["identifier"]):
                                                        return self.add_to_selection(event, id)
                                                self.canvas.tag_bind(id,'<Button-1>', handler_add)
                                        elif len(value) == 3:
                                                ## make a pop-up menu appear when text is clicked
                                                overall_options=value[2]
                                                menu_options = overall_options["menu-options"]
                                                menu_items   = overall_options["menu-items"]
                                                menu = tk.Menu(self.canvas, menu_options)
                                                for item in menu_items:
                                                        menu.add_command(label=item["label"],
                                                                         command=lambda  choice=item["choice"], iid=node.value["identifier"]:
                                                                         item["command"](choice=choice, iid=iid)
                                                                        )
                                                self.posted=False
                                                def toggle_post_menu(event,menu=menu):
                                                        if self.posted:
                                                                menu.unpost()
                                                                self.posted=False
                                                        else:
                                                                menu.post(event.x_root,event.y_root)
                                                                self.posted=True
                                                self.canvas.tag_bind(id,'<Button-1>', toggle_post_menu)
                                                

                                        ## YET:
                                        ## this assumes "text" is always last....
                                        self.line_number += 1
                                        if debug:
                                                print("TreeViewPlus::paint_item: just did create_text")
                                                print("+++++++++++++++++++++++++++posn="+str(x)+"x"+str(y)+"; text=|"+text+"|")

                                elif value[0] == "image":
                                        options={}
                                        options["anchor"]="nw"
                                        options["tags"]="image"
                                        options["image"]=value[1]

                                        x=indent*self.x_indent+self.x_border+xwidth+xwidth2
                                        ##x-=0.1*self.x_indent
                                        y=self.line_number*self.y_spacing+self.y_border
                                        y+= 0.5*self.y_spacing
                                        id=self.canvas.create_image(x,y,options)
                                        
                                        self.canvas.update()
                                        bb=self.canvas.bbox(id)
                                        xwidth2 += bb[2]-bb[0]
                                        
                                elif value[0] == "radio":
                                        pass
                                elif value[0] == "check":
                                        pass
                                elif value[0] == "menu":
                                        self.mbcount += 1
                                        overall_options = value[1]
                                        thetype = overall_options["type"]
                                        menubutton_options = overall_options["menubutton-options"]
                                        menu_options = overall_options["menu-options"]
                                        menu_items = overall_options["menu-items"]
                                        
                                        options={}
                                        options["anchor"]="nw"
                                        options["tags"]="menu"
                                        x=indent*self.x_indent+self.x_border+xwidth+xwidth2
                                        y=self.line_number*self.y_spacing+self.y_border
                                        y+= 0.5*self.y_spacing
                                        id = self.canvas.create_window(x,y,options)

                                        mb = tk.Menubutton(self.canvas,menubutton_options)
                                        ## create some extra attributes so we can store needed stuff:
                                        setattr(mb,"node_type",thetype)
                                        setattr(mb,"node_iid",node.value["identifier"])
                                        self.mb.append(mb)
                                        
                                        #print("mb.node_type="+mb.node_type)
                                        #print("mb.node_iid="+mb.node_iid)
                                        #print("mb.config="+str(mb.config()))

                                        menu = tk.Menu(mb, menu_options)
                                        mb.menu = menu
                                        mb['menu'] = menu

                                        for item in menu_items:
                                                thecommand = item["command"]
                                                menu.add_command(image=item["image"],
                                                                 label=item["label"],
                                                                 compound=item["compound"],
                                                                 command=lambda selfmb=self.mb[self.mbcount], image=thecommand["image"], choice=thecommand["choice"], iid=node.value["identifier"]:
                                                                 thecommand["name"](selfmb=selfmb,image=image,choice=choice,iid=iid)
                                                                 )
                                                
                                        self.canvas.itemconfigure(id,window=mb)
                                        self.canvas.update()
                                        bb=self.canvas.bbox(id)
                                        xwidth2 += bb[2]-bb[0]
                                        ##print("xwidth2="+str(xwidth2))

                                        


                
                if open_item:
                        ## children first:
                        ## children get indented more than parent
                        children = node.value["children"]
                        nchildren=children.size
                        if nchildren > 0:
                                for i in range(nchildren):
                                        try:
                                                self.paint_item(children.nodeat(i).value["identifier"], indent+1)
                                        except:
                                                print("paint_item of a child failed, i="+str(i))
                ## next sibling:
                ## siblings are indented the same amount
                identifier = node.value["identifier"]
                try:
                        node = self.tree_root.next_sibling(identifier)
                        if node is not None:
                                self.paint_item(node.value["identifier"],indent)
                except:
                        pass


        #########################################################################
        def menus(self):
                """
                return list of menubuttons
                """
                return self.mb

        #########################################################################
        def menu_selection(self):
                """
                """
                return [self.menu_iid, self.menu_choice]
                
        #########################################################################
        def onom(self,event):
                """
                debug only for now.
                """
                print("self.optionVar=|"+self.optionVar.get()+"|")
                
        #########################################################################
        def onmenu(self):
                """
                debug only for now.
                """
                print("self.displayVar="+str(self.displayVar.get()))
        
        #########################################################################
        def selection(self):
                """
                Returns the list of selected items (iid's)
                """
                return self.theselection
                
        #########################################################################
        def bind(self, sequence, callback):
                """
                Make a bind on treeview do abind on the canvas
                """
                self.canvas.bind(sequence,callback)
                

        #########################################################################
        def add_to_selection(self, event, item_id):
                """
                add the selected item to the selection.
                adds the iid string.
                """
                ##x=event.x
                ##y=event.y
                ##item_id  = self.position_to_iid(x,y)
                node  =self.items.get_node(item_id)
                if node is None:
                        return
                self.theselection = []
                self.theselection.append(item_id)
                
                self.canvas.event_generate('<<TreeviewSelect>>')
                

                
        #########################################################################
        def toggle_open_close(self, event,item_id):
                """
                modify the current view to toggle the state of the selected item,
                either changing the value of "open" to True if its False,
                or changing the value of "open" to False if its True
                Currently, this has no effect on the "open" state of any of its 
                children.
                """
                ## 1. figure out which node was clicked:
                ##x=event.x
                ##y=event.y
                ##item_id  = self.position_to_iid(x,y)
                node  =self.items.get_node(item_id)
                if node is None:
                        ##print("toggle_open_close:: node is None")
                        return

                ## 2. modify the state of the node
                if "data" in node.value:
                        if node.value["data"] and "open" in node.value["data"]:
                                if node.value["data"]["open"]:
                                        node.value["data"]["open"]=False
                                        self.canvas.event_generate('<<TreeviewClose>>')
                                else:
                                        node.value["data"]["open"]=True
                                        self.canvas.event_generate('<<TreeviewOpen>>')
                
                ## 3. repaint
                self.paint()
                
        #########################################################################
        def position_to_iid(self,x,y):
                """
                Given a position in the canvas, return the item-id,
                or None if not close enough...
                """
                id = self.canvas.find_closest(x,y)[0]
                tags = self.canvas.itemcget(id,"tags")
                item_id=self.parse_tags(tags,"iid")
                return item_id
        
        #########################################################################
        def parse_tags(self,tags,kw):
                """
                Given a string, tags, and a keyword, kw, this function tries to find
                a substring that looks like:
                    kw=value
                and returns the value of the first one it finds, 
                otherwise it returns an empty string.
                """
                i=tags.find(kw+"=")
                if(i<0):
                        return ""
                for s in tags.split(" "):
                        if s.find(kw+"=") >=0:
                                ##print("found: "+s)
                                ##for w in s.split("="):
                                ##        print("w::"+str(w))
                                return s.split("=")[1]
                return ""
        #########################################################################
        def scroll_y(self, *args, **kwargs):
            ''' Scroll canvas vertically and redraw the image '''
            self.canvas.yview(*args, **kwargs)  # scroll vertically

        def scroll_x(self, *args, **kwargs):
            ''' Scroll canvas horizontally and redraw the image '''
            self.canvas.xview(*args, **kwargs)  # scroll horizontally

        
        #########################################################################
        def event_subscribe(self, obj_ref):
            self.subscribers.append(obj_ref)

        def event_publish(self, cmd):
            for sub in self.subscribers:
                sub.event_receive(cmd)

        def event_receive(self,event):
            if len(event) > 0:
                type = event[0]
                if ( type == "GeoStarMenuBar::fileOpen" or
                     type == "GeoStarButtonBar::fileOpen" ):
                    if len(event)>1:
                        filename = event[1]
                        self.fileOpen(filename)
                else:
                    return
