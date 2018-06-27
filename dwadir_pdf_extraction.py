
import xlrd
import  pandas as pd
import numpy as np

df= pd.read_excel('cleaned_xlsx.xlsx',header=None)
df.drop(df.index[0:134],inplace=True)
df.dropna(how="all", inplace=True) 
df[0].replace(np.nan,0,inplace=True)
df=df[pd.to_numeric(df[0], errors='coerce').notnull()]
df.reset_index(drop=True,inplace=True)
df.reset_index(inplace=True)
df[3].replace(np.nan,0,inplace=True)
df[4].replace(np.nan,0,inplace=True)
df[5].replace(np.nan,0,inplace=True)
df.insert(0,'state',np.nan)

for i in df[df[1].str.contains('NAME OF')==True].index.tolist():
    for j in (3,4,5):
        if df[j].iloc[i]!=0:
            df['state'].iloc[i+6]=df[j].iloc[i]

df.insert(1,'district',np.nan)
for i in df[(df[1].str.isupper()==True)&(df[1].str.contains('NAME OF')==False)].index.tolist():
    if df[0].iloc[i+1]==0:
        df['district'][i+3]=df[1].iloc[i]
    elif df[0].iloc[i+1]==1:
        df['district'][i+1]=df[1].iloc[i]


li=df[df[1].str.contains('NAME OF')==True].index.tolist()
for i in li:
    df.drop(i,inplace=True)

B=df[df[1].str.contains('Name of district')==True].index.tolist()
for i in B:
    df.drop(i,inplace=True)

D=df[df[2].str.contains('State')==True].index.tolist()
for i in D:
    df.drop(i,inplace=True)

d1=df[df[2].str.contains('of')==True].index.tolist()
for i in d1:
    df.drop(i,inplace=True)

f1=df[df[2].str.contains('regu')==True].index.tolist()
for i in f1:
    df.drop(i,inplace=True)

g1=df[df[2].str.contains('tion')==True].index.tolist()
for i in g1:
    df.drop(i,inplace=True)

H=df[df[1].str.isupper()==True].index.tolist()
for i in H:
    df.drop(i,inplace=True)

I=df[pd.to_numeric(df[1], errors='coerce').notnull()].index.tolist()
for i in I:
    df.drop(i,inplace=True)

df.reset_index(drop=True,inplace=True)
df.reset_index(inplace=True)
df.drop('level_0',axis=1,inplace=True)
dist=[]
dist=df[(df[1].str.isupper()==True)&(df[1].str.contains('NAME OF')==False)].index.tolist()
df.drop('index',axis=1,inplace=True)
df.insert(2,'wholesale market',np.nan)
df.insert(3,'State of regu-lation',np.nan)
df.insert(4,'Godown facilities',np.nan)
df.insert(5,'Cold storage facility',np.nan)
df.insert(6,'Nearest Railway Station',np.nan)
df.insert(7,'Distance(km)',np.nan)
df.insert(8,'Commodities arriving in the market',np.nan)
df.insert(9,'Tel. No.',np.nan)
df.insert(10,'Commercial grading facility',np.nan)
df.insert(11,'Complete postal address',np.nan)
df.reset_index(inplace=True)

ind=[]
ind=df1[df1['0']>0].index.tolist()
max(ind)
for i,j in enumerate(ind):
    if j<11427:
    M=ind[i+1]
    a=[]
    b=[]
    c=[]
    d=[]
    e=[]
    f=j
    for k in range(j,M,1):
        if (M-j)==1:
            a.append(df[10].iloc[k])
            b.append(df[8].iloc[k])
            c.append(df[7].iloc[k])
            d.append(df[5].iloc[k])
            e.append(df[3].iloc[k])
            break
        else:
            if type(df[10].iloc[k])==str:
                a.append(df[10].iloc[k])
            else:
                a.append(str(df[10].iloc[k]))
            if type(df[8].iloc[k])==str:
                b.append(df[8].iloc[k])
            else:
                b.append(str(df[8].iloc[k]))
            if type(df[7].iloc[k])==str:
                c.append(df[7].iloc[k])
            else:
                c.append(str(df[7].iloc[k]))
            if type(df[5].iloc[k])==str:
                d.append(df[5].iloc[k])
            else:
                d.append(str(df[5].iloc[k]))

    A= ' '.join(str(v) for v in a)
    B= ' '.join(str(v) for v in b)
    C= ' '.join(str(v) for v in c)
    D= ' '.join(str(v) for v in d)
    E= ' '.join(str(v) for v in e)                     
    df['Complete postal address'].iloc[f]=A
    df['Tel. No.'].iloc[f]=B
    df['Commodities arriving in the market'].iloc[f]=C
    df['Nearest Railway Station'].iloc[f]=D
    df['Godown facilities'].iloc[f]=E        
             
    else:
        break

for i,j in enumerate(ind):
    df['wholesale market'].iloc[j]=df[1].iloc[j]
    df['State of regu-lation'].iloc[j]=df[2].iloc[j]
    df['Cold storage facility'].iloc[j]=df[4].iloc[j]
    df['Distance(km)'].iloc[j]=df[6].iloc[j]
    df['Commercial grading facility'].iloc[j]=df[9].iloc[j]

df.to_csv('DWAPDF.csv',index=False)
df=pd.read_csv('DWAPDF.csv')
df.drop(df.columns[13:27],axis=1,inplace=True)
df.drop('index',axis=1,inplace=True)

df.dropna(how="all", inplace=True) 
df.to_csv('final.csv',index=False)
df=pd.read_csv('FFinal.csv')
df.dropna(how="all", inplace=True) 
b=df[df['district'].str.isupper()==True].index.tolist()
df['Godown facilities'] = df['Godown facilities'].astype(str).replace('0', '', regex=True)
df['Nearest Railway Station'] = df['Nearest Railway Station'].astype(str).replace('0', '', regex=True)
df['Tel. No.'] = df['Tel. No.'].astype(str).replace('nan', '', regex=True)
df['Commodities arriving in the market'] = df['Commodities arriving in the market'].astype(str).replace('nan', '', regex=True)
df['Complete postal address'] = df['Complete postal address'].astype(str).replace('nan', '', regex=True)
df.to_csv('FFinal.csv',index=False)

df['state']=df['state'].ffill()
df['district']=df['district'].ffill()

a=df[pd.to_numeric(df['wholesale market'], errors='coerce').notnull()].index.tolist()
for i in a:
    df.drop(i,inplace=True)

df.to_csv('dwadir_csv.csv',index=False)
aa=df2[df2['Godown facilities'].str.contains('do')==True].index.tolist()
for i in aa:
    df2['Godown facilities'].iloc[i]=np.nan

df2['Godown facilities']=df2['Godown facilities'].ffill()
j=0
for i in df.columns:
    j=j+1
    if j>5:
        a=df2[df2[i].str.contains('do')==True].index.tolist()
        for k in a:
            df2[i].iloc[k]=np.nan
        df2[i]=df2[i].ffill()

df2.to_csv('DWADIR_CSV.csv',index=False)
df2=pd.read_csv('dwadir_csv.csv')

