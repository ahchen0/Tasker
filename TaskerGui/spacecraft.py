class spacecraft:
	intlDesignator = None
	catalogNumber = None
	multipleNameFlag = None
	payloadFlag = None
	operationalStatusCode = None # U = currently operational
	name = None
	source = None
	launchDate = None
	launchSite = None
	decayDate = None
	orbitalPeriod = None # minutes
	inclination = None # degrees
	apogee = None # km
	perigee = None # km
	radarCrossSection = None # m^2
	orbitalStatusCode = None

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

