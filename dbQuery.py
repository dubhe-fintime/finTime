import re

## 날짜인지 확인하는 하는 정규식 
def validate_date(date_string):
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(date_pattern.match(date_string))

#####################################
#####################################
##            쿼리 모음             ##
#####################################
#####################################
# 쿼리 모음
def selectQuery(qType, values):
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@S")
    # print("Query Id : "+qType)
    # if len(values) > 0:
    #     print(values)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@E")
    if qType == "Q1": # BACTH LOG 등록
        query = "INSERT INTO BATCH_LOG (BATCH_ID, BATCH_NM, TASK_ID, TASK_NM, ST_DATE, ED_DATE, STATUS, RESULT_DATA) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    elif qType == "Q2": # BACTH 데이터 등록
        query = "INSERT INTO BATCH_RST (COR_NO, EVT_TITLE, EVT_ID, EVT_ST_DATE, EVT_ED_DATE, EVT_THUMBNAIL, EVT_IMG, EVT_NOTI, EVT_LIST_LINK, EVT_DT_LINK) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    elif qType == "Q3": # BACTH 데이터 전체 삭제
        query = "DELETE FROM BATCH_RST"
    elif qType == "Q4": # FILE 업로드 등록
        query = "INSERT INTO FILE_MST (FILE_NM, ORG_FILE_NM, FILE_EXTENSION, FILE_PATH) VALUES (%s, %s, %s, %s)"
    elif qType == "Q5": # FILE 삭제
        query = "DELETE FROM FILE_MST WHERE FILE_NM = %s"
    elif qType == "Q6": # FILE 조회
        query = "SELECT FILE_NM, ORG_FILE_NM, FILE_EXTENSION, FILE_PATH FROM FILE_MST"
    
    elif qType == "QTEMP": # 임시 배치 테이블 조회
        query = "SELECT * FROM BATCH_RST" # 임시 배치 테이블 추후 EVT_MST 호출



        

    

        
    # print("###################################")
    # print(query)
    # print("###################################")
    return query
