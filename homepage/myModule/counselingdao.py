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
def getSmallCate(bname, mname):
    print("DB에서 가져와야해 "+bname + mname)
    sql = "SELECT sname FROM counsel_cate_s WHERE bname=%s AND mname=%s"
    params = (bname, mname)
    return common_sql(1, sql, params)

# 상담번호를 통해 모범상담 내용 가져오기
def getMobumCounsel(counselID):
    sql = "SELECT title, big_cate, question_date, question, answer_date, answer FROM counsel WHERE counsel_id=%s"
    return common_sql(1, sql, counselID)

# 업종 가져오기
def getGijun():
    sql = "SELECT category_name FROM solution GROUP BY category_name"
    return common_sql(1, sql)

# 업종에 따른 분쟁유형 1 가져오기
def getTrouble1(upjongName):
    sql = "SELECT type_1 FROM solution WHERE category_name=%s GROUP BY type_1"
    # sql = "SELECT gijun.type_1 FROM solution_gijun gijun, solution_category cate WHERE gijun.category_id=cate.id AND cate.category_name=%s GROUP BY gijun.type_1"
    return common_sql(1, sql, upjongName)

# 분쟁유형1에 따른 분쟁유형2 가져오기
def getTrouble2(upjongName, trouble1):
    sql = "SELECT type_2 FROM solution WHERE category_name=%s AND type_1=%s GROUP BY type_2"
    params=(upjongName,trouble1)
    # sql = "SELECT gijun.type_2 FROM solution_gijun gijun, solution_category cate WHERE gijun.category_id=cate.id AND cate.category_name=%s AND cate.type_1=%s GROUP BY gijun.type_2"
    return common_sql(1, sql, params)

# 분쟁유형2에 따른 분쟁유형3 가져오기
def getTrouble3(upjongName, trouble1, trouble2):
    sql = "SELECT type_3 FROM solution WHERE category_name=%s AND type_1=%s AND type_2=%s GROUP BY type_3"
    params=(upjongName,trouble1, trouble2)
    # sql = "SELECT gijun.type_2 FROM solution_gijun gijun, solution_category cate WHERE gijun.category_id=cate.id AND cate.category_name=%s AND cate.type_1=%s GROUP BY gijun.type_2"
    return common_sql(1, sql, params)

# 분쟁유형3에 따른 분쟁유형4 가져오기
def getTrouble4(upjongName, trouble1, trouble2, trouble3):
    sql = "SELECT type_4 FROM solution WHERE category_name=%s AND type_1=%s AND type_2=%s AND type_3=%s GROUP BY type_4"
    params=(upjongName,trouble1, trouble2, trouble3)
    # sql = "SELECT gijun.type_2 FROM solution_gijun gijun, solution_category cate WHERE gijun.category_id=cate.id AND cate.category_name=%s AND cate.type_1=%s GROUP BY gijun.type_2"
    return common_sql(1, sql, params)

# 해결기준과 비고 가져오기
def getStandardBigo(cname, t1, t2='', t3='', t4=''):
    print(cname, t1, t2, t3, t4)
    sql = "SELECT category_name, type_1, standard, bigo FROM solution where category_name=%s AND type_1=%s AND type_2=%s AND type_3=%s AND type_4=%s"
    params = (cname, t1, t2, t3, t4)
    return common_sql(1, sql, params)



# 들어온 소분류로 태깅된 단어 빈도수 체크
def countGijunBySmall(sname):
    sql = 'select type_1, b.category_id, c.category_name from itemlist as a join solution_gijun as b on a.category_id = b.category_id join solution_category as c on b.category_id = c.id where a.name = %s'
    return common_sql(1, sql, sname)

# 들어온 중분류로 태깅된 단어 빈도수 체크
def countGijunByMiddle(mname):
    sql = 'select type_1, b.category_id, c.category_name from itemlist as a join solution_gijun as b on a.category_id = b.category_id join solution_category as c on b.category_id = c.id where a.name = %s'
    return common_sql(1, sql, mname)

def getGijunList(type1, id):
    print(type1, id)
    sql = 'select type_1, type_2, type_3, type_4, standard, bigo from solution_gijun where type_1 = %s and category_id = %s'
    params = (type1, id)
    return common_sql(1, sql, params)



# 태깅을 위한 해당 중분류 모범상담 태그 데이터 불러오기
def getMobum(mname):
    sql = 'select id from mid_category where name = %s'
    return common_sql(1, sql, mname)