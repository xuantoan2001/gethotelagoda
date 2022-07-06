# -*- coding: utf-8 -*-
"""
Created on Tue May 10 09:56:07 2022

@author: ACER
"""

import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service

s = Service('E:/python/export_files/chromedriver.exe')
driver = webdriver.Chrome(service=s)

def scrollPage(driver):
    i = 1
    scroll_pause_time = 1 
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

def get_Id(url):
    data = []
    driver.get(url)
    time.sleep(2)  # Allow 2 seconds for the web page to open
    
    while True:
        scrollPage(driver)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        hotel_id = soup.find_all("li",{"class":"data-hotelid"})
       
        for x in hotel_id:
            data.append(x.text)

        button_next = driver.find_elements_by_class_name('pagination2__next')
        if len(button_next)>0:
            button_next = button_next[0]
        else:
            break
        driver.execute_script("arguments[0].click();",button_next)
        time.sleep(5)
    return data