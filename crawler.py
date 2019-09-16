import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from collections import OrderedDict

class spacecraft:
	launchDate = None
	catalogNumber = None
	val3 = None
	name = None
	origin = None
	launchDate2 = None
	launchSite = None
	decayDate = None
	val8 = None
	val9 = None
	val10 = None
	val11 = None
	val12 = None
	val13 = None

	def __init__(self, launchDate = None, catalogNumber = None, val3 = None, name = None, origin = None, launchDate2 = None, launchSite = None, decayDate = None, val8 = None, val9 = None, val10 = None, val11 = None, val12 = None, val13 = None):
		self.launchDate = launchDate
		self.catalogNumber = catalogNumber
		self.val3 = val3
		self.name = name
		self.origin = origin
		self.launchDate2 = launchDate2
		self.launchSite = launchSite
		self.decayDate = decayDate
		self.val8 = val8
		self.val9 = val9
		self.val10 = val10
		self.val11 = val11
		self.val12 = val12
		self.val13 = val13
		

myurl = "https://celestrak.com/pub/satcat.txt"
uClient = uReq(myurl)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
data_string = page_soup.contents[0]
data_lines = data_string.splitlines()

spacecraftCatalog = []

for line in data_lines:
	launchDate = line[0:8].strip()
	catalogNumber = line[13:17].strip()
	val3 = line[19:21].strip()
	name = line[23:47].strip()
	origin = line[49:54].strip()
	launchDate2 = line[56:65].strip()
	launchSite = line[68:72].strip()
	decayDate = line[75:84].strip()
	val8 = line[86:93].strip()
	val9 = line[95:100].strip()
	val10 = line[102:108].strip()
	val11 = line[110:116].strip()
	val12 = line[118:126].strip()
	val13 = line[128:].strip()

	spacecraftCatalog.append(spacecraft(launchDate, catalogNumber, val3, name, origin, launchDate2, launchSite, decayDate, val8, val9, val10, val11, val12, val13))

import pdb
pdb.set_trace()
