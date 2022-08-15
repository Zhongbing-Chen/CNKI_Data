import json

from seleniumwire import webdriver
from seleniumrequests import Chrome
from urllib.parse import urlencode,urlparse,quote
import time

import selenium
import pandas as pd
import re

def interceptor(request):
    # 拦截.png,.jpg,.gif结尾的请求
    if request.path.endswith(('.png', '.jpg', '.gif')):
        request.abort()
    if request.path=='/kns8/Brief/GetGridTableHtml' and re.findall(r'IsSearch=false',request.body.decode()):
        test=request.body
        test = re.sub(r'CurPage=(\d*)?', 'CurPage=18', test.decode())
        test=re.sub(r'HandlerId=\d*?','HandlerId=1',test)
        request.body=test

        print(len(request.body))

browser = webdriver.Chrome()
browser.request_interceptor = interceptor
browser.get("https://kns.cnki.net/kns8/AdvSearch")
target=pd.read_excel("CSSCI期刊.XLSX")


journalInput=browser.find_element("xpath",'//*[@id="gradetxt"]/dd[3]/div[2]/input')
journalInput.send_keys("安徽史学")
searchKey=browser.find_element("xpath",'/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input')
searchKey.click()
time.sleep(25)
test=''
test1=''
for i in browser.requests:
    if i.method!='GET' and i.path=='/kns8/Brief/GetGridTableHtml':
        test=i.body



test=re.sub(r'CurPage=(\d*)?','CurPage=25',test.decode())
