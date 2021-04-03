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



def drama(i) :
    keys = '%s년 종영드라마' %(str(i))
    # 처음 검색은 상관이 없는데 두번째 검색할 때는 해당 검색어가 남아있어서 지워주어야 한다.
    driver.find_element_by_id('nx_query').clear()
    driver.find_element_by_id('nx_query').send_keys(keys)
    driver.find_element_by_class_name('bt_search').click()
    time.sleep(3)

    # %s년 종영드라마를 검색한 후 크롤링하는 코드
    end = int(driver.find_element_by_css_selector('div.cm_paging_area.no_margin._kgs_page > div > span > span._total').text)
    page = 1
    # end는 종영 드라마 페이지의 끝을 알기 위해서, page는 현재 페이지를 의미한다.
    result_title = []
    result_drama_link = []
    # 검색결과를 저장하는 리스트들로 result_title은 종영드라마 전체 제목을, drama_link는 각 드라마별 소개 페이지로 가는 링크가 담겨있다.
    # result_drama_people은 제작진+배우의 이름을 저장하고, 해당 사람들의 링크를 담고 있는 것이 result_drama_people_link이다.
    # 위의 두 개의 리스트는 모두 이중 리스트로 첫 번째 인덱스와 일치하는 인덱스로 title을 검색했을 때 해당 드라마의 제목이 나오도록 하였다.

    for _ in count() :
        drama_table = driver.find_elements_by_css_selector("#mflick > div > div.box_card_image_list._list > ul > li")
        # 드라마 제목을 가지고 오는 코드
        for ele in drama_table :
            title = ele.find_element_by_css_selector('strong').text
            # ul이 보이는 페이지만 유효한 값을 가지고 있어서 ''은 빼주는 작업이 필요하다.
            if title != '' :
                result_title.append(title)
        
        # 드라마 링크를 가지고 오는 코드
        for ele in drama_table :
            link = ele.find_element_by_css_selector('strong > a').get_attribute('href')
            # 보이지 않는 페이지의 링크까지 모두 가지고 와서 있는 링크는 제외시키도록 하였다.
            if link not in result_drama_link :
                result_drama_link.append(link)

        # 페이지 검색을 멈추어 주는 코드
        page = page+1
        if page > end : break

        driver.find_element_by_css_selector("a.pg_next._next.on").click()  
        time.sleep(2)
    
    # 해당 년도 종영 드라마의 총 수
    drama_total = len(result_title)
    return result_title, result_drama_link, drama_total

for i in range(2017,2021) :
    d_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(d_url)
    result_drama_link = drama(i)[1]   
    result=[] 
    for url in result_drama_link:
        # 드라마의 기본 정보를 가지고 오는 코드
        content_url = url + '%20기본정보'
        driver.get(content_url)
        time.sleep(3)
        writer_link = ''
        writer_name = ''
        try:
            drama_name = driver.find_element_by_css_selector('div.title_area._title_area > h2 > a > strong').text
                                                            
        except:
            try:
                drama_name = driver.find_element_by_css_selector('div.title_area._title_area > h2 > span > strong').text
            except:
                drama_name = ''

        making = driver.find_elements_by_css_selector('div.pro_info_box > dl > div:nth-child(1) > dd> ul >li')
        for ele in making :
            if '극본' in ele.find_element_by_css_selector('span.info').text:
                try:
                    writer_name = ele.find_element_by_css_selector('span.text > a').text 
                except:
                    try: 
                        writer_name = ele.find_element_by_css_selector('span.text').text 
                    except:
                        writer_name = ''  
                try:
                    writer_link = ele.find_element_by_css_selector('span.text > a').get_attribute('href')
                except:
                    writer_link = ''
        
        try:
            driver.get(writer_link)
            time.sleep(3)
            writer_link = driver.find_element_by_css_selector('#people_info_z > div > div.api_cs_wrap > div.go_relate > a.btn_txt_more').get_attribute('href')
            driver.get(writer_link)
            time.sleep(3)
            informations = driver.find_elements_by_css_selector('#content > div > div.workact_wrap > dl > dd > span')
            board_num = 0
            movie_num = 0
            for information in informations:
                if '방송' in information.text :
                    board_num = information.text[2:-1]
                if '영화' in information.text :
                    movie_num = information.text[2:-1]
        except :
            directors = driver.find_elements_by_css_selector('div.pro_info_box > dl > div:nth-child(2) > dd > ul >li')
            for ele in directors :
                if '극본' in ele.find_element_by_css_selector('span.info').text:
                    try:
                        writer_name = ele.find_element_by_css_selector('span.text > a').text 
                    except:
                        try: 
                            writer_name = ele.find_element_by_css_selector('span.text').text 
                        except:
                            writer_name = ''
                    try:
                        writer_link = ele.find_element_by_css_selector('span.text > a').get_attribute('href')
                    except:
                        writer_link = ''
            try:
                driver.get(writer_link)
                time.sleep(3)
                writer_link = driver.find_element_by_css_selector('#people_info_z > div > div.api_cs_wrap > div.go_relate > a.btn_txt_more').get_attribute('href')
                driver.get(writer_link)
                time.sleep(3)
                informations = driver.find_elements_by_css_selector('#content > div > div.workact_wrap > dl > dd > span')
                board_num = 0
                movie_num = 0
                for information in informations:
                    if '방송' in information.text :
                        board_num = information.text[2:-1]
                    if '영화' in information.text :
                        movie_num = information.text[2:-1]
                    
            except:
                board_num = ''
                movie_num = ''

        print(drama_name)
        print(writer_name)
        print(board_num)
        print(movie_num)
        result.append([drama_name]+[writer_name]+[board_num]+[movie_num])
    drama_table = pd.DataFrame(result, columns=('drama_name', 'writer_name','writer_board_num', 'writer_movie_num'))
    drama_table.to_csv("%s년 작가정보.csv" %(str(i))) #encoding='cp949'