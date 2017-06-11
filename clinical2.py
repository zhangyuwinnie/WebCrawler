# coding: utf-8
import re

import xlwt
from lxml import etree
import requests
from bs4 import BeautifulSoup

workbook = xlwt.Workbook()
sheet1 = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
urlList = []
titleList = []
statusList = []
conditionList = []
interventionList = []
row = [0]


def getUrl(url, params):
    result = requests.get(url=url, params=params)
    html = result.text
    # print (html)
    root = etree.HTML(html)
    # print (root) 
    href = root.xpath('//td[@style="padding-left:1em; padding-top:2ex"]/a/@href')
    
    status = root.xpath('//td[@style="padding-top:2ex ; text-align:center"]/span[1]/text()')
    title = root.xpath('//td[@style="padding-left:1em; padding-top:2ex"]/a/@title')
    condition = root.xpath('//table[@class="data_table body3"]//tr[1]//td/text()')
    intervention = root.xpath('//table[@class="data_table body3"]//tr[2]//td/text()')
    
    #print (len(href), href) 
    #print (len(status), status) 
    #print (len(title), title)
    #print (len(condition), condition)
    #print (len(intervention), intervention)
    
    index = 0
    for i in range(len(href)):
        index += 1
        # print (index)
        urlList.append(href[i])
        titleList.append(title[i])
        statusList.append(status[i])
        conditionList.append(condition[i])
        interventionList.append(intervention[i])

def getDetail(url):
    result = requests.get(url=url)
    html = result.text
    # print(html)
    soup = BeautifulSoup(html)
    table = soup.table
    # print (table)
    block = table.find_all('tr')

    # print (item[1].get_text())
    
    col = 4
    # print (row[0])
    for i in range(5):
        content = block[i].get_text().split("\n")
        if len(content) > 3:
            sheet1.write(row[0], col, block[i].get_text())
            col = col + 1
    row[0] = row[0] + 1


if __name__ == '__main__':
    getUrl('https://clinicaltrials.gov/ct2/results',
       {'term': 'cancer','currentpage': '1', 'pagesize': '20'})
    for i in range(len(urlList)):
        print (i)
        url = 'https://clinicaltrials.gov/ct2/show/record' + urlList[i][9:]
        sheet1.write(i, 0, titleList[i])
        sheet1.write(i, 1, statusList[i])
        sheet1.write(i, 2, conditionList[i])
        sheet1.write(i, 3, interventionList[i])
        
        getDetail(url)
        workbook.save('/Users/zy/Desktop/webCrawler/临床研究数据抓取——clinicaltrial.xls')
    # url = 'https://clinicaltrials.gov/ct2/show/record/NCT02890667?term=cancer&rank=2'
    # print (url)
 
    
