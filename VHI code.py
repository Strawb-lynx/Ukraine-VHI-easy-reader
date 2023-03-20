import urllib.request
import pandas as pd
from datetime import datetime
from fuzzywuzzy import fuzz
df_list=[]

city_dict_2 = {
    24: 1,
    16: 13,
    25: 2,
    17: 14,
    5: 3,
    18: 15,
    6: 4,
    19: 16,
    20:25,
    27: 5,
    21: 17,
    23: 6,
    22: 18,
    26: 7,
    8: 19,
    7: 8,
    9: 20,
    11: 9,
    12:9.1,
    10: 21,
    13: 10,
    1: 22,
    14: 11,
    3: 23,
    15: 12,
    2: 24,
    4: 25
}
city_dict = {
    'Vinnytsia': 1,
    'Mykolaivska': 13,
    'Volynska': 2,
    'Odesa': 14,
    'Dnipropetrovsk': 3,
    'Poltava': 15,
    'Donetska': 4,
    'Rivenska': 16,
    'Zhytomyrska': 5,
    'Sumy': 17,
    'Zakarpatska': 6,
    'Ternopil': 18,
    'Zaporizhia': 7,
    'Kharkiv': 19,
    'Ivano-Frankivsk': 8,
    'Kherson': 20,
    'Kyivska': 9,
    'Khmelnytska': 21,
    'Kirovohradska': 10,
    'Cherkasska': 22,
    'Luhansk': 11,
    'Chernivtsi': 23,
    'Lvivska': 12,
    'Chernihivska': 24,
    'Republic of Crimea': 25
}
print("Download data from NOAA site again? y/n")
respose=input()
if respose=="y":
    for i in range (1,28):
        url=f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1=1981&year2=2023&type=Mean'
        text=urllib.request.urlopen(url).read()
        text=text.replace(b'<tt><pre>',b'')
        text=text.replace(b'</pre></tt>',b'')
        #######яку область обрати#######
        first_400_bytes = text[:400]
        scores = {}
        for city in city_dict.keys():
            score = fuzz.ratio(first_400_bytes, bytes(repr(city).encode('utf-8')))
            scores[city] = score
        max_score = max(scores.values())
        best_match = [k for k, v in scores.items() if v == max_score][0]
        print(f"(old method) possible best match: {best_match} ({city_dict[best_match]})")
        ###############
        now = datetime.now()
        date_and_time_time = now.strftime("%d%m%Y%H%M%S")
        filename='NOAA_ID'+str(i)+'_'+date_and_time_time+'.csv'
        with open(filename,'wb') as out:
            out.write(text)
            out.close
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
        df=pd.read_csv(filename,header=1,names=headers)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df = df.drop('empty', axis=1)
        df['old area'] = i
        df['new generated']=city_dict[best_match]
        df['new alligned']=city_dict_2[i]
        df_list.append(df)
    merged_df = pd.concat(df_list, axis=0, ignore_index=True)
    merged_df.to_csv("merged_file.csv", index=False)
else:
    file_path = "D:\\uni year 2\\aks labi\laba 1\\merged_file.csv"
    merged_df = pd.read_csv(file_path)
# print(merged_df.head())
# print(merged_df.tail())
print("what region to check? from 1 to 26")
region=int(input())
print("what year? possible data is from 1982 to 2023")
year=int(input())
vhi_data = merged_df[(merged_df['new alligned'] == region) & (merged_df["Year"] == year)][["VHI",'Week']]
print(vhi_data)
print("Minimum VHI value:", vhi_data.min()[0],"week:",vhi_data[(vhi_data["VHI"]==vhi_data.min()[0])]['Week'].values[0])
print("Maximum VHI value:", vhi_data.max()[0],"week:",vhi_data[(vhi_data["VHI"]==vhi_data.max()[0])]['Week'].values[0])
vhi_data_2 = merged_df[(merged_df['new alligned'] == region) & (merged_df["VHI"] <= 15)][["VHI",'Year']]["Year"].unique()
print ("years with severe drought (less 15%): ", vhi_data_2)
vhi_data_3 = merged_df[(merged_df['new alligned'] == region) & (merged_df["VHI"] <= 35)][["VHI",'Year']]["Year"].unique()
print ("years with moderate drought (less 35%): ", vhi_data_3)
