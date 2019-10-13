from poliastro.twobody.orbit import Orbit
from poliastro.plotting.core import OrbitPlotter2D
from spacecraft2 import spacecraft
from poliastro.bodies import Earth
from poliastro.frames import Planes
from poliastro.twobody.angles import M_to_nu
from math import pi, floor, sin, cos, tan
from astropy.time import Time, TimeDelta
from astropy.units import Quantity, dimensionless_unscaled
from datetime import datetime

class TaskerOrbitPlotter:

    def __init__(self):
        # Read in satellite catalog
        self.catalog = []
        file = open("satCat.txt", "r")
        lines = file.readlines()
        lineNum = 0
        while(lineNum < len(lines)):
            name = lines[lineNum]
            line1 = lines[lineNum + 1]
            line2 = lines[lineNum + 2]
            lineNum = lineNum + 3
            item = spacecraft(name, line1, line2)
            self.catalog.append(item)

    # Plot the orbit of the satellite with index i. [NOT FINISHED]
    def plot(self, i):
        sat = self.catalog[i]

        # Calculate semi-major axis
        mu = float(398600) # km^3/s^2
        n = float(sat.meanMotion)
        semiMajorAxis = Quantity(mu**(1/3)/(2*n*pi/86400)**(2/3), "km")

        # Calculate true anomaly (calculated as third order 
        # Fourier expansion of mean anomaly)
        M = Quantity(float(sat.meanAnomaly)*pi/180, 'rad')
        e = Quantity(float(sat.eccentricity), dimensionless_unscaled)
        """
        term0 = M
        term1 = (2*e - (1/4)*e**3)*sin(M)
        term2 = (5/4)*e**2*sin(2*M)
        term3 = (13/12)*e**3*sin(3*M)
        trueAnomaly = Quantity(term0 + term1 + term2 + term3, "radian")
        """
        trueAnomaly = M_to_nu(M, e)


        # Define time in astropy
        time = Time(self.convertTime(int(sat.epochYear), float(sat.epochDay)), format = "datetime")

        # Define quantities
        eccentricity = Quantity(float(sat.eccentricity), dimensionless_unscaled)
        inclination = Quantity(float(sat.inclination), "degree")
        raan = Quantity(float(sat.raan), "degree")
        argumentOfPerigee = Quantity(float(sat.argumentOfPerigee), "degree")

        # Define orbit
        self.orbit = Orbit.from_classical(Earth, semiMajorAxis, eccentricity,
        inclination, raan, argumentOfPerigee, trueAnomaly, time, Planes.EARTH_EQUATOR)

        # Plot
        """
        plotter = OrbitPlotter2D()
        fig = plotter.plot(orbit)
        fig.show()
        """

    def convertTime(self, epochYear, epochDay):
        # Calculate Year
        if epochYear < 0:
            year = 1900 + epochYear
        else:
            year = 2000 + epochYear

        # Determine if year is leap year
        if(epochYear % 4 == 0 and (epochYear % 100 != 0 or epochYear % 400 == 0)):
            isLeapYear = 1
        else:
            isLeapYear = 0

        # Calculate month and day
        if(1 <= epochDay and epochDay <= 31):
            month = 1
            day = floor(epochDay)
        elif(32 <= epochDay and epochDay <= 59 + isLeapYear):
            month = 2
            day = floor(epochDay) - 31
        elif(60 + isLeapYear <= epochDay and epochDay <= 90 + isLeapYear):
            month = 3
            day = floor(epochDay) - 59 - isLeapYear
        elif(91 + isLeapYear <= epochDay and epochDay <= 120 + isLeapYear):
            month = 4
            day = floor(epochDay) - 90 - isLeapYear
        elif(121 + isLeapYear <= epochDay and epochDay <= 151 + isLeapYear):
            month = 5
            day = floor(epochDay) - 120 - isLeapYear
        elif(152 + isLeapYear <= epochDay and epochDay <= 181 + isLeapYear):
            month = 6
            day = floor(epochDay) - 151 - isLeapYear
        elif(182 + isLeapYear <= epochDay and epochDay <= 212 + isLeapYear):
            month = 7
            day = floor(epochDay) - 181 - isLeapYear
        elif(213 + isLeapYear <= epochDay and epochDay <= 243 + isLeapYear):
            month = 8
            day = floor(epochDay) - 212 - isLeapYear
        elif(244 + isLeapYear <= epochDay and epochDay <= 273 + isLeapYear):
            month = 9
            day = floor(epochDay) - 243 - isLeapYear
        elif(274 + isLeapYear <= epochDay and epochDay <= 304 + isLeapYear):
            month = 10
            day = floor(epochDay) - 273 - isLeapYear
        elif(305 + isLeapYear <= epochDay and epochDay <= 334 + isLeapYear):
            month = 11
            day = floor(epochDay) - 304 - isLeapYear
        elif(335 + isLeapYear <= epochDay and epochDay <= 365 + isLeapYear):
            month = 12
            day = floor(epochDay) - 334 - isLeapYear
        else:
            month = 0
            day = 0
            print("Invalid date")

        hour = floor((epochDay - floor(epochDay))*24)
        minute = floor((epochDay-floor(epochDay))*1440 - hour*60)
        second = floor((epochDay-floor(epochDay))*86400 - hour*3600 - minute*60)

        return datetime(year, month, day, hour, minute, second)

    def calcGroundTrack(self):
        days = 3
        secondsPerDay = 86400;
        maxTime = secondsPerDay * days;

        t = 0;
        dt = 30;

        self.position = []

        while t <= maxTime:
            newOrbit = self.orbit.propagate(TimeDelta(t, format = 'sec'))
            self.position.append(newOrbit.r)
            t = t + dt

    def eci2ecef(self, position):
        pass

        

plotter = TaskerOrbitPlotter()
plotter.plot(89)
plotter.calcGroundTrack()
import pdb
pdb.set_trace()
