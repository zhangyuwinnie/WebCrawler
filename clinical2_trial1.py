# -*- coding: utf-8 -*-
# 修改clinical，通过detail list的index取title，status等，但index条目之间不一致

# coding: utf-8
import re

import xlwt
from lxml import etree
import requests
from bs4 import BeautifulSoup

workbook = xlwt.Workbook()
sheet1 = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
urlList = []
row = [0]


def getUrl(url, params):
    result = requests.get(url=url, params=params)
    html = result.text
    # print (html)
    root = etree.HTML(html)
    # print (root) 
    node_List = root.xpath('//td[@style="padding-left:1em; padding-top:2ex"]/a/@href')
    
    #status = root.xpath('//span[@style="color:  green  "]/text()')
    #title = root.xpath('//td[@style="padding-left:1em; padding-top:2ex"]/a/@title')
    # print (len(node_List), node_List) 
    index = 0
    for node in node_List:
        index += 1
        # print (index)
        urlList.append(node)

def getDetail(url):
    result = requests.get(url=url)
    html = result.text
    # print(html)
    soup = BeautifulSoup(html)
    table = soup.table
    # print (table)
    block = table.find_all('tr')

    # print (item[1].get_text())
    
    col = 0
    
    # title, condition, intervention,status, NCT,...
    print (len(block))
    select = [14,24, 25,31, 46, 40,41,52,53,54,55]
    for i in select:
        if i <= len(block) - 1:
            content = block[i].get_text().split("\n")
            # print (i,content)
            if len(content) > 3:
                sheet1.write(row[0], col, block[i].get_text())
                col = col + 1
        else:
            col = col + 1
    row[0] = row[0] + 1
        
        


if __name__ == '__main__':
    getUrl('https://clinicaltrials.gov/ct2/results',
       {'term': 'cancer','currentpage': '1', 'pagesize': '20'})
    for i in range(len(urlList)):
        url = 'https://clinicaltrials.gov/ct2/show/record' + urlList[i][9:]
        print (i)
        getDetail(url)
        workbook.save('/Users/zy/Desktop/webCrawler/临床研究数据抓取——clinicaltrial.xls')
    # url = 'https://clinicaltrials.gov/ct2/show/record/NCT02890667?term=cancer&rank=2'
    # print (url)
 
    
