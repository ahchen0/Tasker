#!/usr/bin/python

from sys import argv
import os
import math
import urllib.request
import random
import os.path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def download_url(zoom, xtile, ytile, filename):
    # Switch between otile1 - otile4
    subdomain = random.randint(1, 4)
    
    url = "http://c.tile.openstreetmap.org/%d/%d/%d.png" % (zoom, xtile, ytile)
    dir_path = "./%d/%d/" % (zoom, xtile)
    download_path = "tiles/%d/%d/%d.png" % (zoom, xtile, ytile)
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    if(not os.path.isfile(download_path)):
        print("downloading " + url)
        req = urllib.request.Request(url, data = None, headers = header)
        source = urllib.request.urlopen(req)
        content = source.read()
        source.close()
        destination = open(filename,'wb')
        destination.write(content)
        destination.close()
        #img = mpimg.imread(filename)
        #plt.imshow(img)
        #plt.show()
    else: print("skipped " +  url)

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

for i in range(0, 4):
    download_url(2, i, 0, "map" + str(i) + "0.png")
    vert_im = Image.open("map" + str(i) + "0.png")
    for j in range(1, 4):
        download_url(2, i, j, "map" + str(i) + str(j) + ".png")
        new_im = Image.open("map" + str(i) + str(j) + ".png")
        vert_im = get_concat_v(vert_im, new_im)
    if(i == 0):
        hor_im = vert_im
    else:
        hor_im = get_concat_h(hor_im, vert_im)

"""  
download_url(1, 0, 0, "map1.png")
download_url(1, 0, 1, "map2.png")
download_url(1, 1, 0, "map3.png")
download_url(1, 1, 1, "map4.png")

im00 = Image.open("map1.png")
im01 = Image.open("map2.png")
im10 = Image.open("map3.png")
im11 = Image.open("map4.png")

im_left = get_concat_v(im00, im01)
im_right = get_concat_v(im10, im11)
im = get = get_concat_h(im_left, im_right)
"""
hor_im.save("map.png")
plt.imshow(hor_im)
plt.show()