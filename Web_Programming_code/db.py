import pymysql
# pip install pandas

# 버전 확인 
# print(pymysql.__version__)

# 데이터 베이스에 접속하는 함수
def get_connection() :
    conn = pymysql.connect(host='127.0.0.1', user='root',
            password='yhj970217^*^', db='flaskdb'
            , charset='utf8')
    # print(conn)
    if conn:
        print('디비 접속 완료')
        print(conn)
             
    return conn


# 전체 레코드 조회 함수
def get_member_all() :
    # 데이터베이스 접속
    conn = get_connection()

    # 작업변수 생성
    cursor = conn.cursor()

    # 쿼리문
    # userID 정렬 기준
    sql = "SELECT * FROM membertbl;"
    # 쿼리실행 
    cursor.execute(sql)

    # 결과를 가져온다.
    # fetchone() 
    # fetchall()
    # fetchmany(n)
    result = cursor.fetchall()
    
    # 데이터를 추출한다.
    # 딕셔너리 리스트 구조
    temp_list = []

    # 리스트안의 딕셔너리 구조화 emp_no, first_name, last_name, gender
    for row in result :
        temp_dic = {}
        temp_dic['userNo'] = row[0]
        temp_dic['useId'] = row[1]
        temp_dic['userName'] = row[2]
        temp_dic['pwd'] = row[3]

        # 딕셔너리를 리스트로 삽입 
        temp_list.append(temp_dic)

    conn.close()
    return temp_list


# id 값을 이용해서 특정 레코드 조회
def get_member_one(userId) :
    # 데이터베이스 접속
    conn = get_connection()

    # 작업변수 생성
    cursor = conn.cursor()

    # 쿼리문
    # id 값을 이용해서 특정 레코드 조회 
    sql = "SELECT * FROM membertbl WHERE userId=%s;"
    # 쿼리실행
    cursor.execute(sql, userId)

    # 결과를 가져온다.
    result = cursor.fetchone()
    if result:
    # 딕셔너리 구조로 변경
        temp_dic = {}
        temp_dic['userNo'] = result[0]
        temp_dic['useId'] = result[1]
        temp_dic['userName'] = result[2]
        temp_dic['pwd'] = result[3]
        conn.close()
        return temp_dic

#레코트 추가함수
def add_member(userId, userName, pwd):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "insert into membertbl (userId, userName, pwd) values (%s, %s, %s)"

    cursor.execute(sql, (userId, userName, pwd))

    conn.commit()
    conn.close()

#회원 추가 테스트
#add_member('kokomong', '나훈아', '0000')


# userId, pwd 데이 값 확인함수 
# 레코드 한개 조회 함수 
def login_result(userId, pwd):
    # 데이터베이스 접속
    conn = get_connection()

    # 작업변수 생성
    cursor = conn.cursor()

    # 쿼리문
    # userId, pwd 값을 이용해서 특정 레코드 조회 
    sql = "SELECT * FROM memberTbl WHERE userId=%s AND pwd=%s;"
    # 쿼리실행 
    cursor.execute(sql, (userId, pwd))

    # 결과를 가져온다.
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False
