import time

import selenium
import pandas as pd
import re
from selenium import webdriver

browser = webdriver.Chrome()

paper=pd.read_csv("./paper.csv")

def parse(text):
    resultList=re.findall(r"FileName=(.*?)&DbName=(.*?)&DbCode=(.*?)&",text)
    return "https://kns.cnki.net/kcms/detail/detail.aspx?dbcode="+resultList[0][2]+"&dbname="+resultList[0][1]+"&filename="+resultList[0][0]

for i in range(1,paper.__len__()+1):
    if pd.isna(paper.iloc[i,8]):
        continue

    browser.get(parse(paper.iloc[i,8]))
    authors = browser.find_elements("xpath", '//*[@id="authorpart"]/span')
    authors_str=''
    for j in authors:
        authors_str=authors_str+" "+j.text
    keyWords = browser.find_element("xpath", '/html/body/div[2]/div[1]/div[3]/div/div/div[5]/p')
    page = browser.page_source
    total = re.findall(r"专辑\S*?p>(.*?)</p>[\s\S]*专题\S*?p>(.*?)</p", page)
    album = total[0][0]
    topics = total[0][1]
    paper.loc[i,10]=authors_str
    paper.loc[i,11]=keyWords.text
    paper.loc[i,12]=album
    paper.loc[i,13]=topics
    time.sleep(35)



page=browser.page_source
total=re.findall(r"专辑\S*?p>(.*?)</p>[\s\S]*专题\S*?p>(.*?)</p",page)
album=total[0][0]
topics=total[0][1]


