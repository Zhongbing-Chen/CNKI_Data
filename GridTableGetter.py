import time
import traceback
from dataclasses import dataclass

import selenium
import pandas as pd
import re
from seleniumwire import webdriver


target=pd.read_excel('CSSCI期刊.XLSX')


browser = webdriver.Chrome()

@dataclass
class GridTableGetter:
    def __init__(self,target,pages=1):
        self.browser=browser
        self.pages=pages
        self.advSearch="https://kns.cnki.net/kns8/AdvSearch"
        self.journalInputElement='//*[@id="gradetxt"]/dd[3]/div[2]/input'
        self.searchKeyElement='/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input'
        self.result=pd.read_csv('paper_all.csv',names=range(1,10))
        self.target=target

    def intercepter_helper(self):
        def intercepter(request):
            if request.method != 'GET' and re.findall(r'IsSearch=false', request.body.decode()):
                request.body = re.sub(r'CurPage=\d+?&', 'CurPage=' + str(self.pages) + '&', request.body.decode())

        return intercepter
    def search(self):
        self.browser.request_interceptor = self.intercepter_helper()
        self.browser.get(self.advSearch)
        self.journalInput=self.browser.find_element('xpath',self.journalInputElement)
        self.searchKey=self.browser.find_element('xpath',self.searchKeyElement)
        self.journalInput.send_keys(self.target)
        time.sleep(1)

        self.searchKey.click()
        time.sleep(5)
        self.nextPage=browser.find_element("xpath", '//*[@id="PageNext"]')

        if self.pages>1:
            self.nextPage.click()
            self.scrapy()
        else:
            self.scrapy()
    def scrapy(self):
        while sum(self.result.loc[self.result.__len__()-1,:].isnull() == True)>4 \
                or self.result.__len__()==0 \
                or self.result.loc[self.result.__len__()-1, 5] > '2015-01-01' \
                or gridTableGetter.result.loc[self.result.__len__()-1,4]!=self.target:
            time.sleep(2)
            for i in range(1, 21):
                row = self.result.__len__() + 1
                for j in range(1, 9):
                    self.result.loc[row, j] = browser.find_element("xpath", '//*[@id="gridTable"]/table/tbody/tr[' + str(
                        i) + ']/td[' + str(j) + ']').text
                self.result.loc[row, 9] = browser.find_element("xpath", '//*[@id="gridTable"]/table/tbody/tr[' + str(
                    i) + ']/td[2]/a').get_attribute('href')
            self.pages += 1
            print(self.pages)
            nextPage = browser.find_element("xpath", '//*[@id="PageNext"]').click()

            time.sleep(3)
        self.result.to_csv('paper_all.csv',header=None,index=None)
        self.pages='Done'



gridTableGetter = GridTableGetter('安徽史学', 9)

items=0
try:
    for i in range(0, target.__len__()):
        if target.loc[i, 'Pages']=='Done':
            continue
        items=i
        gridTableGetter = GridTableGetter(target.loc[i, '期刊名称'], target.loc[i, 'Pages'])
        gridTableGetter.search()
        target.loc[i, 'Pages'] = gridTableGetter.pages
        target.to_excel('CSSCI期刊.xlsx', index=None)
except:

    target.loc[items,'Pages']=gridTableGetter.pages
    gridTableGetter.result.to_csv('paper_all.csv', header=None,index=None)
    target.to_excel('CSSCI期刊.xlsx', index=None)
    traceback.print_exc()
    raise Exception("Restart")