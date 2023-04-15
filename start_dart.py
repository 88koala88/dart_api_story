### 필요한 모듈
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import pandas as pd

from time import sleep
import requests
import json
import os


from datetime import datetime

api_key = "801b9fc87e380dfc40a19a593d6fd762bc681388"

corp_info_stock_code = pd.read_csv("corp_info_stock_code.csv", dtype = {'corp_code':str, 'stock_code':str})

bsns_year_list = ['2022']
reprt_code_list = ['11011','11012','11013','11015']
fs_div_val_list = ['CFS']

bsns_year_val = '2022'
fs_div_val = 'CFS'

if not os.path.exists(f'fnlttSinglAcntAll'):
    os.makedirs('fnlttSinglAcntAll')
    
# total = pd.DataFrame()
for corp_code_val in corp_info_stock_code['corp_code']:  # corp code
    for reprt_code_val in reprt_code_list: # reprt code (11011, 11012, 11013, 11014)
        print(f'{corp_code_val}_{bsns_year_val}_{reprt_code_val}_{fs_div_val}')
        
        url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?'
        params = f'crtfc_key={api_key}&corp_code={corp_code_val}&bsns_year={bsns_year_val}&reprt_code={reprt_code_val}&fs_div={fs_div_val}'
    
        try:
    
            api_url = url + params
   
            r = requests.get(api_url)
            r_json = r.json()
            sleep(0.7)
            
            df = pd.DataFrame([r_json][0]['list'])
            
            df.to_csv(f'fnlttSinglAcntAll/{corp_code_val}_{bsns_year_val}_{reprt_code_val}_{fs_div_val}.csv', index = False)
            
            # log
            now = datetime.now()
            log_df = pd.DataFrame({
                'corp_code':corp_code_val,
                'bsns_year':bsns_year_val,
                'reprt_code':reprt_code_val,
                'fs_div':fs_div_val,
                'time': now.strftime('%Y-%m-%d %H:%M:%S'),
                'status':r_json['message']            
            },index = [0])
            
            if not os.path.exists(f'log_fnlttSinglAcntAll.csv'):
                log_df.to_csv(f'log_fnlttSinglAcntAll.csv', index = False, mode = 'w')
            else:
                log_df.to_csv(f'log_fnlttSinglAcntAll.csv', index = False, mode = 'a', header = False)    
            print('success')
            
         
        except:
            # log
            now = datetime.now()
            log_df = pd.DataFrame({
                'corp_code':corp_code_val,
                'bsns_year':bsns_year_val,
                'reprt_code':reprt_code_val,
                'fs_div':fs_div_val,
                'time': now.strftime('%Y-%m-%d %H:%M:%S'),
                'status':r_json['message']            
            },index = [0])
            
            if not os.path.exists(f'log_fnlttSinglAcntAll.csv'):
                log_df.to_csv(f'log_fnlttSinglAcntAll.csv', index = False, mode = 'w')
            else:
                log_df.to_csv(f'log_fnlttSinglAcntAll.csv', index = False, mode = 'a', header = False)   
            print('failed')
            
#     df = pd.DataFrame([r_json][0]['list'])    
#     total = pd.concat([total,df])