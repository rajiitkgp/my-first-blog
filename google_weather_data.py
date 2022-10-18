

# df=pd.read_csv('ghcnd-inventory.txt',delim_whitespace=True, header = None,names=("ID","LATITUDE","LONGITUDE","ELEMENT","FIRSTYEAR","LASTYEAR"))
# #sep='\s+' will work in place of delim_whitespace=true
# df1=df[df['ID'].str.startswith("IN")]
# l1=df1['ID'].unique()

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from zipfile import BadZipfile
from sqlalchemy import create_engine
from pandas.io import sql
import pymysql
import string,re
import xlrd
import  pandas as pd
import numpy as np
import glob
import tarfile


option = webdriver.ChromeOptions()
browser = webdriver.Chrome(executable_path='/home/farmguide/myproject/chromedriver', chrome_options=option)
url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd_all.tar.gz'
browser.get(url)
#will download ghcnd_all.tar.gz from url

with tarfile.open('/home/farmguide/Downloads/ghcnd_all.tar.gz') as tar:
    def is_within_directory(directory, target):
        
        abs_directory = os.path.abspath(directory)
        abs_target = os.path.abspath(target)
    
        prefix = os.path.commonprefix([abs_directory, abs_target])
        
        return prefix == abs_directory
    
    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    
        for member in tar.getmembers():
            member_path = os.path.join(path, member.name)
            if not is_within_directory(path, member_path):
                raise Exception("Attempted Path Traversal in Tar File")
    
        tar.extractall(path, members, numeric_owner=numeric_owner) 
        
    
    safe_extract(tar)
#will unzipp the file

print('unzipped')
p=0
for f in glob.glob('/home/farmguide/Downloads/ghcnd_all/IN*.dly'): #it will take out.dly file starting with IN or INM
    a=f.rsplit('/', 1)[-1]
    b=a.rsplit('.')[0] 

    df=pd.read_csv(f,header=None)
    df['ID']=df[0].apply(lambda x:x[0:11])
    df['YEAR']=df[0].apply(lambda x:x[11:15])
    df['MONTH']=df[0].apply(lambda x:x[15:17])
    df['ELEMENT']=df[0].apply(lambda x:x[17:21])   #extraction of id, year, value, MFLAG etc. data from .dly file
    list1 =np.arange(22,270,8)
    for idx,i in enumerate(list1):
        VALUE = 'VALUE{}'.format(idx+1)
        MFLAG = 'MFLAG{}'.format(idx+1)
        QFLAG = 'QFLAG{}'.format(idx+1)
        SFLAG = 'SFLAG{}'.format(idx+1)
        df[VALUE]=df[0].apply(lambda x:x[i-1:i+4])
        df[MFLAG]=df[0].apply(lambda x:x[i+4:i+5])
        df[QFLAG]=df[0].apply(lambda x:x[i+6:i+7])
        df[SFLAG]=df[0].apply(lambda x:x[i+7:i+8])
    path1=('/home/farmguide/Downloads/newcsv/{}.csv'.format(b))  #saving csv format of data extracted from .dly file into different folder newcsv
    df.to_csv(path1)



for f in glob.glob('/home/farmguide/Downloads/newcsv/IN*.csv'): #taking out each csv from newcsv and preporess into good format.
    df7 = pd.read_csv(f)    
    a=f.rsplit('/', 1)[-1]
    b=a.rsplit('.')[0] 
    df7['date']=(df7.YEAR).map(str)+'-'+(df7.MONTH).map(str)
    df7['date1']=pd.to_datetime(df7['date'])
    df7['days_in_month'] = df7['date1'].dt.daysinmonth #addition of column with number of days in a month.
    del df7['date']
    del df7['date1']

    cols = [c for c in df7.columns if str(c)[1:5] == 'FLAG'] #deletion of column containing name flag
    df7.drop(df7[cols],axis=1,inplace=True)

    df7.drop(['0','Unnamed: 0'],axis=1,inplace=True)

    df4 = pd.melt(df7[df7.ELEMENT=='PRCP'], id_vars=['ID', 'YEAR', 'MONTH','ELEMENT','days_in_month'], 
                      var_name="Day", value_name="Precip_10thOfMM")
    df5 = pd.melt(df7[df7.ELEMENT=='TMAX'], id_vars=['ID', 'YEAR', 'MONTH','ELEMENT','days_in_month'], 
                      var_name="Day", value_name="TMAX")
    df6 = pd.melt(df7[df7.ELEMENT=='TMIN'], id_vars=['ID', 'YEAR', 'MONTH','ELEMENT','days_in_month'], 
                      var_name="Day", value_name="TMIN")
    df8 = pd.melt(df7[df7.ELEMENT=='TAVG'], id_vars=['ID', 'YEAR', 'MONTH','ELEMENT','days_in_month'], # 4 different dataframe with a new column containing Precip_10thOfMM,tmax,tmin tavg of each day
                      var_name="Day", value_name="TAVG")
    df9=pd.merge(df4, df5, on=['ID', 'YEAR', 'MONTH','days_in_month', 'Day'],how='outer')
    df9=pd.merge(df9, df6, on=['ID', 'YEAR', 'MONTH','days_in_month', 'Day'],how='outer')
    df9=pd.merge(df9, df8, on=['ID', 'YEAR', 'MONTH','days_in_month', 'Day'],how='outer') #merging all new dataframe into single one
    df9.drop(df9.columns[[3,7]], axis=1,inplace=True)
    df9['Day']=df9['Day'].str.replace('[^0-9]', '')
    df9=df9.sort_values(['YEAR','MONTH','Day'], ascending=[True,True,True])
    df9.TMAX.replace(np.NaN, -8888, inplace=True)
    df9.Precip_10thOfMM.replace(np.NaN, -8888, inplace=True)
    df9.TMIN.replace(np.NaN, -8888, inplace=True)
    df9.TAVG.replace(np.NaN, -8888, inplace=True) #replacing nan values in each newly created column
    df9.columns = ['Station_ID', 'YEAR', 'MONTH', 'days_in_month', 'Day', 'Precip_10thOfMM','TMAX_10thOfC', 'TMIN_10thOfC', 'TAVG_10thOfC']
    df9['date']=(df9.YEAR).map(str)+'-'+(df9.MONTH).map(str)+'-'+(df9.Day).map(str)
    df9['date']=pd.to_datetime(df9['date'], errors='coerce') # addition of date column
    df9['YEAR']=df9['YEAR'].apply(int)
    df9['MONTH']=df9['MONTH'].apply(int)
    df9['Day']=df9['Day'].apply(int) #converting day,year, month in int type

    df9.head()
#     df9.drop(df9.tail(10).index,inplace=True) 
    path1=('/home/farmguide/Downloads/newcsv2/{}.csv'.format(b)) #saving preprocessed csv into new folder
    df9.to_csv(path1,index=False)
    
get_ipython().run_line_magic('time', "print('step2')")


all_data=pd.DataFrame()
p=0
for f in glob.glob('/home/farmguide/Downloads/newcsv2/IN*.csv'):
    DF= pd.read_csv(f)
    DF=DF[DF['YEAR']>2017] #adding those data in which year is greater than 2017
    all_data=all_data.append(DF,ignore_index=True)   #merging of each csv file into a single file
    p=p+1
    print(p)
all_data.to_csv('/home/farmguide/Downloads/merged_station.csv',index=False)

    
def clean_df_db_dups(DF, tablename, engine, dup_cols=[]): #function for adding data into mysql database.
  
    
    DF.drop_duplicates(dup_cols, keep='last', inplace=True)
    
    new = pd.read_sql_query("SELECT Station_ID,YEAR,MONTH,Day FROM TESTING", engine) 
    # it will take these four column from mysql table for checking whether database contains upcoming data or not.

    DF = pd.merge(DF, new, how='left', on=dup_cols, indicator=True)
    DF = DF[DF['_merge'] == 'left_only']
    DF.drop(['_merge'], axis=1, inplace=True)
    return DF # will return those rows from the file which is not present in the database


for f in glob.glob('/home/farmguide/Downloads/newcsv2/IN*.csv'):
    DF= pd.read_csv(f) #will take file to add into database
    engine= create_engine('mysql://root:farmguide@localhost:3306/testdb?charset=utf8mb4')
    get_ipython().run_line_magic('time', "DF = clean_df_db_dups(DF, 'TESTING', engine, dup_cols=['Station_ID','YEAR','MONTH','Day'])")
    print('step4')
    DF[DF.columns].to_sql('TESTING', engine, if_exists='append', index=False) #adding only new rows or data into database
    p=p+1
    print(p)
    

