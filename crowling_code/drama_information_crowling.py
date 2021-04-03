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

d_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
driver = webdriver.Chrome('chromedriver.exe')
driver.get(d_url)

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

for i in range(2020,2021) :
    result = drama(i)
    result_drama_link = result[1]
    result_title = result[0] 
    result_drama_people = []
    result_drama_people_link = []
    result_drama_infotmation = []
    result_people_num = []

    # 드라마 상세페이지에서 크롤링하는 코드
    for url in result_drama_link :
        # 이중 리스트로 저장하기 위해 새로운 list를 선언한다.
        drama_person_link = []
        drama_information = []
        # 드라마의 기본 정보를 가지고 오는 코드

        content_url = url + '%20기본정보'
        driver.get(content_url)
        time.sleep(2)
        # 방송사 정보
        board = driver.find_element_by_css_selector('div.detail_info > dl > div:nth-child(1) > dd > a').text
        # 방송된 전체 날짜 정보
        Day = driver.find_element_by_css_selector('div.detail_info > dl > div:nth-child(1) > dd > span').text[:26]
        # 총 회수에 대한 정보
        total = driver.find_element_by_css_selector('div.detail_info > dl > div:nth-child(1) > dd > span >em').text
        # 요일과 시간에 대한 정보 -> 없는 경우 오류가 나서 오류 처리를 해주었다.
        try :
            week = driver.find_element_by_css_selector('div.detail_info > dl > div:nth-child(1) > dd > span:nth-child(3)').text
        except :
            # week에 대한 정보가 없으면 정보 저장을 하지 않는다.
            week = ''
        # 드라마 소개에 대한정보
        content = driver.find_element_by_css_selector('div.cm_content_wrap > div:nth-child(2) > div > div.intro_box > p').text
        # 제작사에 대한 정보 -> 없는 경우 오류가 나서 오류 처리를 해주었다.
        try :
            making = driver.find_element_by_css_selector('div.pro_info_box > dl > div:nth-child(1) > dd').text
        except :
            # making에 대한 정보가 없으면 정보 저장을 하지 않는다.
            making = ''

        # 주연 배우 5명 크롤링하는 코드
        person_url = url + '%20등장인물'
        driver.get(person_url)
        time.sleep(2)
        response = get_request_url(driver.current_url)
        soupData = BeautifulSoup(response, 'html.parser')
        Data = soupData.find('ul', {'class' : 'tab_list'})
        people = Data.find('li', {'aria-selected' : 'true'}).text
        time.sleep(3)

        # 등장인물이 없는 드라마는 데이터 수집에 의미가 없어서 제외한다.
        if  '전체' in people :
            i = result_drama_link.index(url)
            result_title = result_title[:i] + result_title[i+1:]
            result_drama_link = result_drama_link[:i] + result_drama_link[i+1:]
        else :
            drama_people = ['', '', '', '', '']
            people = driver.find_elements_by_css_selector('span.sub_text.type_ell_2._html_ellipsis')
            try :
                for i in range(5) :
                    try :
                        drama_person_link.append(people[i].find_element_by_css_selector('a').get_attribute('href'))
                    except :
                        continue
                    drama_people[i] = people[i].text
                # 등장인물이 들어가 있는 위치가 드라마마다 달라서 css를 간단하게 잡았다.
                # 하나 하나 선택을 할 수가 없어서 등장인물 전체 페이지를 잡아서 맨 앞에 두 개에 대한 정보만 받아왔다.
                # 전체 페이지를 가져온 것이 list의 형태이기 때문에 인덱스로 잘랐다.
            except :
                for i in range(len(people)) :
                    drama_people[i] = people[i].text
                    drama_person_link.append(people[i].find_element_by_css_selector('a').get_attribute('href'))
            # 여기까지 코드가 오면 제작진과 배우의 이름은 drama_people 리스트에
            # 각 해당하는 사람들의 link는 drama_person_link 리스트에 들어가게 된다.

            drama_information.append(board)
            drama_information.append(Day)
            drama_information.append(total)
            drama_information.append(week)
            drama_information.append(content)
            drama_information.append(making)

            # 시청률 정보를 크롤링하는 코드
            view_url = url + '%20시청률'
            driver.get(view_url)
            response = get_request_url(driver.current_url)
            soupData = BeautifulSoup(response, 'html.parser')
            Data = soupData.find('ul', {'class' : 'tab_list'})
            V = Data.find('li', {'aria-selected' : 'true'}).text
            time.sleep(2)

            # 등장인물 정보는 있는데 시청률 정보가 없을 경우 시청률은 저장하지 않는다.
            if '전체' in V :
                view = []
            else :
                view = list(driver.find_element_by_css_selector('g.bb-texts.bb-texts-rank').text.split('\n'))
            drama_information.append(view)

            result_drama_people.append(drama_people)
            result_drama_people_link.append(drama_person_link)
            result_drama_infotmation.append(drama_information)
        # 리스트에 리스트를 append함으로써 이중 리스트가 완성된다.
        # 각 드라마 상세페이지를 돌 때마다 drama_people과 drama_person_link가 초기화 되기 때문에 
        # 드라마 별로 list가 만들어지고 최종 list에 list 자체가 들어가기 때문에 드라마 별로 접근이 쉬워진다.

    # 드라마 인물 상세 정보를 크롤링하는 코드
    for i in range(len(result_drama_people_link)) :
        people_num = ['', '', '', '', '', '', '', '', '', '']
        k = 0
        for url in result_drama_people_link[i] :
            driver.get(url)
            more = driver.find_element_by_css_selector('#people_info_z > div > div.api_cs_wrap > div.go_relate > a.btn_txt_more').get_attribute('href')
            driver.get(more)
            time.sleep(2)

            informations = driver.find_elements_by_css_selector('#content > div > div.workact_wrap > dl > dd > span')
            board_num = '0'
            movie_num = '0'
            for information in informations:
                if '방송' in information.text :
                    board_num = information.text[2:-1]
                if '영화' in information.text :
                    movie_num = information.text[2:-1]
            people_num[k] = board_num
            people_num[k+1] = movie_num
            k = k+2
        result_people_num.append(people_num)

    final_list = []
    for i in range(len(result_title)) :
        final_list.append([result_title[i]]+ [result_drama_infotmation[i][0]]+ [result_drama_infotmation[i][1]]+ [result_drama_infotmation[i][2]]+ \
                [result_drama_infotmation[i][3]]+ [result_drama_infotmation[i][4]]+ [result_drama_infotmation[i][5]]+[result_drama_infotmation[i][6]]+ \
                [result_drama_people[i][0]]+ [result_people_num[i][0]]+ [result_people_num[i][1]]+ [result_drama_people[i][1]]+\
                [result_people_num[i][2]]+[result_people_num[i][3]]+ [result_drama_people[i][2]]+ [result_people_num[i][4]]+ [result_people_num[i][5]]+ \
                [result_drama_people[i][3]]+[result_people_num[i][6]]+ [result_people_num[i][7]]+ [result_drama_people[i][4]]+ [result_people_num[i][8]]+\
                [result_people_num[i][9]])
        
    table = pd.DataFrame(final_list, columns=('드라마 이름', '방송사', '방송기간', '총 부작', '요일 및 시간', '내용', '제작사', '시청률', \
                '등장인물_1', '방송갯수_1', '영화갯수_1', '등장인물_2', '방송갯수_2', '영화갯수_2', '등장인물_3', '방송갯수_3', '영화갯수_3', \
                '등장인물_4', '방송갯수_4', '영화갯수_4', '등장인물_5', '방송갯수_5', '영화갯수_5'))
    table.to_csv('%s년 드라마.csv' %str(i), encoding='cp949', index=False)
