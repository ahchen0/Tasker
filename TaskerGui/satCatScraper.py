""" Script for scraping satellite catalog
on celestrak.com for satellite data """

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from collections import OrderedDict
from spacecraft import spacecraft

""" Gets data from internet """
myurl = "https://celestrak.com/pub/satcat.txt"
uClient = uReq(myurl)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
data_string = page_soup.contents[0]
data_lines = data_string.splitlines()

""" Stores data in txt file and list"""
spacecraftCatalog = []
file = open("spacecraftCatalog.txt", "w")
for line in data_lines:
	file.write(line + "\n")
	spacecraftCatalog.append(spacecraft(line))
file.close()
