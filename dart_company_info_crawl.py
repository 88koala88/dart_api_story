### 필요한 모듈
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import pandas as pd

from time import sleep
import requests
import json
from datetime import datetime

api_key = "801b9fc87e380dfc40a19a593d6fd762bc681388"

corp_info_stock_code = pd.read_csv("corp_info_stock_code.csv", dtype = {'corp_code':str, 'stock_code':str})

total = pd.DataFrame()
# for corp_code_val in test_for['corp_code']: # last 10 
for corp_code_val in corp_info_stock_code['corp_code']:  # total
    url = 'https://opendart.fss.or.kr/api/company.json?'
    params = f'crtfc_key={api_key}&corp_code={corp_code_val}'
    
    api_url = url + params    
    
    r = requests.get(api_url)
    r_json = r.json()
    df = pd.DataFrame(r_json, index  = [0])
    total = pd.concat([total, df])
    
    sleep(1)
    
    # log
    now = datetime.now()
    
    log_df = pd.DataFrame({
        'corp_code': corp_code_val,
        'time': now.strftime('%Y-%m-%d %H:%M:%S')
            }, index = [0])
    
    log_df.to_csv('log.csv', index = False, mode = 'a', header = False)
    
    # print(api_url)
    # print(corp_code_val)
    
total.to_csv('company_info.csv', index = False)