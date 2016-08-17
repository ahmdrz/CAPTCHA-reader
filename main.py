import requests
import bs4
import time
import urllib

i = 0
while True :
	i = i + 1
	url = "http://student.iaun.ac.ir"
	r = requests.get(url)
	soup = bs4.BeautifulSoup(r.text)
	images = soup.find_all('img')
	img = images[1]
	link = url + "/" + img['src']
	urllib.urlretrieve(link,str(i)+".jpg")
	time.sleep(1)

