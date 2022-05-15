import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import numpy as np
import pandas as pd
from pathlib import Path


def scrollPage(driver):
    i = 1
    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    while True:
        # scroll one screen height each time
        driver.execute_script(
            "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break


def checkNullData(index):
    if(index != None):
        return index.text
    else:
        return '0 '


def get_Data(url):
    s = Service(r'./chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    data = []
    driver.get(url)
    time.sleep(2)  # Allow 2 seconds for the web page to open

    while True:
        scrollPage(driver)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        hotel = soup.find_all("li", {"class": "PropertyCard PropertyCardItem"})
        print('count = ', len(hotel))

        for item in hotel:
            data.append(item)

        button_next = driver.find_elements_by_class_name('pagination2__next')
        if len(button_next) > 0:
            button_next = button_next[0]
        else:
            time.sleep(2)
            break
        driver.execute_script("arguments[0].click();", button_next)
        
    return data

def getIndex(hotels):
    hotel_id = []
    hotel_name = []
    hotel_start = []
    hotel_adress = []
    hotel_price = []
    hotel_price_sale = []
    hotel_url = []
    hotel_review = []
    hotel_num_of_review = []
    hotel_rating_average = []
    hotel_active = []
    hotel_image = []
    i = 0
    loss = 0
    for x in hotels:
        #Lấy dữ liệu
        try:
            idh = x.get('data-hotelid')
            name = x.find("h3",{"class":"PropertyCard__HotelName"}).text
            start = x.find("i",{"id":"NHAWEB-2124"}).get('title')
            adress = x.find("span",{"class":"Address__Text"}).text
            price = checkNullData(x.find("div",{"class":"PropertyCardPrice"}))
            price_sale = checkNullData(x.find("span",{"class":"PropertyCardPrice__Value"}))
            url =  x.find("a", {"class":"PropertyCard__Link"})['href']
            review = checkNullData(x.find("span",{"class":"Spanstyled__SpanStyled-sc-16tp9kb-0 kkSkZk kite-js-Span Box-sc-kv6pi1-0 eRxXoo"}))
            num_of_review = checkNullData(x.find("span",{"class":"Spanstyled__SpanStyled-sc-16tp9kb-0 jYmZbG kite-js-Span Box-sc-kv6pi1-0 jjmSNA"}))
            rating_average = checkNullData(x.find("p",{"class":"Typographystyled__TypographyStyled-sc-j18mtu-0 Hkrzy kite-js-Typography"}))
            active = checkNullData(x.find("button",{"class":"Buttonstyled__ButtonStyled-sc-5gjk6l-0 evAQLf"}))
            image = x.find("div",{"class":"Overlay"}).find('img')['src']
        
            #Xử lý dữ liệu
            start = float(start[:start.find(" ")] if (start[:start.find(" ")].strip()) else 0)
            price = price[:price.find(" ")].replace('.', '')
            price_sale = price_sale[:price_sale.find(" ")].replace('.', '')
            num_of_review = int(num_of_review[:num_of_review.find(" ")].replace('.', ''))
            rating_average = rating_average.replace(',', '.')
            url = 'https://www.agoda.com/' + url
        
            #Thêm dữ liệu
            hotel_id.append(idh)
            hotel_name.append(name)
            hotel_start.append(start)
            hotel_adress.append(adress)
            hotel_price.append(price)
            hotel_price_sale.append(price_sale)
            hotel_url.append(url)
            hotel_rating_average.append(rating_average)
            hotel_num_of_review.append(num_of_review)
            hotel_review.append(review)
            hotel_active.append(active)
            hotel_image.append(image)
            i+=1
        except Exception as e:
            print(e)
            i+=1
            loss+= 1
            print('hotel count',i,',id-hotel=',idh,',hotel-name: ',name, ',error: ',e)
    print('loss : ',loss)
    d = { 'hotel_id' : hotel_id
         ,'hotel_name' : hotel_name
         ,'hotel_start' : hotel_start
         ,'hotel_adress' : hotel_adress
         ,'hotel_price' : hotel_price
         ,'hotel_price_sale' : hotel_price_sale
         ,'hotel_url' : hotel_url
         ,'hotel_rating_average' : hotel_rating_average
         ,'hotel_review' : hotel_review
         ,'hotel_num_of_review' : hotel_num_of_review
         ,'hotel_active' : hotel_active
         ,'hotel_image' : hotel_image}
    # Ghi vào data
    dFrame = pd.DataFrame(d)
    # lọc các dòng trùng nhau
    dFrame = dFrame.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
    return dFrame

def getAll(url):
    hotels = get_Data(url)
    print("Sum hotel = ", len(hotels))
    return getIndex(hotels)
    