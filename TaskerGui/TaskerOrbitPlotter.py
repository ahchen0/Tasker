from poliastro.twobody.orbit import Orbit
from poliastro.plotting.core import OrbitPlotter2D
from spacecraft2 import spacecraft
from poliastro.bodies import Earth
from math import pi, floor
from astropy.time import Time
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

	def plot(self, i):
		sat = self.catalog[i]

		# Calculate semi-major axis
		mu = float(398600) # km^3/s^2
		n = float(sat.meanMotion)
		a = mu**(1/3)/(2*n*pi)**(2/3)

		# Define time in astropy
		time = Time(self.convertTime(int(sat.epochYear), float(sat.epochDay)), format = "datetime")
		# Define orbit
		orbit = Orbit.from_classical(Earth, a, float(sat.eccentricity), float(sat.inclination),
										float(sat.raan), float(sat.argumentOfPerigee),
										float(sat.meanAnomaly), time)

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


plotter = TaskerOrbitPlotter()
plotter.plot(0)
