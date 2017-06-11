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
    # print (len(node_List), node_List) 
    index = 0
    for node in node_List:
        index += 1
        print (index)
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
    print (row[0])
    for i in range(5):
        content = block[i].get_text().split("\n")
        if len(content) > 3:
            sheet1.write(row[0], col, block[i].get_text())
            col = col + 1
    row[0] = row[0] + 1
        
        


if __name__ == '__main__':
    getUrl('https://clinicaltrials.gov/ct2/results',
       {'term': 'cancer','currentpage': '1', 'pagesize': '5'})
    for i in range(len(urlList)):
        url = 'https://clinicaltrials.gov/ct2/show/record' + urlList[i][9:]
        getDetail(url)
        workbook.save('/Users/zy/Desktop/广州昕康/临床研究数据抓取——clinicaltrial.xls')
    # url = 'https://clinicaltrials.gov/ct2/show/record/NCT02890667?term=cancer&rank=2'
    # print (url)
 
    
