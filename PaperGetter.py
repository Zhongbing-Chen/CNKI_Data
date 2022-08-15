import time

import selenium
import pandas as pd
import re
import requests
from selenium import webdriver

browser = webdriver.Chrome()

browser.get("https://kns.cnki.net/kns8/AdvSearch")

journalInput=browser.find_element("xpath",'//*[@id="gradetxt"]/dd[3]/div[2]/input')
journalInput.send_keys("安徽史学")
searchKey=browser.find_element("xpath",'/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input')
searchKey.click()
time.sleep(25)
df=pd.DataFrame()
df.loc[1,5]="2022-09-09"
while df.loc[df.__len__(),5]>'2015-01-01':
    for i in range(1,21):
        row=df.__len__()+1
        for j in range(1,9):
            df.loc[row,j]=browser.find_element("xpath",'//*[@id="gridTable"]/table/tbody/tr['+str(i)+']/td['+str(j)+']').text
        df.loc[row,9]=browser.find_element("xpath",'//*[@id="gridTable"]/table/tbody/tr['+str(i)+']/td[2]/a').get_attribute('href')
    nextPage=browser.find_element("xpath",'//*[@id="PageNext"]').click()
    time.sleep(25)

df.to_csv("./paper2.csv",encoding='utf-8-sig')

class PaperGetter:
    def __init__(self,browser):
        self.browser=browser

    def search_with_key(self,key):
        journalInput = browser.find_element("xpath", '//*[@id="gradetxt"]/dd[3]/div[2]/input')
        journalInput.send_keys(key)
        searchKey = browser.find_element("xpath", '/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input')
        searchKey.click()