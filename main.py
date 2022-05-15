# -*- coding: utf-8 -*-
"""
Created on Sat May  7 13:57:31 2022

@author: ACER


Cào dữ liệu danh sách khách sạn ở Đà Nẵng từ agoda và đổ vào DB
"Lấy tất cả thông tin hiển thị trên web
Đổ vào DB ở local host
Build API cho DB với cách endpoint sau:
- Endpoint nhận khoảng giá tiền và xuất ra danh sách khách sạn
- Endpoint nhận khoảng sao đánh giá và xuất ra  danh sách khách sạn"
"""
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import numpy as np
import pandas as pd
from pathlib import Path
from getIdHotel import *

result = getAll('https://www.agoda.com/vi-vn/search?city=16440')
filepath = Path(r'hotel_agoda.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(filepath,encoding='utf-8-sig',index=False) 