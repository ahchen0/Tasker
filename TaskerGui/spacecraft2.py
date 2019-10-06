# Class that contains information for a spacecraft

class spacecraft:

	def __init__(self, name, line1, line2):
		self.name = name.strip()

		# Line 1
		self.catalogNumber = line1[2:8]
		self.intlDesignator = line1[9:17]
		self.epochYear = line1[18:20]
		self.epochDay = line1[20:32]
		self.firstDerivativeOfMeanMotion = line1[33:43]
		self.secondDerivativeOfMeanMotion = line1[44:52]
		self.dragTerm = line1[53:61]
		self.ephemerisType = line1[62]
		self.elementSetNumber = line1[64:68]
		self.CheckSum1 = line1[68]

		# Line 2
		self.inclination = line2[8:16]
		self.raan = line2[17:25]
		self.eccentricity = line2[26:33]
		self.argumentOfPerigee = line2[34:42]
		self.meanAnomaly = line2[43:51]
		self.meanMotion = line2[52:63]
		self.revolutionNumberAtEpoch = line2[63:68]
		self.CheckSum2 = line2[68]
