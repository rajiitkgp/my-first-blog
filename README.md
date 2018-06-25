project name- google_weather_data.py

It contains automation code for google weather data. which includes code for following steps
1.Dowloading of ghcnd_all file from url into downloads folder.
2.unzipping ghcnd_all file in the downloads folder.
3.Taking out all the .dly file starts with IN or INM from ghcnd_all which was unzipped in second step and converted them in a csv format and save into newcsv folder.
4.Taken all the file from newcsv folder and preprocessed them in a good csv format and save into newcsv2 folder.
5.finally, All files from newcsv2 folder is transferred into mysql database.