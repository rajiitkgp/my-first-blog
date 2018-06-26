import pandas as pd
import numpy as np
import json
mandi=json.loads(open('mandi_profile.json').read()) #getting json file from local

l=[]
for k in mandi['0']['area_info'].keys(): #taking out area info of each record from the file
    l.append(k.split(" ",1)[-1])
    
Area_info= pd.DataFrame(columns=l)
p=0
for q in mandi.keys():
    m=[]
    for r in mandi[q]['area_info'].values():
        m.append(r)
     
    Area_info.loc[p]=m  #saving area info in dataframe
    p=p+1

    
l=[]
for i in mandi['0']['general_info'].keys(): #taking out general info of each record or market
    l.append(i.split(" ",1)[-1])
General_info= pd.DataFrame(columns=l)

p=0
for q in mandi.keys():
    m=[]
    for r in mandi[q]['general_info'].values():
        m.append(r)
     
    General_info.loc[p]=m #saving general info of each record in the dataframe
    p=p+1
    
    
l=[]
for i in mandi['0']['admin_info'].keys():
    l.append(i.split(" ",1)[-1])
Admin_info= pd.DataFrame(columns=l)
p=0
for q in mandi.keys():
    m=[]
    for r in mandi[q]['admin_info'].values():
        m.append(r)
     
    Admin_info.loc[p]=m
    p=p+1
    
    
l=[]
for i in mandi['0']['connectivity_info'].keys():
    l.append(i.split(" ",1)[-1])
Connectivity_info= pd.DataFrame(columns=l)
p=0
for q in mandi.keys():
    m=[]
    for r in mandi[q]['connectivity_info'].values():
        m.append(r)
     
    Connectivity_info.loc[p]=m
    p=p+1
    
    
l=[]
j=0
for i in mandi['0'].keys(): #taking out common info state, village, market last updated, for each record or market
    if j<3:
        l.append(i)
    else:
        break
    j=j+1

info=pd.DataFrame(columns=l)
p=0
for q in mandi.keys():
    j=0
    m=[]
    for i in mandi[q].values():
        if j<3:
            m.append(i) 
           
        else:
            break
        j=j+1
    info.loc[p]=m #saving common info of each market into the dataframe info
    p=p+1
    


dfnew = pd.concat(
    [
        info,General_info,Admin_info,Connectivity_info  #concaneting each dataframe created above in a single dataframe
    ], axis=1
)
  
l=[]
for i in mandi['0']['commodities_info']['0'].keys(): #extracting all types of commoditites comming into each market 
    l.append(i)   

commodities_info=pd.DataFrame(columns=l)
p=0
for q in mandi.keys():
    
    for a in mandi[q]['commodities_info'].keys():
        m=[]
        for r in mandi[q]['commodities_info'][a].values():
            m.append(r)
        commodities_info.loc[p]=m  #saving commodities info into commodities_info dataframe.
        p=p+1   


        
col=[]
for i in  dfnew.columns:
    col.append(i)    
Repeat=pd.DataFrame(columns=col)
p=0
i=0
for q in mandi.keys():
    if len(mandi[q]['commodities_info'].keys())>0: 
        for a in mandi[q]['commodities_info'].keys():
            repeat.loc[p]=dfnew.loc[i] #repeating each record in the dfnew dataframe according to number of different types of commodities coming in each market
            p=p+1
        i=i+1
    else:
        repeat.loc[p]=dfnew.loc[i] #create another dataframe with repeating records.
        p=p+1
        i=i+1

mandi_Data = pd.concat(
    [
        Repeat,commodities_info  #Finally, concaneting data frame with general, admin , common info etc with dataframe containing commodities info
    ], axis=1
)
