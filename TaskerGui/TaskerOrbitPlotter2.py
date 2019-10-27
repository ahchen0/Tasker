from skyfield.api import Topos, load
from datetime import datetime, timedelta
from matplotlib import pyplot, pylab
from matplotlib.figure import Figure
from math import pi
from spacecraft2 import spacecraft
from haversine import haversine, Unit

"""
Task for calculating ground tracks. To use:
    1. Initialize with name of satellite
    2. Create start time as datetime object
    3. Create end time as datetime object
    4. Call plot with start and end time
"""

class TaskerOrbitPlotter:

    def __init__(self, master):
        self.master = master
        self.satellites = load.tle("https://celestrak.com/NORAD/elements/active.txt")
        

    def show(self):
        im = pyplot.imread("map2.jpg")
        pyplot.imshow(im, origin = "upper", extent = [-180, 180, -90,
        90])

        self.fig = pyplot.gcf()
        self.axis = pyplot.gca()
        return self.fig

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

        for dt in [dt, -dt]:
            t = time
            while True:
                currentTime = ts.utc(t.year, t.month, t.day, t.hour, t.minute,
                                     t.second)
                geocentric = self.satellite.at(currentTime)
                subpoint = geocentric.subpoint()
                latitudes.append(subpoint.latitude.radians*180/pi)
                longitudes.append(subpoint.longitude.radians*180/pi)
                t = t + dt
                if len(longitudes) >= 2 and abs(longitudes[-2] - longitudes[-1]) > 300:
                    break
                if isGeosynchronous and abs(t - time) >= timedelta(seconds =
                86400):
                    break

        i = 1
        x = []
        x.append(longitudes[0])
        y = []
        y.append(latitudes[0])
        while i < len(longitudes):
            if abs(longitudes[i-1] - longitudes[i]) > 300:
                pyplot.plot(x, y, color = 'y', linewidth = 4)
                x = []
                y = []
            else:
                x.append(longitudes[i])
                y.append(latitudes[i])
            i = i + 1
                
        pyplot.plot(x, y, color = 'y', linewidth = 4)
        pyplot.scatter(longitudes[0], latitudes[0], s = 200, color = 'y')
        pyplot.gca().annotate(sat.name, (longitudes[0], latitudes[0]))

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

        im = pyplot.imread("map2.jpg")
        pyplot.imshow(im, origin = "upper", extent = [-180, 180, -90,
        90])

        for sat in satellites:
            self.plot(sat)

        self.master.canvas.draw()



"""
plotter = TaskerOrbitPlotter()
start = datetime(2019, 10, 13, 1, 38, 0)
end = start + timedelta(seconds = 20000)
plotter.show()
"""
