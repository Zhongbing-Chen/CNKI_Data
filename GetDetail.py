import time

import selenium
import pandas as pd
import re
import traceback
from selenium import webdriver

browser = webdriver.Chrome()

paper=pd.read_csv("./paper1.csv",names=range(0,14),header=None)

def parse(text):
    resultList=re.findall(r"FileName=(.*?)&DbName=(.*?)&DbCode=(.*?)&",text)

    return "https://kns.cnki.net/kcms/detail/detail.aspx?dbcode="+resultList[0][2]+"&dbname="+resultList[0][1]+"&filename="+resultList[0][0]


def get_latest_row(df):
    if 10 in df.columns or '10' in df.columns:
        selector=10 if 10 in df.columns else '10'
        auxiliary=9 if 9 in df.columns else '9'
        for i in range(1,df.__len__()):
            if pd.isna(df.loc[i,selector]) and not pd.isna(df.loc[i,auxiliary]):
                return i
        return df.__len__()
    else:
        return 1


start=get_latest_row(paper)
try:
    for i in range(start, paper.__len__() + 1):
        if pd.isna(paper.iloc[i, 9]):
            continue
        print("This is the "+str(i)+"th item in paper.csv")
        browser.get(parse(paper.iloc[i, 9]))
        authors = browser.find_elements("xpath", '//*[@id="authorpart"]/span')
        authors_str = ''
        for j in authors:
            authors_str = authors_str + " " + j.text
        try:
            keyWords = browser.find_element("xpath", '/html/body/div[2]/div[1]/div[3]/div/div/div[5]/p')
        except:
            keyWords= ""
        page = browser.page_source
        total = re.findall(r"专辑\S*?p>(.*?)</p>[\s\S]*专题\S*?p>(.*?)</p", page)
        album = total[0][0]
        topics = total[0][1]
        paper.loc[i, 10] = authors_str if authors_str.strip()!='' else "None"
        paper.loc[i, 11] = keyWords.text if type(keyWords)!=type("") else "None"
        paper.loc[i, 12] = album
        paper.loc[i, 13] = topics
        time.sleep(8)
except:
        traceback.print_exc()
        paper.to_csv('paper1.csv',encoding='utf-8-sig',header=None,index=None)
paper.to_csv('paper1.csv',encoding='utf-8-sig',header=None,index=None)

