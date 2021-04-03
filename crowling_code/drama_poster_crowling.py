import urllib.request
import ssl
from bs4 import BeautifulSoup
import datetime
import math
import pandas as pd
from selenium import webdriver
from itertools import count
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request

context = ssl._create_unverified_context()

def get_request_url(url, enc='utf-8') :
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url)
    try :
        response = urllib.request.urlopen(req, context=context)
        if response.getcode() == 200 :
            try :
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError :
                ret = rcv.decode(enc, 'replace')
            return ret
    except Exception as e :
        print(e)
        print("[%s] Error for URL" %datetime.datetime.now())

d_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
driver = webdriver.Chrome('chromedriver.exe')
driver.get(d_url)

for i in range(2019, 2020):
    keys = '%s년 종영드라마' %(str(i))
    # 처음 검색은 상관이 없는데 두번째 검색할 때는 해당 검색어가 남아있어서 지워주어야 한다.
    driver.find_element_by_id('nx_query').clear()
    driver.find_element_by_id('nx_query').send_keys(keys)
    time.sleep(1)
    driver.find_element_by_class_name('bt_search').click()
    time.sleep(3)

    # %s년 종영드라마를 검색한 후 크롤링하는 코드
    end = int(driver.find_element_by_css_selector('div.cm_paging_area.no_margin._kgs_page > div > span > span._total').text)
    page = 1
    # end는 종영 드라마 페이지의 끝을 알기 위해서, page는 현재 페이지를 의미한다.
    result_title = []
    img_url = []
    for _ in count() :
        drama_table = driver.find_elements_by_css_selector("#mflick > div > div.box_card_image_list._list > ul > li")
        img_data = driver.find_elements_by_css_selector('#mflick > div > div.box_card_image_list._list > ul > li > div.thumb_area > a > img')
        
        #이미지 src주소를 가져오는 코드
        for k in img_data:
            url_i = k.get_attribute('src')
            img_url.append(url_i)
        # 드라마 제목을 가지고 오는 코드
        for ele in drama_table :
            title = ele.find_element_by_css_selector('strong').text
            # ul이 보이는 페이지만 유효한 값을 가지고 있어서 ''은 빼주는 작업이 필요하다.
            if title != '' :
                result_title.append(title)
                

        # 페이지 검색을 멈추어 주는 코드
        page = page+1
        if page > end: break

        driver.find_element_by_css_selector("a.pg_next._next.on").click()  
        time.sleep(2)
    
    #드라마제목리스트(result_title)의 index번호를 위해 num변수 선언
    num = 0
    # img_url에 이미지src주소가 중복되어 들어가는 경우가 발생해서 중복값제거를 시행
    new_list = []
    for v in img_url:
        if v not in new_list:
            new_list.append(v)
    #new_list에 있는 이미지src주소를 for문을 이용해서 하나씩 저장
    for j in new_list:
        urllib.request.urlretrieve(j, "img/%s년/%s_%s.jpg" %(str(i), str(num), str(result_title[num])))
        num +=1


