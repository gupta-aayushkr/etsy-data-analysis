import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

shopName = input("Enter the name of the Shop: ")
lastPage = int(input("Enter the last Paginated Page: "))

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
        time.sleep(t)
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

soldUnits.head(10).plot(kind='barh')
plt.show()