# coding: utf-8
import re

import xlwt
from lxml import etree
import requests
from bs4 import BeautifulSoup

workbook = xlwt.Workbook()
sheet1 = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
row = [0]


def getUrl(url, params):
    urlList = []
    # titleList = []
    statusList = []
    conditionList = []
    result = requests.get(url=url, params=params)
    html = result.text
    # print (html)
    root = etree.HTML(html)
    # print (root) 
    
    href = root.xpath('//td[@style="padding-left:1em; padding-top:2ex"]/a/@href')
    color = root.xpath('//td[@style="padding-top:2ex ; text-align:center"]/span[1]/@style')
    #print (len(href), len(color))
    
    status = root.xpath('//td[@style="padding-top:2ex ; text-align:center"]/span[1]/text()')
    # title = root.xpath('//td[@style="padding-left:1em; padding-top:2ex"]/a/@title')
    condition = root.xpath('//table[@class="data_table body3"]//tr[1]//td/text()')
    
    #print (len(href), href) 
    #print (len(status), status) 
    #print (len(title), title)
    #print (len(condition), condition)
    #print (len(intervention), intervention)
    
    index = 0
    for i in range(len(href)):
        index += 1      
        if "green" in color[i]: 
            # print (index)
            urlList.append(href[i])
            # titleList.append(title[i])
            statusList.append(status[i])
            conditionList.append(condition[i])
    return [urlList, statusList, conditionList]
    
def getDetail(url):
    result = requests.get(url=url)
    html = result.text
    # print(html)
    root = etree.HTML(html)
    soup = BeautifulSoup(html)
    
    tables = soup.findAll("table")
    # type, design, official title
    studyInfo = tables[1]
    tds1 = studyInfo.select('tr td')
    officialTitle = tds1[5].get_text()
    stype = tds1[1].get_text()
    design = tds1[3].get_text()
    #print (stype, design,officialTitle)
    col = 2
    sheet1.write(row[0], col, officialTitle)
    col+=1
    sheet1.write(row[0], col, stype)
    col+=1
    sheet1.write(row[0], col, design)
    col+=1

    # purpose
    purpose = root.xpath('//div[@id="main-content"]/div[@class = "indent1" and @style = "margin-top:3ex"]/div[@class = "indent2" and @style = "margin-top:2ex"]/div[@class = "body3"]')
    purposeInfo = purpose[0].xpath('string(.)').strip()
    #print (purposeInfo)
    sheet1.write(row[0], col, purposeInfo)
    col+=1
    
    # sponsor
    sponsor = root.xpath('//div[@class = "info-text" and @id = "sponsor"]')
    sponsorInfo = sponsor[0].xpath('string(.)').strip()
    #print (sponsorInfo)
    sheet1.write(row[0], col, sponsorInfo)
    col+=1
    
    # primary outcome, secondary outcome
    # primaryOut = root.xpath('//div[@class="body3"]//ul[@style="margin-top:1ex; margin-bottom:1ex;"]//li/text()')[0]
    # primaryOutfirst = root.xpath('//div[contains(text(),"Primary Outcome")]//ul//li/text()')
    # primaryOutsecond = root.xpath('//div[contains(text(),"Primary Outcome")]//div/text()')
    # print (primaryOutfirst)
    primary = root.xpath('//div[@id="main-content"]/div[@class = "indent1" and @style = "margin-top:3ex"]/div[@class ="indent2" and @style = "margin-top:2ex"]/div[@class = "indent3"]/div[contains(text(),"Primary")]')
    primaryInfo = primary[0].xpath('string(.)').strip()
    #print (primaryInfo)
    sheet1.write(row[0], col, primaryInfo)
    col+=1
    
    secondary = root.xpath('//div[@id="main-content"]/div[@class = "indent1" and @style = "margin-top:3ex"]/div[@class ="indent2" and @style = "margin-top:2ex"]/div[@class = "indent3"]/div[contains(text(),"Secondary")]')
    if len(secondary) > 0:
        secondaryInfo = secondary[0].xpath('string(.)').strip()
        sheet1.write(row[0], col, secondaryInfo)
        #secondInfo = measures[1].xpath('string(.)').encode('utf-8').strip()
        #print (secondaryInfo)
    col+=1
    
    # enrollment, start date, end date
    enrollInfo = tables[2]
    tds2 = enrollInfo.select('tr td')
    enrollment = tds2[1].get_text()
    startDate = tds2[3].get_text()
    endDate = tds2[5].get_text()
    #print (enrollment, startDate, endDate)
    sheet1.write(row[0], col, enrollment)
    col+=1
    sheet1.write(row[0], col, startDate)
    col+=1
    sheet1.write(row[0], col, endDate)
    col+=1
    
    # eligibility & criteria
    criteria = root.xpath('//div[@id="main-content"]/div[@class = "indent1" and @style="margin-top:3ex; border:1px solid white"]')
    # info = criteria[0].xpath('descendant-or-self::text()').extract() 
    criteriaInfo = criteria[0].xpath('string(.)').strip()
    #print (criteriaInfo)
    sheet1.write(row[0], col, criteriaInfo)
    col+=1
    
    # contact
    contact = root.xpath('//table[@summary = "Layout table for location contacts"]')
    if len(contact) > 0:
        contactInfo = contact[0].xpath('string(.)').strip()
        #print (contactInfo)
        sheet1.write(row[0], col, contactInfo)
    col+=1
    
    # investigator
    investigator = root.xpath('//table[@summary = "Layout table for investigator information"]')
    if len(investigator) > 0:
        investigatorInfo = investigator[0].xpath('string(.)').strip()
        #print (investigatorInfo)
        sheet1.write(row[0], col, investigatorInfo)
    col+=1
    
    # Identifier
    nct = root.xpath('//table[@summary = "Layout table for additional information"]//tr[2]//td[2]/a[1]/text()')
    #print (nct)
    sheet1.write(row[0], col, nct)
    col+=1
    row[0] = row[0] + 1


if __name__ == '__main__':
    for pg in range(10):
        results = getUrl('https://clinicaltrials.gov/ct2/results',
        {'term': 'cancer','pg': pg+1})
        # print (results)
        for i in range(len(results[0])):
            print (pg,i)
            url = 'https://clinicaltrials.gov/ct2/show/study' + results[0][i][9:]
            print(url)
            # sheet1.write(i, 0, titleList[i])
            sheet1.write(row[0], 0, results[1][i])
            sheet1.write(row[0], 1, results[2][i])            
            getDetail(url)      
        # url = 'https://clinicaltrials.gov/ct2/show/record/NCT02890667?term=cancer&rank=2'
        # print (url)
        workbook.save('/Users/zy/Desktop/webCrawler/临床研究数据抓取——clinicaltrial.xls')
 
    
