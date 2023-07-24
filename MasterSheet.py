import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import random
import math
import matplotlib.pyplot as plt
import glob
#run later -- quirkyclickprint

csv_files = glob.glob('*-SoldUnits.{}'.format('csv'))
print(csv_files)

df_csv_append = pd.DataFrame()

# append the CSV files
l = []

for f in csv_files:
    l.append(pd.read_csv(f))

df_res = pd.concat(l, ignore_index=True)

df_res.to_csv('Master.csv')