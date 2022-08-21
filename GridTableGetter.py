import time
import traceback
from dataclasses import dataclass

import selenium
import pandas as pd
import re

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
import ddddocr
from ddddocr import DdddOcr

target=pd.read_excel('CSSCI期刊.XLSX')
chrome_options = Options()
chrome_options.add_argument("--headless")

browser = webdriver.Chrome()

@dataclass
class GridTableGetter:
    def __init__(self,target,pages=1):
        self.browser=browser
        self.pages=pages
        self.advSearch="http://kns.cnki.net/kns8/AdvSearch"
        self.journalInputElement='//*[@id="gradetxt"]/dd[3]/div[2]/input'
        self.searchKeyElement='/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input'
        self.result=pd.read_csv('paper_all.csv',names=range(1,10))
        self.target=target
        self.ocr=ddddocr.DdddOcr()

    def intercepter_helper(self):
        def intercepter(request):
            if request.path.endswith(('.png', '.jpg', '.gif')):
                request.abort()
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
        time.sleep(2)
        self.nextPage=browser.find_element("xpath", '//*[@id="PageNext"]')

        if self.pages>1:
            self.nextPage.click()
            self.scrapy()
        else:
            self.scrapy()
    # TODO settle down the problem like out of index due to page number
    def scrapy(self):
        while (sum(self.result.loc[self.result.__len__()-1,:].isnull() == True)>4 \
                or self.result.__len__()==0 \
                or self.result.loc[self.result.__len__()-1, 5] > '2015-01-01' \
                or gridTableGetter.result.loc[self.result.__len__()-1,4]!=self.target):
                # and not self.result.loc[self.result.__len__()-1, 5] < '2015-01-01':
            time.sleep(0.5)
            self.verify()
            time.sleep(0.5)
            for i in range(1, 21):
                row = self.result.__len__() + 1
                for j in range(1, 9):
                    self.result.loc[row, j] = browser.find_element("xpath", '//*[@id="gridTable"]/table/tbody/tr[' + str(
                        i) + ']/td[' + str(j) + ']').text
                self.result.loc[row, 9] = browser.find_element("xpath", '//*[@id="gridTable"]/table/tbody/tr[' + str(
                    i) + ']/td[2]/a').get_attribute('href')
            self.pages += 1
            print("This is the "+str(self.pages)+"th page in this journal")

            # nextPage = browser.find_element("xpath", '//*[@id="PageNext"]')
            # nextPage.click()
            time.sleep(0.5)
            WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="PageNext"]'))).click()


        self.result.to_csv('paper_all.csv',header=None,index=None)
        self.pages='Done'
    def verify(self):
        for i in range(0,3):
            time.sleep(1)
            if len(self.browser.find_elements('xpath', '//*[@id="changeVercode"]')) > 0:

                self.verification_code = self.browser.find_element('xpath', '//*[@id="changeVercode"]')
                time.sleep(0.5)
                self.verification_code_text = self.ocr.classification(self.verification_code.screenshot_as_png)
                code_input_box = self.browser.find_element('xpath', '//*[@id="vericode"]')
                code_input_box.clear()
                code_input_box.send_keys(self.verification_code_text)
                enter_button = self.browser.find_element('xpath', '//*[@id="checkCodeBtn"]')
                enter_button.click()
                print("The verification code is "+self.verification_code_text)
                time.sleep(5)
            else:
                time.sleep(0.1)
                break





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
    gridTableGetter.result.to_csv('paper_all.csv', header=None,index=None,encoding='utf-8-sig')
    target.to_excel('CSSCI期刊.xlsx', index=None)
    traceback.print_exc()
    raise Exception("Restart")

# verification_code=browser.find_element('xpath','//*[@id="changeVercode"]')
# ocr = ddddocr.DdddOcr()
#
# verification_code_text=ocr.classification(verification_code.screenshot_as_png)
#
# for i in range(0, 3):
#     if len(browser.find_elements('xpath', '//*[@id="changeVercode"]')) > 0:
#         verification_code = browser.find_element('xpath', '//*[@id="changeVercode"]')
#         verification_code_text = ocr.classification(verification_code.screenshot_as_png)
#         code_input_box = browser.find_element('xpath', '//*[@id="vericode"]')
#         code_input_box.clear()
#         code_input_box.send_keys(verification_code_text)
#         enter_button = browser.find_element('xpath', '//*[@id="checkCodeBtn"]')
#         enter_button.click()
#     else:
#         break