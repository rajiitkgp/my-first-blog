# Description of projects

## A.google_weather_data.py

### It contains automation code for preprocessing of GLOBAL HISTORICAL CLIMATOLOGY NETWORK data downloaded from google. The Global Historical Climatology Network (GHCN) is an integrated database of climate summaries from land surface stations across the globe that have been subjected to a common suite of quality assurance reviews.<br/>

it includes code for following steps <br/>

1.Dowloading of ghcnd_all.tar.gz(it contains".dly" files for all of GHCN-Daily) file from google link into downloads folder. <br/>

2.unzipping ghcnd_all.tar.gz file in the downloads folder. <br/>

3.Taking out all the .dly file (Each ".dly" file contains data for one station and Each record in a file contains one month of daily data) starts with IN or INM from ghcnd_all which was unzipped in second step and converted them in a csv format and save into a folder named newcsv. <br/>

4.Taken all the file from newcsv folder and preprocessed them in a good csv format and save into another folder newcsv2. <br/>

5.finally, All files from newcsv2 is merged into a single file and transferred into mysql database <br/>


## B.statewise_fertiliser_data_scrapping.py <br/>

### This file contains code for scrapping of statewise fertiliser data from urvarak.com. It contains explanation of each step involved in the code.<br/>

1.In first step we took the url to be scrapped and clicked on the name statewise by using xpath of name statewise. Then we moved into second window which opened after clicking. <br/> 

2.In the new window opened, we clicked on the each month and each year and submit button in a loop. Each time after submitting we get report of fertiliser data. <br/>

3.Finally after getting the report we scrapped the data from the page using beautiful soup and saved it to dataframe. <br/>


## C.Companywise_fertiliser_data_scrapping.py </br>

It contains same steps as mentioned in the satewise_fertiliser_data_scrapping.py <br/>


## D.Structuring_nested_json_into_csv.py <br/>

### In this project we extracted important information of all market from mandi profile data and structured into a good csv format. <br/>

1.we took out area_info, admin info, general_info, state-market info, commodities_info for each market and made separate dataframe for each type of info.<br/>

2.we combined area_info, admin_info, general_info and state_market info into a single dataframe. Since each market have more than one or none commodities info, so we duplicated each record or rows in the dataframe according to number of commodities came into each market.<br/>

3.Finally, we combined above dataframe with dataframe containing commodities info to a single required dataframe.<br/>


## E. Merging_excelfile.py</br>

### This file contains code for extracting all useful information from excels file and strcuturing it to a good format and then merging them all into a single file.<br/>

1.we took each file by iteration and extracted state, district, subdistrict, village from there and made a separate column for each in the table.<br/>

2.Deleted all columns with na values and all unnecessary rows with non-required info.<br/>

3.Modified each column names,then merged all the files in a single one and transferred each file into mysql database simultaneously.<br/>


## F.Scrapping_of_apis.py <br/>

### In this project we scrapped api link from data.gov website. Each api link contains data of different types, for instance data for Current Daily Price of Various Commodities from Various Markets (Mandi), Farmers Queries in Kisan Call Centre (KCC) from KURNOOL district of ANDHRA PRADESH for the month of April 2018 etc. in csv or xml format.<br/>

1.At first we clicked on name of each api in a loop and moved to new window opened.<br/>

2.we extracted some text from there and combined this text with http://data.gov.in/ to get a link. <br/>

3.we parsed that link using beautiful soup and extracted an api link from there which contains data in csv or xml format.<br/>

4.Finally, we created a dataFrame containing name of each api, api link and year duration taken from the name of api. <br/>


