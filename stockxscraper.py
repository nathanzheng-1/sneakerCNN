import urllib.request

from bs4 import BeautifulSoup as soup
import csv
import os 

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
urllist = []
valuelist = []

csv_file = open('percentages.csv', 'w', newline = '')
csv_writer = csv.writer(csv_file)


for i in range(1): #changeable to # of pages
    page_url = "https://stockx.com/sneakers/top-selling?page=" + str(i+1)
    uClient = urllib.request.Request(url=page_url, headers=headers)
    fullpage = urllib.request.urlopen(uClient)
    pagetext = soup(fullpage, "lxml")
    tiles = pagetext.findAll('div', class_ = 'tile browse-tile false')

    print('scraped page ' + str(i + 1))
    for j in range(len(tiles)):
        urls = tiles[j].find('a')['href']
        urllist.append("https://stockx.com" + urls)
    
for k in range(3): #change to len(urllist)
    pageurl = urllist[k]
    pageClient = urllib.request.Request(url=pageurl, headers=headers)
    fullpage = urllib.request.urlopen(pageClient)
    htmlpage = soup(fullpage, "lxml")

    print('scraped item ' + str(k+1))
    percentage = htmlpage.findAll('div', class_ = 'gauge-value')[1].text
    value = percentage.split("%")[0]
    valuelist.append(value)
    csv_writer.writerow([value])

    print('downloading image ' + str(k+1))
    picture_url = htmlpage.find('div', class_= 'image-container' )
    picture_url2 = picture_url.find('img')['src']
    urllib.request.urlretrieve(picture_url2, str(k + 1))


csv_file.close()




