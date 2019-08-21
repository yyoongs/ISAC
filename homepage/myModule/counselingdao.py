# -- coding: utf-8 --
#python mysql 연결 드라이버
import pymysql
import time
import datetime

def getConnection():
    return pymysql.connect(host = '133.130.122.150', user = "pingu", password = "datacampus12", db = "ISAC")

#sql 중복 부분 리팩토링
def sql_template(type, sql, params=None):
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
def getCounseling(title):
    sql = "select title, big_cate, mid_cate, question_date, question from realtime_counsel where title=%s"

    return sql_template(1, sql, (title,))

#넘어온 상담들 등록
def setCounseling(counsel):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    #넘어온 데이터중 빈값이 있으면 0 리턴
    # 처리하기

    sql = "INSERT INTO realtime_counsel (title, big_cate, mid_cate, small_cate, question_date, question) VALUES (%s, %s, %s, %s, %s, %s)"
    params = (counsel['title'], counsel['big'], counsel['mid'],counsel['small'],  timestamp, counsel['question'])
    return sql_template(3, sql, params)

# 해결기준 가져오기
def getGijun():
    sql = "SELECT category_name FROM category cate, solution_gijun gijun where cate.id=gijun.id"
    return sql_template(1, sql)