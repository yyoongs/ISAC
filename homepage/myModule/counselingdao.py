# -- coding: utf-8 --
# 모델 부분을 (일단) 여기가 대신하고 있음
import pymysql

def getConnection():
    return pymysql.connect(host = '133.130.122.150', user = "pingu", password = "datacampus12", db = "ISAC")

#sql 중복 부분 리팩토링
def common_sql(type, sql, params=None):
    # Connection 연결
    connetion = getConnection()
    try:
        #insert, update, delete 사용
        if type == 3 :
            with connetion.cursor() as cursor :
                # 데이터 입력
                cursor.execute(sql, params)

                # commit
                connetion.commit()
        else :
            # 1 = fetchall() 2 = fetchone()
            with connetion.cursor(pymysql.cursors.DictCursor) as cursor :
                # SQL 처리
                cursor.execute(sql, params)
                # 처리된 data 가져옴
                if type == 1 :
                    return cursor.fetchall()
                elif type == 2 :
                    return cursor.fetchone()
    finally:
        # Connection 닫기
        connetion.close()

# 상담 가져오기
def getCounseling(questionDate):
    sql = "select title, big_cate, mid_cate, question_date, question from realtime_counsel where question_date=%s"
    print(questionDate)
    return common_sql(1, sql, (questionDate,))

#넘어온 상담들 등록
def setCounseling(counsel):
    # 넘어온 데이터중 빈값이 있으면 0 리턴
    # 대분류, 중분류에서 전체가 넘어오면 * 으로 처리하기

    sql = "INSERT INTO realtime_counsel (title, big_cate, mid_cate, small_cate, question_date, question) VALUES (%s, %s, %s, %s, %s, %s)"
    params = (counsel['title'], counsel['big_cate'], counsel['mid_cate'],counsel['small_cate'],  counsel['question_date'], counsel['question'])
    return common_sql(3, sql, params)

# 대분류 가져오기
def getBigCate():
    sql = "SELECT name FROM big_category"
    return common_sql(1, sql)

# 대분류에 따른 중분류 가져오기
def getMidCate(bname):
    sql = "SELECT mname FROM counsel_cate WHERE bname=%s"
    return common_sql(1, sql, bname)

# 중분류에 따른 소분류 가져오기
def getSmallCate(mname):
    print(mname)
    sql = "SELECT s.name FROM small_category s, mid_category m WHERE s.mid_id=m.id AND m.name=%S"
    return common_sql(1, sql, mname)

# 상담번호를 통해 모범상담 내용 가져오기
def getMobumCounsel(counselID):
    sql = "SELECT title, big_cate, question_date, question, answer_date, answer FROM counsel WHERE counsel_id=%s"
    return common_sql(1, sql, counselID)

# 업종 가져오기
def getGijun():
    sql = "SELECT category_name FROM category cate, solution_gijun gijun where cate.id=gijun.id"
    return common_sql(1, sql)

# 업종에 따른 분쟁유형 1 가져오기
def getTrouble1(upjongName):
    sql = "SELECT gijun.type_1 FROM solution_gijun gijun, category cate WHERE gijun.category_id=cate.id AND cate.category_name=%s GROUP BY gijun.type_1"
    return common_sql(1, sql, upjongName)

# 해결기준과 비고 가져오기
def getStandardBigo(str1, str2):
    sql = "SELECT cate.category_name, gijun.type_1, gijun.standard, gijun.bigo FROM solution_gijun gijun, category cate where cate.category_name=%s AND type_1=%s"
    params = (str1, str2)
    return common_sql(1, sql, params)