Description of projects

a.google_weather_data.py

It contains automation code for preprocessing of GLOBAL HISTORICAL CLIMATOLOGY NETWORK data downloaded from google. The Global Historical Climatology Network (GHCN) is an integrated database of climate summaries from land surface stations across the globe that have been subjected to a common suite of quality assurance reviews.<br/>

it includes code for following steps <br/>

1.Dowloading of ghcnd_all.tar.gz(it contains".dly" files for all of GHCN-Daily) file from google link into downloads folder. <br/>

2.unzipping ghcnd_all.tar.gz file in the downloads folder. <br/>

3.Taking out all the .dly file (Each ".dly" file contains data for one station and Each record in a file contains one month of daily data) starts with IN or INM from ghcnd_all which was unzipped in second step and converted them in a csv format and save into a folder named newcsv. <br/>

4.Taken all the file from newcsv folder and preprocessed them in a good csv format and save into another folder newcsv2. <br/>

5.finally, All files from newcsv2 is merged into a single file and transferred into mysql database <br/>