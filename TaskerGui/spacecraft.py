# Class that contains information for a spacecraft
class spacecraft:
	intlDesignator = ""
	catalogNumber = ""
	multipleNameFlag = ""
	payloadFlag = ""
	operationalStatusCode = "" # U = currently operational
	name = ""
	source = ""
	launchDate = ""
	launchSite = ""
	decayDate = ""
	orbitalPeriod = "" # minutes
	inclination = "" # degrees
	apogee = "" # km
	perigee = "" # km
	radarCrossSection = "" # m^2
	orbitalStatusCode = ""

	# Constructor: Takes a line from the Celestrak txt database as argument
	# (each line contains data for one spacecraft)
	def __init__(self, line):
		self.intlDesignator = line[0:11].strip()
		self.catalogNumber = line[13:18].strip()
		self.multipleNameFlag = line[19].strip()
		self.payloadFlag = line[20].strip()
		self.operationalStatusCode = line[21].strip()
		self.name = line[23:47].strip()
		self.source = line[49:54].strip()
		self.launchDate = line[56:66].strip()
		self.launchSite = line[68:73].strip()
		self.decayDate = line[75:85].strip()
		self.orbitalPeriod = line[87:94].strip()
		self.inclination = line[96:101].strip()
		self.apogee = line[103:109].strip()
		self.perigee = line[111:117].strip()
		self.radarCrossSection = line[119:127].strip()
		self.orbitalStatusCode = line[129:132].strip()

