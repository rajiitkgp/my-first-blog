from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import pandas as pd
import time
import re

import glob
option = webdriver.ChromeOptions()
browser = webdriver.Chrome(executable_path='/home/farmguide/myproject/chromedriver', chrome_options=option)
url = 'https://data.gov.in/ogpl_apis?sort=desc&order=Updated&org_type=Central&sector=Select&org=Ministry%20of%20Agriculture%20and%20Farmers%20Welfare&org_l1=Department%20of%20Animal%20Husbandry%2C%20Dairying%20and%20Fisheries&org_l2=Select&page_size=120&ogpl_apis_title='
browser.get(url)
main_window = browser.current_window_handle  #getting url of site containing list of apis.


para=np.arange(1,21,1)
head=np.arange(1,4,1)

file2=[]
link2=[]

j=0
for h in head:
    print(h)
    for p in para:
        if p<21:
            x_path = '//*[@id="block-system-main"]/div/div[1]/div['
            x_path += str(h)
            x_path += ']/div['
            x_path +=str(p)
            x_path +=']/a'
            print(p)
            print(x_path) #finding xpath of particular api
            while(True):
                try:
                    browser.find_element_by_xpath(x_path).click() #clicking the api
                    print('y')
                    break
                except NoSuchElementException:
                    print('no element')
                    browser.close()
                    break
                except Exception:
                    time.sleep(10)
                    browser.switch_to.window(main_window)   #handling error caused due to page loading, or any other error
                    browser.get(url)
                    print('v')
                    continue
                
#             time.sleep(5)
            browser.switch_to_window(browser.window_handles[1])
            browser.switch_to_default_content()
            soup= BeautifulSoup(browser.page_source,'html.parser')
            time.sleep(5)

            xpath2='//*[contains(@id,"swagger-ui")]'
            c2=browser.find_element_by_xpath(Xpath).text
            H=re.findall('"([^"]*)"', c2)[0]
            file2.append(H)  #finding xpath of header name of api 


            Xpath="//*[contains(@id,'operations-Resource')]"
            w=browser.find_element_by_xpath(Xpath)
            t=w.text.split('\n')[1]
            Z='https://data.gov.in'
            c=Z+t    #finding xpath of a text which on adding with http://data.gov.in ... will give a link


            client=uReq(c)
            page=client.read()
            client.close()
            soup1= BeautifulSoup(page, "html.parser")
            a=soup1.script.string
            d=re.findall('"([^"]*)"', a) 
            link2.append(d[0]) # we took the link which is created above and used that link to extract an another api link, which contains required data in csv or xml format.



            browser.close()
            browser.switch_to.window(main_window)
            
        else:
            break

df=pd.DataFrame()
df['link']=link2
df['file']=file2
df.to_csv('apilink.csv',index=False) # storing name of api and api link into dataframe

all_data = pd.DataFrame()
for f in glob.glob('apilink*.csv'):
        DFF = pd.read_csv(f)
        print(DFF.shape[0])
        
        all_data = all_data.append(DFF,ignore_index=True) #all df containing api link and name is merged into single dataframe
        

all_data["is_duplicate"]= all_data.duplicated()
dup=all_data[all_data['is_duplicate']==True].index.tolist()
for i in dup:
    all_data.drop(i,inplace=True) #deleting duplicate row from the dataframe.


p=[]
for i in all_data['file']:
    p.append(re.findall('[\d-]+', i))
c=[]
for i in p:
    c.append(' '.join(str(v) for v in i))
d=[]
for i in c:
    b=i.lstrip("-")
    e=b.lstrip(' ')
    g=e.rstrip('-')
    d.append(g)  #used name of apis to extract year

all_data['year']=d #column of year is added to df
all_data.reset_index(drop=True,inplace=True)
all_data.drop('is_duplicate',axis=1,inplace=True)
all_data.to_csv('Apilink.csv',index=False) # dataframe containing api link, name of api, year.