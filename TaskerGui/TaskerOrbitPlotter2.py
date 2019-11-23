from skyfield.api import Topos, load
from datetime import datetime, timedelta
from matplotlib import pyplot, pylab, scale
from matplotlib.figure import Figure
from math import pi, sin, cos, tan, log, atan
from spacecraft2 import spacecraft
from haversine import haversine, Unit
from PIL import Image
import numpy as np

import os
import math
import urllib.request
#import random
import os.path
"""
Task for calculating ground tracks. To use:
    1. Initialize with name of satellite
    2. Create start time as datetime object
    3. Create end time as datetime object
    4. Call plot with start and end time
"""

def onClick(event):
    import pdb
    pdb.set_trace()
    print("x: " + event.x + ",     y: " + event.y)

class TaskerOrbitPlotter:

    def __init__(self, master):
        self.master = master
        self.satellites = load.tle("https://celestrak.com/NORAD/elements/active.txt")
        self.zoom = 2
        self.top = 0
        self.left = 0
        self.drawMap()
        self.centerX = 0
        self.centerY = 0
        self.width = 360
        self.height = 170.102258
        self.vertScale = 1
        self.horScale = 1
        self.zoomHistory = []
        
    """ Initializes the plot and displays the map image """
    def show(self):
        im = pyplot.imread("map.png")
        self.fig = pyplot.gcf()
        #self.clickID = self.fig.canvas.mpl_connect("button_press_event", onClick)
        xstart = self.centerX - self.width/2
        xend = self.centerX + self.width/2
        ystart = self.centerY - self.height/2
        yend = self.centerY + self.height/2
        pyplot.imshow(im, origin = "upper", extent = [xstart, xend, ystart, yend])
        pyplot.gca().set_aspect("auto")
        pyplot.yscale("linear")
        pyplot.axis("off")

        self.axis = pyplot.gca()
        return self.fig

    """
    Called whenever an orbit needs to be plotted.
    Plots the orbit from -180 to 180 degrees longitude for the current orbit.
    For most satellites, this means that one full period is plotted.
    For satellites near polar orbit, multiple periods may be plotted
    """
    def plot(self, sat):
        time = self.master.parent.time

        self.satellite = self.satellites[sat.name]
        pyplot.figure(self.fig.number)

        latitudes = []
        longitudes = []

        # Calculate orbital period
        n = float(sat.meanMotion)
        mu = 398600; # km^3/s^2
        a = mu**(1/3) / (2*n*pi/86400)**(2/3)
        T = 2*pi*(a**3/mu)**(1/2)

        # Check if orbit is geosynchronous:
        isGeosynchronous = False
        if abs(T - 86400) < 600:
            isGeosynchronous = True

        ts = load.timescale()
        dt = timedelta(seconds = T/100)

        # Propogate orbit and save the coordinates
        longitudes_counted = 0
        for dt in [dt, -dt]:
            t = time
            while True:
                currentTime = ts.utc(t.year, t.month, t.day, t.hour, t.minute,
                                     t.second)
                geocentric = self.satellite.at(currentTime)
                subpoint = geocentric.subpoint()
                latitude = subpoint.latitude.radians
                longitude = subpoint.longitude.radians*180/pi
                t = t + dt
                longitudes_counted = longitudes_counted + 1
                if longitudes_counted >= 2 and abs(longitudes[-1] - longitude) > 300:
                    longitudes_counted = 0
                    break
                if isGeosynchronous and abs(t - time) >= timedelta(seconds =
                86400):
                    longitudes_counted = 0
                    break

                latitudes.append(latitude)
                longitudes.append(longitude)

        # Convert latitude to Mercator projection and correct for polar latitudes
        mapHeight = 170.102258
        for i in range(0, len(latitudes)):
            mercN = log(tan((pi/4)+(latitudes[i]/2)))
            latitudes[i] = (mapHeight/2)-(mapHeight*mercN/(2*pi)) - 90
            if(latitudes[i] > 85):
                latitudes[i] = 85
            if(latitudes[i] < -85):
                latitudes[i] = -85

        # Plot the orbit
        i = 1
        x = []
        x.append(longitudes[0])
        y = []
        y.append(latitudes[0])
        while i < len(longitudes):
            longitude = longitudes[i]
            latitude = latitudes[i]
            #if abs(longitudes[i-1] - longitude) > 30:
            if abs(longitudes[i] - longitudes[0]) < 1:
                pyplot.plot(x, y, color = 'y', linewidth = 4)
                x = []
                x.append(longitudes[i])
                y = []
                y.append(latitudes[i])
            else:
                x.append(longitude)
                y.append(latitude)
            i = i + 1
                
        pyplot.plot(x, y, color = 'y', linewidth = 4)
        pyplot.scatter(longitudes[0], latitudes[0], s = 200, color = 'y')
        pyplot.gca().annotate(sat.name, (longitudes[0], latitudes[0]))
        pyplot.gca().set_xlim(left = self.centerX - self.width/2, right = self.centerX + self.width/2)
        pyplot.gca().set_ylim(bottom = self.centerY - self.height/2, top = self.centerY + self.height/2)

        self.master.parent.statusbar.update(time)
        self.master.canvas.draw()

    # Plots a point
    def plotPoint(self, point):
        pyplot.figure(self.fig.number)

        # Convert latitude for Mercator Projection
        mapHeight = 170.102258
        mercN = log(tan((pi/4)+(point.lat/2)))
        plottedLat = (mapHeight/2)-(mapHeight*mercN/(2*pi)) - 90
        if(plottedLat > mapHeight/2):
            plottedLat = mapHeight/2
        if(plottedLat < -mapHeight/2):
            plottedLat = -mapHeight/2
        
        plottedLon = point.lon

        # Plot to figure
        pyplot.scatter(plottedLon, plottedLat)
        pyplot.gca().annotate(point.name, (plottedLon, plottedLat))

        # Show updated figure
        self.master.parent.statusbar.update(time)
        self.master.canvas.draw()



    
    """ Returns the time for which a satellite is over the given coordinates within the time range given"""
    def search(self, sat, lat, long, timeStart, timeEnd, tolerance):
        self.satellite = self.satellites[sat.name]

        # Calculate orbital period
        n = float(sat.meanMotion)
        mu = 398600; # km^3/s^2
        a = mu**(1/3) / (2*n*pi/86400)**(2/3)
        T = 2*pi*(a**3/mu)**(1/2)

        # Determine dt
        ts = load.timescale()
        dt = timedelta(seconds = T/100)

        # Search for time
        t = timeStart
        while t <= timeEnd:
            currentTime = ts.utc(t.year, t.month, t.day, t.hour, t.minute,
                                    t.second)
            geocentric = self.satellite.at(currentTime)
            subpoint = geocentric.subpoint()
            currentLat = subpoint.latitude.degrees
            currentLong = subpoint.longitude.degrees
            if(haversine((lat, long), (currentLat, currentLong)) < tolerance):
                return t
            t = t + dt

        # If nothing found return None
        return None

    """ Updates the plot to the current time """
    def updateAll(self):
        satellites = self.master.parent.treeview.satList
        self.axis.cla()

        im = pyplot.imread("map.png")
        xstart = self.centerX - self.width/2
        xend = self.centerX + self.width/2
        ystart = self.centerY - self.height/2
        yend = self.centerY + self.height/2
        pyplot.imshow(im, origin = "upper", extent = [xstart, xend, ystart, yend])
        pyplot.yscale("linear")
        pyplot.gca().set_aspect("auto")
        pyplot.axis("off")

        for sat in satellites:
            self.plot(sat)

        self.master.canvas.draw()


    """ Downloads OpenStreetMap tiles given the zoom level and tile indices. These are combined in drawMap() to make a complete image """
    def download_url(self, zoom, xtile, ytile, filename):
        
        url = "http://c.tile.openstreetmap.org/%d/%d/%d.png" % (zoom, xtile, ytile)
        dir_path = "tiles/%d/%d/" % (zoom, xtile)
        download_path = "maps/map%d%d%d.png" % (zoom, xtile, ytile)
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        if(not os.path.isfile(download_path)):
            print("downloading " + url)
            req = urllib.request.Request(url, data = None, headers = header)
            source = urllib.request.urlopen(req)
            content = source.read()
            source.close()
            destination = open(filename,'wb')
            destination.write(content)
            destination.close()
        else:
            print("skipped " +  url)

    """ Helper function to horizontally concatenate map tile images """
    def get_concat_h(self, im1, im2):
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    """ Helper function to vertically concatenate map tile images """
    def get_concat_v(self, im1, im2):
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst

    """ Combines map tile images to make a full map """
    def drawMap(self):
        if os.path.exists("map.png"):
            os.remove("map.png")
        for i in range(self.left, self.left + 4):
            self.download_url(self.zoom, i, self.top, "maps/map" + str(self.zoom) + str(i) + str(self.top) + ".png")
            vert_im = Image.open("maps/map" + str(self.zoom) + str(i) + str(self.top) + ".png")
            for j in range(self.top + 1, self.top + 4):
                self.download_url(self.zoom, i, j, "maps/map" + str(self.zoom) + str(i) + str(j) + ".png")
                new_im = Image.open("maps/map" + str(self.zoom) + str(i) + str(j) + ".png")
                vert_im = self.get_concat_v(vert_im, new_im)
            if(i == self.left):
                hor_im = vert_im
            else:
                hor_im = self.get_concat_h(hor_im, vert_im)
        hor_im.save("map.png")

    def zoomIn(self, event):
        if(self.zoom >= 20):
            return

        self.zoom = self.zoom + 1
        tilesAcross = 2**self.zoom
        self.width = self.width/2
        self.height = self.height/2

        # Top left quadrant
        if(event.xdata <= self.centerX and event.ydata >= self.centerY):
            self.centerX = self.centerX - self.width/2
            self.centerY = self.centerY + self.height/2
            self.top = self.top*2
            self.left = self.left*2
            self.zoomHistory.append(1)

        # Top right quadrant
        elif(event.xdata >= self.centerX and event.ydata >= self.centerY):
            self.centerX = self.centerX + self.width/2
            self.centerY = self.centerY + self.height/2
            self.top = self.top*2
            self.left = self.left*2 + int(tilesAcross/(2**(self.zoom - 2)))
            self.zoomHistory.append(2)

        # Bottom left quadrant
        elif(event.xdata <= self.centerX and event.ydata <= self.centerY):
            self.centerX = self.centerX - self.width/2
            self.centerY = self.centerY - self.height/2
            self.top = self.top*2 + int(tilesAcross/(2**(self.zoom - 2)))
            self.left = self.left*2
            self.zoomHistory.append(3)

        # Bottom right quadrant
        elif(event.xdata >= self.centerX and event.ydata <= self.centerY):
            self.centerX = self.centerX + self.width/2
            self.centerY = self.centerY - self.height/2
            self.left = self.left*2 + int(tilesAcross/(2**(self.zoom - 2)))
            self.top = self.top*2 + int(tilesAcross/(2**(self.zoom - 2)))
            self.zoomHistory.append(4)

        self.drawMap()
        self.updateAll()

    def zoomOut(self, event):
        if len(self.zoomHistory) == 0:
            return
        
        self.zoom = self.zoom - 1
        tilesAcross = 2**self.zoom
        self.width = self.width*2
        self.height = self.height*2

        # Top left quadrant
        if self.zoomHistory[-1] == 1:
            self.centerX = self.centerX + self.width/4
            self.centerY = self.centerY - self.height/4
            self.top = int(self.top/2)
            self.left = int(self.left/2)

        # Top right quadrant
        elif self.zoomHistory[-1] == 2:
            self.centerX = self.centerX - self.width/4
            self.centerY = self.centerY - self.height/4
            self.top = int(self.top/2)
            self.left = int((self.left - int(tilesAcross/(2**(self.zoom - 1))))/2) - 1

        # Bottom left quadrant
        elif self.zoomHistory[-1] == 3:
            self.centerX = self.centerX + self.width/4
            self.centerY = self.centerY + self.height/4
            self.top = int((self.top - int(tilesAcross/(2**(self.zoom - 1))))/2) - 1
            self.left = int(self.left/2)

        # Bottom right quadrant
        elif self.zoomHistory[-1] == 4:
            self.centerX = self.centerX - self.width/4
            self.centerY = self.centerY + self.height/4
            self.left = int((self.left - int(tilesAcross/(2**(self.zoom - 1))))/2) - 1
            self.top = int((self.top - int(tilesAcross/(2**(self.zoom - 1))))/2) - 1

        self.zoomHistory.pop()
        self.drawMap()
        self.updateAll()

    def lla2ecef(self, lat, lng, alt):
        #lla = [lat (deg), lon (deg), altitude (km)]
        #ecef = km

        d2r = pi/180
        f = (1-1/298.257223563)^2 #WGS84 flattening
        R = 6378.1370 #WGS84 equatorial radius (km)

        lat = lat*d2r
        lon = lon*d2r

        lmbda = atan(f*tan(lat)); #mean sea level at lat
        slambda = sin(lmbda)
        clambda = cos(lmbda)

        r = sqrt( R**2/(1+(1/f-1)*slambda**2) ) #radius at surface point
        k1 = r*clambda + alt*cos(lat)

        ecef = [k1*cos(lng), k1*sin(lng), r*slambda + alt*sin(lat)]
        return ecef

"""
plotter = TaskerOrbitPlotter()
start = datetime(2019, 10, 13, 1, 38, 0)
end = start + timedelta(seconds = 20000)
plotter.show()
"""
