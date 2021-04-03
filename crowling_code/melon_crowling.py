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

url = 'https://www.melon.com/index.htm'
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
#멜론차트 탭 클릭
driver.find_element_by_css_selector("li.nth1").click() 
time.sleep(2) 
#차트파인더 클릭
driver.find_element_by_class_name('btn_chart_f').click()
time.sleep(3)
#월간차트 클릭
driver.find_element_by_css_selector("h4.tab02").click() 
time.sleep(1)
#2020년대~2010년대 버튼 클릭을 위해 for문 사용
for decade in range(1,3):
    id_1 = 'decade_%s' %(str(decade))
    #click함수를 사용하면 에러가 나서 execute_script함수 사용
    element = driver.find_element_by_id(id_1)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1)
    #연도에서 2010~2019년, 2020~2021년을 클릭하기위해 for문사용
    for year in range(1,11):
        id_2 = 'year_%s' %(str(year))
        #2020년대는 2020, 2021 2개 밖에 없으므로 try문을 활용하여 예외처리
        try:
            element = driver.find_element_by_id(id_2)
        except:
            break
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        #1~12월 클릭하기위해 for문 사용
        for month in range(1,13):
            id_3 = 'month_%s' %(str(month))
            #2021년은 2월까지존재하므로 try문 활용하여 예외처리
            try:
                element = driver.find_element_by_id(id_3)
            except:
                break
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
            #장르종합 박스 클릭
            element = driver.find_element_by_xpath("//input[@id='gnr_1']")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
            #검색버튼 클릭
            driver.find_element_by_class_name('btn_b26').click()
            time.sleep(3)
            #월간차트별로 csv파일을 저장할 것이므로 빈 리스트(rssult)를 여기에 생성
            result=[]
            boxItems = driver.find_elements_by_css_selector('#chartListObj > tr')
            for item in boxItems:
                album = item.find_element_by_css_selector('td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank03 > a').text
                #앨법명에 OST가 포함된 것만 크롤링하기위해 if문 사용
                if 'OST' in album: 
                    rank = item.find_element_by_css_selector('td:nth-child(2) > div > span:nth-child(1)').text
                    title = item.find_element_by_css_selector('td:nth-child(4) > div > div > div.ellipsis.rank01 > span > strong > a').text
                    #가수가 여러명인 경우를 대비하기위해 list로 받은 후 순차적으로 text를 저장
                    singer_list = item.find_elements_by_css_selector('td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank02 > a')
                    singer=[]
                    for singer1 in singer_list:
                        if singer1.text != '':
                            singer.append(singer1.text)
                    #순위, 제목, 가수, 앨범명 순서로 결과저장
                    result.append([rank]+[title]+[singer]+[album])
            #51~100순위 차트로 넘어간 후 정보수집
            driver.execute_script("javascript:movePage(2)")
            time.sleep(3)
            boxItems = driver.find_elements_by_css_selector('#chartListObj > tr')
            for item in boxItems:
                album = item.find_element_by_css_selector('td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank03 > a').text
                if 'OST' in album:
                    rank = item.find_element_by_css_selector('td:nth-child(2) > div > span:nth-child(1)').text
                    title = item.find_element_by_css_selector('td:nth-child(4) > div > div > div.ellipsis.rank01 > span > strong > a').text
                    singer_list = item.find_elements_by_css_selector('td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank02 > a')
                    singer=[]
                    for singer1 in singer_list:
                        if singer1.text != '':
                            singer.append(singer1.text)
                    result.append([rank]+[title]+[singer]+[album])
            #csv파일 제목에 년도, 월을 쓰기위해 정보 크롤링
            boxItems = driver.find_elements_by_css_selector('#conts > div > div.wrap_serch_value')
            for item in boxItems:
                #년도
                tt1 = item.find_element_by_css_selector('#serch_cnt > span:nth-child(1)').text
                #월
                tt2 = item.find_element_by_css_selector('#serch_cnt > span:nth-child(3)').text
            #월간차트 csv파일로 저장
            melon_table = pd.DataFrame(result, columns=('rank', 'title', 'singer', 'album'))
            melon_table.to_csv("%s년 %s월 멜론차트.csv" %(str(tt1), str(tt2))) #encoding='cp949'