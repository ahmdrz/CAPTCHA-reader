# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 12:37:24 2016

@author: aiden
"""
import requests
import bs4
import time
import urllib
# import base64

while True :
    url = "http://student.iaun.ac.ir"
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text)
    images = soup.find_all('img')
    img = images[1]
    link = img['src']
    link = link[link.index('=')+1:] #get captcha encrypted text
    link = urllib.unquote(link) #url decoding
    # link = base64.b64decode(link) #base64 decodisng
    print link
    time.sleep(1) # make a delay
