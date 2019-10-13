from skyfield.api import Topos, load
from datetime import datetime, timedelta
from matplotlib import pyplot, pylab
from math import pi

"""
Task for calculating ground tracks. To use:
    1. Initialize with name of satellite
    2. Create start time as datetime object
    3. Create end time as datetime object
    4. Call plot with start and end time
"""

class TaskerOrbitPlotter:

    def __init__(self, satName = "ISS (ZARYA)"):
        self.satellites = load.tle("https://celestrak.com/NORAD/elements/active.txt")
        self.satellite = self.satellites[satName]
        
        """
        ts = load.timescale()
        t = ts.utc(2019, 10, 12, 21, 30, 0)
        geocentric = satellite.at(t)
        
        subpoint = geocentric.subpoint()
        print("Latitude: ", subpoint.latitude)
        print("Longitude: ", subpoint.longitude)
        print("Altitude: ", subpoint.elevation.km)
        """

    def plot(self, timeStart, timeEnd):
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
        
        im = pyplot.imread("map2.jpg")
        implot = pyplot.imshow(im, origin = "upper", extent = [-180, 180, -85,
        85])

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
        pyplot.show()

plotter = TaskerOrbitPlotter()
start = datetime(2019, 10, 13, 1, 38, 0)
end = start + timedelta(seconds = 5400)
plotter.plot(start, end)
