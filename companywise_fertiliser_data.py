from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import FirefoxOptions
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time,requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import time
import re

# similar to statewise data.    
browser.switch_to_frame('fullfrm')
browser.find_element_by_xpath('//*[@id="trHome1"]/td/table/tbody/tr[1]/td/table/tbody/tr[5]/td[2]/a').click()
browser.switch_to_window(browser.window_handles[1])
browser.switch_to_default_content()
browser.switch_to_frame('fullfrm')
browser.implicitly_wait(30)

month=np.arange(1,13,1)
year=np.arange(7,13,1)
i=0
j=0
all_data = pd.DataFrame()
for y in year:
    x_path = '//*[@id="ddl_Year"]/option[{0}]'.format(y)
    browser.find_element_by_xpath(x_path).click()
    browser.implicitly_wait(5)
    yr=browser.find_element_by_xpath(x_path).text
    print(yr)  
    for m in month2:
        x_path = '//*[@id="ddl_Month"]/option[{0}]'.format(m)
        browser.find_element_by_xpath(x_path).click()
        mnth=browser.find_element_by_xpath(x_path).text
        print(mnth)
        browser.implicitly_wait(3)
        browser.find_element_by_xpath('//*[@id="goBtn"]').click()
        time.sleep(15)

        browser.implicitly_wait(5)
        browser.switch_to_default_content()
        browser.switch_to_frame('fullfrm')
        soup= BeautifulSoup(browser.page_source,'lxml')
        right_table=soup.find('table',{"id":'pnlData'})

        A=[]
        B=[]
        C=[]
        D=[]
        E=[]
        F=[]
        G=[]
        H=[]
        I=[]
        J=[]
        K=[]
        L=[]
        M=[]
        for match in right_table.findAll('tr', id=re.compile("^rpt_AllData__ctl")):
            cells=match.findAll('td')

            if len(cells)==11:
                A.append(cells[0].findChildren(text=True)[-1])
                B.append(cells[1].findChildren(text=True)[-1])
                C.append(cells[2].findChildren(text=True)[-1])
                D.append(cells[3].findChildren(text=True)[-1])
                E.append(cells[4].findChildren(text=True)[-1])
                F.append(cells[5].findChildren(text=True)[-1])
                G.append(cells[6].findChildren(text=True)[-1])
                H.append(cells[7].findChildren(text=True)[-1])
                I.append(cells[8].findChildren(text=True)[-1])
                J.append(cells[9].findChildren(text=True)[-1])
                K.append(cells[10].findChildren(text=True)[-1])
                L.append(yr)
                M.append(mnth)
            else:
                break



        DF = pd.DataFrame()
        DF['Year']=L
        DF['Month']=M
        DF['FG']=A
        DF['State']=B
        DF['Company']=C
        DF['Requirement']=D
        DF['Opening Stock']=E
        DF['Monthly Plan']=F
        DF['Dispatches']=G
        DF['Net Receipts']=H
        DF['Availability']=I
        DF['Sales']=J
        DF['Closing Stock']=K
        all_data = all_data.append(DF,ignore_index=True)
all_data.to_csv('companywise_data.csv',index=False)

     
 #code for creating list of dataframes
# d = {}
# for name in companies:
#     d[name] = pd.DataFrame()
           