import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import random
import math
import matplotlib.pyplot as plt
import datetime

shopName = input("Enter the name of the Shop: ")

#Determining Last Paginated Page

lastPage = 1
pagination = []

url = f"https://www.etsy.com/in-en/shop/{shopName}/sold"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

for pages in soup.find_all("span", class_="screen-reader-only"):
        pagination.append(pages.text.strip())
        print(f'{pagination}')

#if there is only one page try block will handle the error
try:
    lastPage = pagination[-2]
    lastPage = int(lastPage[5:])
    print(f"lastpage={lastPage}")
except:
    print(f"lastpage={lastPage}")

time.sleep(5)

#Calculating Crawl
firstPage = 1
title = []

crawlRate = math.ceil(lastPage/10)
lastLoop = crawlRate + 1

print(f"lastloop = {lastLoop}")
url = f"https://www.etsy.com/in-en/shop/{shopName}"

#Function for Crawling
def crawl(firstPage, lastPage):
    for i in range(firstPage, lastPage+1):
        t = random.randint(20, 30)
        print(i)
        localurl = f"{url}/sold?ref=pagination&page={i}"
        # time.sleep(t)
        r = requests.get(localurl)
        soup = BeautifulSoup(r.content, 'html.parser')

        for heading in soup.find_all("h3", class_="wt-text-caption v2-listing-card__title wt-text-truncate"):
            title.append(heading.text.strip())
            print(f'{i} {title}')

#THINK FOR FORMULAE --
for i in range(1, lastLoop):
    print(f"value of {i}")
    if(lastLoop==2):
        crawl(firstPage, lastPage)
        break
        #endloop

    if(i==1):
        crawl(firstPage, firstPage+10)

    elif(i>1 and i+2<lastLoop):
        crawl(firstPage*i*10+1,firstPage*(i+1)*10)
        time.sleep(300)

    elif(i+1==lastLoop):
        crawl(firstPage*(i-1)*10+1,lastPage)

#All items Sold in Order
items = pd.DataFrame(title, columns=['Title'])
items.to_csv(f'{shopName}-Items.csv')

#Frequency of Item Sold
soldUnits = items['Title'].value_counts()
soldUnits.to_csv(f'{shopName}-SoldUnits.csv')

#Additional Information Added
#Since value_count() converts df to series therefore -
df = pd.read_csv(f"{shopName}-SoldUnits.csv")
now = datetime.datetime.now()
df.insert(0, 'TimeStamp', pd.to_datetime('now').replace(microsecond=0))
df.insert(1, 'Shop Name', f'{shopName}', allow_duplicates = False)
df.to_csv(f'{shopName}-Advance.csv')

#Generating Plots
soldUnits.head(10).plot(kind='barh')
plt.show()

#PixelPressArt