import time

import pandas as pd
import re
from selenium import webdriver

browser=webdriver.Chrome()

class Paper_Detailer:
    def __init__(self,paper):
        self.paper=paper
        self.start=1 #The begining row
        self.browser=browser
    def parse(self,text):
        resultList = re.findall(r"FileName=(.*?)&DbName=(.*?)&DbCode=(.*?)&", text)
        return "https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=" + resultList[0][
            2] + "&dbname=" + resultList[0][1] + "&filename=" + resultList[0][0]

    def get_latest_row(self):
        if 10 in self.paper.columns or '10' in self.paper.columns:
            selector = 10 if 10 in self.paper.columns else '10'
            auxiliary = 9 if 9 in self.paper.columns else '9'
            for i in range(0, self.paper.__len__() + 1):
                if pd.isna(self.paper.loc[i, selector]) and not pd.isna(self.paper.loc[i, auxiliary]):
                    return i
            return self.paper.__len__()
        else:
            return 1
        
        
        
    def test(self):
        self.start = self.get_latest_row(self.paper)
        try:
            for i in range(self.start, self.paper.__len__() + 1):
                if pd.isna(self.paper.iloc[i, 9]):
                    continue

                browser.get(self.parse(self.paper.iloc[i, 9]))
                authors = browser.find_elements("xpath", '//*[@id="authorpart"]/span')
                authors_str = ''
                for j in authors:
                    authors_str = authors_str + " " + j.text
                keyWords = browser.find_element("xpath", '/html/body/div[2]/div[1]/div[3]/div/div/div[5]/p')
                page = browser.page_source
                total = re.findall(r"专辑\S*?p>(.*?)</p>[\s\S]*专题\S*?p>(.*?)</p", page)
                album = total[0][0]
                topics = total[0][1]
                self.paper.loc[i, 10 if 10 in self.paper.columns else '10'] = authors_str
                self.paper.loc[i, 11 if 11 in self.paper.columns else '11'] = keyWords.text
                self.paper.loc[i, 12 if 12 in self.paper.columns else '12'] = album
                self.paper.loc[i, 13 if 13 in self.paper.columns else '13'] = topics
                time.sleep(8)
        except:
            self.paper.to_csv('All.csv', encoding='utf-8-sig', header=None)



