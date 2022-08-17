import time
import traceback

import pandas as pd
import re
from seleniumwire import webdriver

browser = webdriver.Chrome()


class DetailGetter:
    def __init__(self):
        self.paper = pd.read_csv("./paper_all.csv", names=range(1, 15), header=None)
        self.start = 0  # The begining row
        self.browser = browser

    def parse(self, text):
        resultList = re.findall(r"FileName=(.*?)&DbName=(.*?)&DbCode=(.*?)&", text)
        return "https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=" + resultList[0][
            2] + "&dbname=" + resultList[0][1] + "&filename=" + resultList[0][0]

    def get_latest_row(self):
        if 10 in self.paper.columns or '10' in self.paper.columns:
            selector = 10
            auxiliary = 9
            for i in range(0, self.paper.__len__() + 1):
                if pd.isna(self.paper.loc[i, selector]) and not pd.isna(self.paper.loc[i, auxiliary]):
                    return i
            return self.paper.__len__()
        else:
            return 1

    def intercepter_helper(self):
        def interceptor(request):
            # 拦截.png,.jpg,.gif结尾的请求
            if request.path.endswith(('.png', '.jpg', '.gif')):
                request.abort()

        return interceptor

    def test(self):
        self.browser.request_interceptor = self.intercepter_helper()
        self.start = self.get_latest_row()
        try:
            for i in range(self.start, self.paper.__len__() + 1):
                if pd.isna(self.paper.loc[i, 9]):
                    continue
                print("This is the " + str(i) + "th item in paper_all.csv")
                browser.get(self.parse(self.paper.loc[i, 9]))
                authors = browser.find_elements("xpath", '//*[@id="authorpart"]/span')
                authors_str = ''
                for j in authors:
                    authors_str = authors_str + " " + j.text
                try:
                    self.keyWords = browser.find_element("xpath", '/html/body/div[2]/div[1]/div[3]/div/div/div[5]/p')
                except:
                    self.keyWords = "None"

                page = browser.page_source
                total = re.findall(r"专辑\S*?p>(.*?)</p>[\s\S]*专题\S*?p>(.*?)</p", page)
                self.album = total[0][0]
                self.topics = total[0][1]
                self.paper.loc[i, 10] = authors_str if authors_str.strip() != '' else "None"
                self.paper.loc[i, 11] = self.keyWords.text if type(self.keyWords) != type("") else "None"
                self.paper.loc[i, 12] = self.album
                self.paper.loc[i, 13] = self.topics
                time.sleep(4)
        except:
            traceback.print_exc()
            self.paper.to_csv('paper_all.csv', encoding='utf-8-sig', header=None)
        self.paper.to_csv('paper_all.csv', encoding='utf-8-sig', header=None, index=None)


detailGetter = DetailGetter()
detailGetter.test()
# import time
#
# import selenium
# import pandas as pd
# import re
# import traceback
# from selenium import webdriver
#
# browser = webdriver.Chrome()
#
# paper=pd.read_csv("./paper_all.csv",names=range(1,15),header=None)
#
# def parse(text):
#     resultList=re.findall(r"FileName=(.*?)&DbName=(.*?)&DbCode=(.*?)&",text)
#
#     return "https://kns.cnki.net/kcms/detail/detail.aspx?dbcode="+resultList[0][2]+"&dbname="+resultList[0][1]+"&filename="+resultList[0][0]
#
#
# def get_latest_row(df):
#     if 10 in df.columns or '10' in df.columns:
#         selector=10
#         auxiliary=9
#         for i in range(0,df.__len__()):
#