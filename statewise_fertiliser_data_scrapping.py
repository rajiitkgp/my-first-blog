from selenium import webdriver 

from selenium.webdriver.common.by import By 

from selenium.webdriver.support.ui import WebDriverWait 

from selenium.webdriver.support import expected_conditions as EC 

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import numpy as np
import pandas as pd
import time
import re


option = webdriver.ChromeOptions()
browser = webdriver.Chrome(executable_path='/home/farmguide/Downloads/chromedriver', chrome_options=option)
url = 'http://urvarak.co.in/'
browser.get(url)   #clicking of url using selenium

browser.switch_to_frame('fullfrm')
browser.find_element_by_xpath('//*[@id="trHome1"]/td/table/tbody/tr[1]/td/table/tbody/tr[3]/td[2]/a').click() #click into statewise data 
browser.switch_to_window(browser.window_handles[1])
browser.switch_to_default_content()
browser.switch_to_frame('fullfrm') #switch into main frame in the new window.
browser.implicitly_wait(30)

month=np.arange(1,13,1)
year=np.arange(1,13,1)

all_data = pd.DataFrame()
for y in year:
    x_path = '//*[@id="ddl_Year"]/option[{0}]'.format(y)
    browser.find_element_by_xpath(x_path).click() #finding x_path of year and clicking it.
    browser.implicitly_wait(6)
    yr=browser.find_element_by_xpath(x_path).text #text for year
    print(yr)
    for m in month:
        x_path = '//*[@id="ddl_Month"]/option[{0}]'.format(m) 
        browser.find_element_by_xpath(x_path).click() #findig x_path of month and another clicking 
        mnth=browser.find_element_by_xpath(x_path).text 
        print(mnth)
        browser.implicitly_wait(5)
        browser.find_element_by_xpath('//*[@id="goBtn"]').click() #final click on submit button for getting the data.
        time.sleep(23) #make browser wait until the data get loaded in the page.
        browser.switch_to_default_content() #switching to default content.
        browser.switch_to_frame('fullfrm')
        
        #steps for extracting data from the page
        soup= BeautifulSoup(browser.page_source,'lxml')
        right_table=soup.find('table',{"id":'Table4'})
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
        L=[]
        M=[]
        for match in right_table.findAll('tr'): #each tr contain one record
            cells=match.findAll('td')

            if len(cells)==10:
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
                L.append(yr)
                M.append(mnth)  #getting all data(columns) of each record along with month and year
            else:
                break
                
        DF = pd.DataFrame()
        DF['Year']=L
        DF['Month']=M
        DF['State']=A
        DF['FG']=B
        DF['Requirement']=C
        DF['Opening Stock']=D
        DF['Monthly Plan']=E
        DF['Dispatches']=F
        DF['Net Receipts']=G
        DF['Availability']=H
        DF['Sales']=I
        DF['Closing Stock']=J
        all_data = all_data.append(DF,ignore_index=True)
        
browser.quit()

