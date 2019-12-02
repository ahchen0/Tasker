"""
Script for scraping satellite catalog
on celestrak.com for satellite data
"""

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from collections import OrderedDict

class Scraper:

	def __init__(self):
		# Gets data from internet
		myurl = "https://celestrak.com/NORAD/elements/active.txt"
		uClient = uReq(myurl)
		page_html = uClient.read()
		uClient.close()
		page_soup = soup(page_html, "html.parser")
		data_string = page_soup.contents[0]
		data_lines = data_string.splitlines()

		# Stores data in txt file
		file = open("satCat.txt", "w")
		for line in data_lines:
			file.write(line + "\n")
		file.close()
