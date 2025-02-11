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
    
    




        

    

        
    # print("###################################")
    # print(query)
    # print("###################################")
    return query
