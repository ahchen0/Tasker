from skyfield.api import Topos, load
from datetime import datetime, timedelta
from matplotlib import pyplot, pylab
from matplotlib.figure import Figure
from math import pi

"""
Task for calculating ground tracks. To use:
    1. Initialize with name of satellite
    2. Create start time as datetime object
    3. Create end time as datetime object
    4. Call plot with start and end time
"""

class TaskerOrbitPlotter:

    def __init__(self):
        self.satellites = load.tle("https://celestrak.com/NORAD/elements/active.txt")
        

    def show(self, timeStart, timeEnd):
        ts = load.timescale()

        dt = timedelta(seconds = 30)
        t = timeStart

        latitudes = []
        longitudes = []

        """
        while t < timeEnd:
            currentTime = ts.utc(t.year, t.month, t.day, t.hour, t.minute,
                                 t.second)
            geocentric = self.satellite.at(currentTime)
            subpoint = geocentric.subpoint()
            latitudes.append(subpoint.latitude.radians*180/pi)
            longitudes.append(subpoint.longitude.radians*180/pi)
            t = t + dt
        """
        
        im = pyplot.imread("map2.jpg")
        implot = pyplot.imshow(im, origin = "upper", extent = [-180, 180, -90,
        90])

        """
        i = 1
        x = []
        x.append(longitudes[0])
        y = []
        y.append(latitudes[0])
        while i < len(longitudes):
            if abs(longitudes[i-1] - longitudes[i]) > 300:
                pyplot.plot(x, y, color = 'y')
                x = []
                y = []
            else:
                x.append(longitudes[i])
                y.append(latitudes[i])
            i = i + 1
                
        pyplot.plot(x, y, color = 'y')
        # pyplot.plot(longitudes, latitudes, color = 'y')
        # pyplot.show()
        """

        self.fig = pyplot.gcf()
        return self.fig

    def plot(self, satName = "ISS (ZARYA)", timeStart = datetime.now(),
             timeEnd = datetime.now() + timedelta(seconds = 10000)):
        self.satellite = self.satellites[satName]
        pyplot.figure(self.fig.number)

        ts = load.timescale()
        dt = timedelta(seconds = 30)
        t = timeStart

        latitudes = []
        longitudes = []

        while t < timeEnd:
            currentTime = ts.utc(t.year, t.month, t.day, t.hour, t.minute,
                                 t.second)
            geocentric = self.satellite.at(currentTime)
            subpoint = geocentric.subpoint()
            latitudes.append(subpoint.latitude.radians*180/pi)
            longitudes.append(subpoint.longitude.radians*180/pi)
            t = t + dt

        i = 1
        x = []
        x.append(longitudes[0])
        y = []
        y.append(latitudes[0])
        while i < len(longitudes):
            if abs(longitudes[i-1] - longitudes[i]) > 300:
                pyplot.plot(x, y, color = 'y')
                x = []
                y = []
            else:
                x.append(longitudes[i])
                y.append(latitudes[i])
            i = i + 1
                
        pyplot.plot(x, y, color = 'y')
        # pyplot.plot(longitudes, latitudes, color = 'y')
        # pyplot.show()





plotter = TaskerOrbitPlotter()
start = datetime(2019, 10, 13, 1, 38, 0)
end = start + timedelta(seconds = 20000)
plotter.show(start, end)
